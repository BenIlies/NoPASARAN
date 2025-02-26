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
        self.TIMEOUT = 5
        self.cloudflare_origin = False

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
        """Send frames and check for GOAWAY response"""
        socket_to_use = self.sock if not hasattr(self, 'client_socket') else self.client_socket
        sent_frames = []
        is_server = hasattr(self, 'client_socket')
        
        for frame in frames:
            send_frame(self.conn, socket_to_use, frame, is_server)
            sent_frames.append(frame)
            
            # Check for GOAWAY response after sending each frame
            data = self._receive_frame()
            if data is not None:
                events = self.conn.receive_data(data)
                for event in events:
                    if isinstance(event, h2.events.ConnectionTerminated):
                        return (
                            EventNames.GOAWAY_RECEIVED.name,
                            str(sent_frames),
                            f"Connection terminated by peer: Received GOAWAY frame with error code {event.error_code}. Additional data: {event.additional_data}."
                        )
        
        return EventNames.FRAMES_SENT.name, str(sent_frames), f"Successfully sent {len(sent_frames)} frames."

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
        #skip function
        # if self.cloudflare_origin:
        return EventNames.PREFACE_RECEIVED.name, f"Successfully received peer's preface.", None

        data = self._receive_frame()
        if data is None:
            return EventNames.TIMEOUT.name, f"Timeout after {self.TIMEOUT}s while waiting for peer's preface (SETTINGS frame)", None
        
        events = self.conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.RemoteSettingsChanged):
                outbound_data = self.conn.data_to_send()  # This will generate SETTINGS ACK
                if outbound_data:
                    socket_to_use = self.sock if not hasattr(self, 'client_socket') else self.client_socket
                    socket_to_use.sendall(outbound_data)

                return EventNames.PREFACE_RECEIVED.name, f"Successfully received peer's preface.", str(event)

        return EventNames.ERROR.name, f"Expected SETTINGS frame for preface but received error instead", str(events)
    
        
    def wait_for_preface_ack(self) -> str:
        """Wait for PREFACE_ACK frame"""
        data = self._receive_frame()
        if data is None:
            return EventNames.TIMEOUT.name, f"Timeout after {self.TIMEOUT}s while waiting for peer's SETTINGS ACK frame"
        
        events = self.conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.SettingsAcknowledged):
                outbound_data = self.conn.data_to_send()
                if outbound_data:
                    socket_to_use = self.sock if not hasattr(self, 'client_socket') else self.client_socket
                    socket_to_use.sendall(outbound_data)

            return EventNames.ACK_RECEIVED.name, "Successfully received peer's SETTINGS ACK frame"

        return EventNames.ERROR.name, f"Expected SETTINGS ACK frame but received: {events}"
    
    def receive_test_frames(self, test_frames) -> str:
        """Wait for test frames with adaptive timeout"""
        frames_received = []
        expected_frame_count = len(test_frames)
        last_frame_time = time.time()
        
        while len(frames_received) < expected_frame_count:
            data = self._receive_frame()
            
            if data is not None:
                last_frame_time = time.time()
                events = self.conn.receive_data(data)
                
                for event in events:
                    if isinstance(event, h2.events.StreamReset):
                        return EventNames.CONNECTION_TERMINATED.name, f"Stream {event.stream_id} reset after receiving {len(frames_received)}/{expected_frame_count} frames. Got error code {event.error_code}.", str(events)

                    if isinstance(event, h2.events.ConnectionTerminated):
                        return EventNames.CONNECTION_TERMINATED.name, f"Peer terminated connection after receiving {len(frames_received)}/{expected_frame_count} frames. Got error code {event.error_code}.", str(events)
                    
                    # Skip initial settings frame
                    if isinstance(event, h2.events.RemoteSettingsChanged):
                        settings = event.changed_settings.items()
                        if len(settings) >= 2:
                            continue
                    
                    # Skip initial settings ACK
                    if isinstance(event, h2.events.SettingsAcknowledged):
                        continue

                    if isinstance(event, h2.events.StreamEnded):
                        continue

                    if isinstance(event, h2.events.WindowUpdated):
                        continue

                    if isinstance(event, h2.events.DataReceived):
                        # check content if equal to 'Connection test from client'
                        if event.data == 'Connection test from client':
                            continue

                    if isinstance(event, h2.events.ResponseReceived):
                        # check for 5xx status code
                        for header_name, header_value in event.headers:
                            if header_name == ':status':
                                if int(header_value) >= 500:
                                    return EventNames.CONNECTION_TERMINATED.name, f"Received 5xx status code {header_value} after receiving {len(frames_received)}/{expected_frame_count} frames.", str(event)

                    # Filter for connection-test headers
                    if isinstance(event, h2.events.RequestReceived):
                        # Headers are a list of tuples in h2, not a dictionary
                        path_header = None
                        for header_name, header_value in event.headers:
                            if header_name == ':path':
                                path_header = header_value
                                break
                        
                        if path_header == '/connection-test':
                            continue

                    frames_received.append(event)

                    if len(frames_received) == expected_frame_count:
                        return EventNames.TEST_COMPLETED.name, f"Successfully received all {len(frames_received)}/{expected_frame_count} frames.", str(frames_received)
                    
                    # Check tests after each frame is received
                    # for expected_frame in test_frames:
                    #     result, test_index = self._handle_test(event, expected_frame)
                    #     if result is True:
                    #         return EventNames.TEST_COMPLETED.name, f'Test {test_index} passed successfully. Matching frame: {event}', str(frames_received)
                    
            
            # Check for timeout since last frame
            elif time.time() - last_frame_time > self.TIMEOUT:
                return EventNames.TIMEOUT.name, f"Timeout after {self.TIMEOUT}s. Received {len(frames_received)} of {expected_frame_count} expected frames.", str(frames_received)
        
        # If we get here with all frames but no test passed
        # if expected_frame_count == 0:
        #     if len(frames_received) == 0:
        #         return EventNames.TEST_COMPLETED.name, "No frames were expected or received", str(frames_received)
        #     else:
        #         return EventNames.TEST_COMPLETED.name, f"Received {len(frames_received)} unexpected frames", str(frames_received)
        
        # if result is False:
        #     return EventNames.TEST_COMPLETED.name, f"Successfully received all {expected_frame_count} frames but none matched test criteria.", str(frames_received)
        # else:
        #     return EventNames.TEST_COMPLETED.name, f"Successfully received all {expected_frame_count} expected frames.", str(frames_received)

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