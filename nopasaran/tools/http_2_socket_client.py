import time
import select
import h2.connection
import h2.config
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

# Add at the top with other constants
MAX_RETRY_ATTEMPTS = 3
TIMEOUT = 10

class HTTP2SocketClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None
        self.conn = None

    def start(self, tls_enabled = False, protocol = 'h2', connection_settings_client = {}):
        """Handle IDLE state: Create connection and move to WAITING_PREFACE"""
        self.sock = create_socket(self.host, self.port)

        if tls_enabled:
            ssl_context = create_ssl_context(
                protocol=protocol,
                is_client=False
            )
            
            self.sock = ssl_context.wrap_socket(
                self.sock,
                server_hostname=self.host
            )
        
        self.sock.connect((self.host, self.port))
        
        config_settings = H2_CONFIG_SETTINGS.copy()
        config_settings.update(connection_settings_client)
        config = h2.config.H2Configuration(client_side=True, **config_settings)
        self.conn = h2.connection.H2Connection(config=config)
        
        # Send connection preface
        self.conn.initiate_connection()
        self.sock.sendall(self.conn.data_to_send())

    def _receive_frame(self) -> bytes:
        """Helper method to receive data"""
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > TIMEOUT:
                return None
            
            ready_to_read, _, _ = select.select([self.sock], [], [], TIMEOUT)
            if ready_to_read:
                frame = self.sock.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
                return frame

    def wait_for_server_preface(self) -> str:
        """Wait for server's SETTINGS frame"""
        data = self._receive_frame()
        if data is None:
            return EventNames.TIMEOUT.name
        
        events = self.conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.RemoteSettingsChanged):
                outbound_data = self.conn.data_to_send()  # This will generate SETTINGS ACK
                if outbound_data:
                    self.sock.sendall(outbound_data)

        return EventNames.PREFACE_RECEIVED.name

    def wait_for_server_ack(self) -> str:
        """Wait for server's SETTINGS_ACK frame"""
        data = self._receive_frame()
        if data is None:
            return EventNames.TIMEOUT.name
        
        events = self.conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.SettingsAcknowledged):
                outbound_data = self.conn.data_to_send()
                if outbound_data:
                    self.sock.sendall(outbound_data)

        return EventNames.ACK_RECEIVED.name

    def send_frames(self, client_frames):
        """Send frames based on test case"""
        for frame in client_frames:
            send_frame(self.conn, self.sock, frame)

        # Add a small delay to ensure frames are transmitted
        time.sleep(0.1)

        return EventNames.FRAMES_SENT.name

    def receive_server_frames(self, server_frames) -> bool | str:
        """
            Wait for server's frames
        
            Returns:
                - True if 
                    - the test passed or 
                    - the proxy dropped the frames (timed out)
                - False if 
                    - the test failed or 
                    - no tests were run and the proxy did not drop the frames
        """
        retry_count = 0
                
        for frame in server_frames:
            data = self._receive_frame()

            # if data is None, it means the proxy dropped the frames (so conformant?)
            if data is None:  # Timeout occurred
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
        
        return False, EventNames.TEST_FAILED.name, "No tests were found for the frame and the proxy did not drop the frames"

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
                
                if not function(event, *params):
                    all_checks_passed = False
                    break
            
            if all_checks_passed:
                return True, test_index  # Exit after first successful test
        
        # If we get here, all tests failed
        return False, None