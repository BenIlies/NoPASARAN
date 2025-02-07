import time
import select
import h2.connection
import h2.config
import h2.events
from nopasaran.tools.checks import function_map
from nopasaran.definitions.events import EventNames
from nopasaran.http_2_utils import (
    SSL_CONFIG,
    send_frame
)

class HTTP2SocketBase:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None
        self.conn = None
        self.MAX_RETRY_ATTEMPTS = 3
        self.TIMEOUT = 10

    def _receive_frame(self) -> bytes:
        """Helper method to receive data"""
        start_time = time.time()
        socket_to_check = self.sock if not hasattr(self, 'client_socket') else self.client_socket
        
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > self.TIMEOUT:
                return None
            
            ready_to_read, _, _ = select.select([socket_to_check], [], [], self.TIMEOUT)
            if ready_to_read:
                frame = socket_to_check.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
                return frame

    def send_frames(self, frames):
        """Send frames based on test case"""
        socket_to_use = self.sock if not hasattr(self, 'client_socket') else self.client_socket
        
        for frame in frames:
            send_frame(self.conn, socket_to_use, frame)
        
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
                
                if not function(event, *params):
                    all_checks_passed = False
                    break
            
            if all_checks_passed:
                return True, test_index  # Exit after first successful test
        
        # If we get here, all tests failed
        return False, None
    
    def wait_for_preface(self) -> str:
        """Wait for preface"""
        data = self._receive_frame()
        if data is None:
            return EventNames.TIMEOUT.name, "Timeout occurred while waiting for preface"
        
        events = self.conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.RemoteSettingsChanged):
                outbound_data = self.conn.data_to_send()  # This will generate SETTINGS ACK
                if outbound_data:
                    socket_to_use = self.sock if not hasattr(self, 'client_socket') else self.client_socket
                    socket_to_use.sendall(outbound_data)

                return EventNames.PREFACE_RECEIVED.name, "Preface received"

        return EventNames.ERROR.name, "Proxy returned an error"
    
        
    def wait_for_preface_ack(self) -> str:
        """Wait for PREFACE_ACK frame"""
        data = self._receive_frame()
        if data is None:
            return EventNames.TIMEOUT.name, "Timeout occurred while waiting for PREFACE_ACK frame"
        
        events = self.conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.SettingsAcknowledged):
                outbound_data = self.conn.data_to_send()
                if outbound_data:
                    socket_to_use = self.sock if not hasattr(self, 'client_socket') else self.client_socket
                    socket_to_use.sendall(outbound_data)

        return EventNames.ACK_RECEIVED.name, "PREFACE_ACK frame received"
    
    def receive_test_frames(self, test_frames) -> str:
        """Wait for test frames"""
        retry_count = 0
        frames_received = []
        result = None
        
        for frame in test_frames:
            data = self._receive_frame()

            if data is None:
                retry_count += 1
                if retry_count >= self.MAX_RETRY_ATTEMPTS:
                    return EventNames.TIMEOUT.name, "Timeout occurred", frames_received
                continue
            
            retry_count = 0
            events = self.conn.receive_data(data)
            frames_received.append(events)
            
            for event in events:
                result, test_index = self._handle_test(event, frame)

                if result is True:
                    return EventNames.TEST_COMPLETED.name, f'Test {test_index} passed with frame {event}', frames_received
                elif result is False:
                    continue
        
        if frames_received == [] and test_frames != []:
            return EventNames.TEST_COMPLETED.name, "Expected frames were not received", frames_received
        
        if result is None:
            return EventNames.TEST_COMPLETED.name, "Frames were received but no tests were defined.", frames_received
        else:
            return EventNames.TEST_COMPLETED.name, "Frames were received but all tests failed", frames_received

    def close(self):
        """Close the HTTP/2 connection and clean up resources"""
        try:
            if self.conn:
                # Send GOAWAY frame to indicate graceful shutdown
                self.conn.close_connection()
                socket_to_use = self.sock if not hasattr(self, 'client_socket') else self.client_socket
                if socket_to_use:
                    socket_to_use.sendall(self.conn.data_to_send())
            
            # Close sockets
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.close()
            if self.sock:
                self.sock.close()
            
            # Clear references
            self.conn = None
            if hasattr(self, 'client_socket'):
                self.client_socket = None
            self.sock = None
            
            return EventNames.CONNECTION_CLOSED.name
        except Exception as e:
            return EventNames.ERROR.name