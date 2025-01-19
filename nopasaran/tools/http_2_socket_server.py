import time
import select
import h2.config
import h2.connection
import h2.events
import nopasaran.tools.http_2_overwrite
from nopasaran.tools.checks import function_map
from nopasaran.definitions.events import EventNames
from nopasaran.http_2_utils import (
    create_ssl_context,
    create_socket,
    SSL_CONFIG,
    H2_CONFIG_SETTINGS,
    send_frame
)

TIMEOUT = 10
MAX_RETRY_ATTEMPTS = 3

class HTTP2SocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None
        self.conn = None
        self.client_socket = None

    def start(self, tls_enabled = False, protocol = 'h2', connection_settings_server = {}):
        """Start the HTTP/2 server"""
        self.sock = create_socket(self.host, self.port, is_server=True)
        self.sock.listen(5)
        
        self.client_socket, address = self.sock.accept()    
        
        if tls_enabled:
            ssl_context = create_ssl_context(
                protocol=protocol,
                is_client=False
            )
            
            self.client_socket = ssl_context.wrap_socket(
                self.client_socket,
                server_side=True
            )
        
        config_settings = H2_CONFIG_SETTINGS.copy()
        config_settings.update(connection_settings_server)
        config = h2.config.H2Configuration(client_side=False, **config_settings)
        self.conn = h2.connection.H2Connection(config=config)
        
        # Send connection preface
        self.conn.initiate_connection()
        self.client_socket.sendall(self.conn.data_to_send())

    def _receive_frame(self) -> bytes:
        """Helper method to receive data"""
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > TIMEOUT:
                return None
            
            ready_to_read, _, _ = select.select([self.client_socket], [], [], TIMEOUT)
            if ready_to_read:
                frame = self.client_socket.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
                return frame

    def wait_for_client_preface(self) -> str:
        """Wait for client's connection preface"""
        data = self._receive_frame()
        if data is None:
            return EventNames.TIMEOUT.name
        
        events = self.conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.RemoteSettingsChanged):
                outbound_data = self.conn.data_to_send()  # This will generate SETTINGS ACK
                if outbound_data:
                    self.client_socket.sendall(outbound_data)

        return EventNames.PREFACE_RECEIVED.name
    
    def wait_for_client_ack(self) -> str:
        """Wait for server's SETTINGS_ACK frame"""
        data = self._receive_frame()
        if data is None:
            return EventNames.TIMEOUT.name
        
        events = self.conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.SettingsAcknowledged):
                outbound_data = self.conn.data_to_send()
                if outbound_data:
                    self.client_socket.sendall(outbound_data)

        return EventNames.ACK_RECEIVED.name

    def receive_client_frames(self, client_frames) -> bool | str:
        """
            Wait for client's frames

            Returns:
                - True if 
                    - the test passed or 
                    - the proxy dropped the frames (timed out)
                - False if 
                    - the test failed or 
                    - no tests were run and the proxy did not drop the frames
        """
        retry_count = 0
        for frame in client_frames:
            data = self._receive_frame()

            # if data is None, it means the proxy dropped the frames (so conformant?)
            if data is None:
                retry_count += 1
                if retry_count >= MAX_RETRY_ATTEMPTS:
                    return True, EventNames.TIMEOUT.name
                continue
            
            retry_count = 0  # Reset retry counter on successful receive
            events = self.conn.receive_data(data)

            # if there is a test for the frame, it will run it and return True or False. If no test exists, it will return None
            result, test_index = self._handle_test(events[0], frame)

            # if a test passes, return True
            if result is True:
                return True, EventNames.TEST_PASSED.name, f'Test {test_index} passed'
            elif result is False:
                return False, EventNames.TEST_FAILED.name, "All tests failed for the frame"
        
        # will reach here if there were no individual tests to run and the proxy did not drop the frames (no timeout)
        return False, EventNames.TEST_FAILED.name, "No tests were found for the frame and the proxy did not drop the frames"

    def send_frames(self, server_frames):
        """Send frames based on test case"""
        for frame in server_frames:
            send_frame(self.conn, self.client_socket, frame)
        
        # Add a small delay to ensure frames are transmitted
        time.sleep(0.1)

        return EventNames.FRAMES_SENT.name

    def _handle_test(self, event, frame) -> bool | int | None:
        """
        Handle test cases for received frames.
        Each scenario can have multiple tests, where each test contains multiple checks.
        A test passes if all its checks pass. A scenario passes if one of its tests passes.

        Returns:
            - True if the test passed
            - False if the test failed
            - None if no tests were found for that frame
        """
        tests = frame.get('tests', [])

        if not tests:
            return None, None
        
        for test_index, test in enumerate(tests, 1):
            all_checks_passed = True
            
            # Try all checks in this test
            for check in test:
                function_name = check['function']
                params = check['params']
                
                function = function_map.get(function_name)

                # check if check exists
                if not function:
                    all_checks_passed = False
                    break
                
                # run the check. if it fails, break the loop
                if not function(event, *params):
                    all_checks_passed = False
                    break
            
            if all_checks_passed:
                return True, test_index  # Exit after first successful test
        
        # If we get here, all tests failed
        return False, None