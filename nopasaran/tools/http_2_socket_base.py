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
        self.TIMEOUT = 5.0
        self.cloudflare_origin = False

    def _receive_frame(self, timeout = None) -> bytes:
        """Helper method to receive data"""
        try:
            start_time = time.time()
            socket_to_check = self.sock if not hasattr(self, 'client_socket') else self.client_socket
            
            if timeout is None:
                timeout = self.TIMEOUT
            
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    return None
                
                remaining = max(0, timeout - elapsed_time)
                ready_to_read, _, _ = select.select([socket_to_check], [], [], remaining)
                
                if ready_to_read:
                    frame = socket_to_check.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
                    return frame
        except (ConnectionResetError, BrokenPipeError) as e:
            # Connection was terminated by the peer
            return None
        except Exception as e:
            # Log unexpected errors
            return None

    def send_frames(self, frames):
        """Send frames with GOAWAY checking after each frame"""
        socket_to_use = self.sock if not hasattr(self, 'client_socket') else self.client_socket
        sent_frames = []
        is_server = hasattr(self, 'client_socket')
        reaction_window = 0.3  # seconds to drain control events after sends
        idle_grace = 0.05      # stop early if idle for this long
        
        for frame in frames:
            # Send the current frame
            send_frame(self.conn, socket_to_use, frame, is_server, self.cloudflare_origin)
            sent_frames.append(frame)

            # Flush socket after each frame to ensure it's sent
            outbound_data = self.conn.data_to_send()
            if outbound_data:
                socket_to_use.sendall(outbound_data)
            
            # Drain readable data for a bounded window to catch control frames deterministically
            drain_start = time.time()
            last_activity = drain_start
            while True:
                now = time.time()
                if (now - drain_start) >= reaction_window:
                    break
                # Stop early if idle
                if (now - last_activity) >= idle_grace:
                    break
                remaining = max(0.0, min(idle_grace, reaction_window - (now - drain_start)))
                ready_to_read, _, _ = select.select([socket_to_use], [], [], remaining)
                if not ready_to_read:
                    continue
                data = socket_to_use.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
                if not data:
                    continue
                last_activity = time.time()
                events = self.conn.receive_data(data)
                # Send any acks generated
                outbound = self.conn.data_to_send()
                if outbound:
                    socket_to_use.sendall(outbound)
                for event in events:
                    if isinstance(event, h2.events.ConnectionTerminated):
                        return (
                            EventNames.GOAWAY_RECEIVED.name,
                            str(sent_frames),
                            f"Connection terminated by peer: Received GOAWAY frame after sending {len(sent_frames)} of {len(frames)} frames. Error code {getattr(event, 'error_code', 'unknown')}. Additional data: {getattr(event, 'additional_data', b'')}"
                        )
                    if isinstance(event, h2.events.StreamReset):
                        return (
                            EventNames.RESET_RECEIVED.name,
                            str(sent_frames),
                            f"Stream {event.stream_id} reset by peer: Received StreamReset after sending frame #{len(sent_frames)} of {len(frames)}: {frame.get('type')}. Error code {getattr(event, 'error_code', 'unknown')}"
                        )
                    if isinstance(event, h2.events.ResponseReceived) or isinstance(event, h2.events.RequestReceived):
                        for header_name, header_value in event.headers:
                            if header_name == ':status' and int(header_value) >= 500:
                                return (
                                    EventNames.REJECTED.name,
                                    str(sent_frames),
                                    f"Received 5xx status code {header_value} after sending {len(sent_frames)}/{len(frames)} frames."
                                )

        # Final short drain for any late control frames
        drain_start = time.time()
        while time.time() - drain_start < 0.1:
            ready_to_read, _, _ = select.select([socket_to_use], [], [], 0.1)
            if not ready_to_read:
                break
            data = socket_to_use.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
            if not data:
                break
            events = self.conn.receive_data(data)
            outbound = self.conn.data_to_send()
            if outbound:
                socket_to_use.sendall(outbound)
            for event in events:
                if isinstance(event, h2.events.ConnectionTerminated):
                    return (
                        EventNames.GOAWAY_RECEIVED.name,
                        str(sent_frames),
                        f"Connection terminated by peer: Received GOAWAY frame with error code {getattr(event, 'error_code', 'unknown')}. Additional data: {getattr(event, 'additional_data', b'')}"
                    )
        
        return EventNames.FRAMES_SENT.name, str(sent_frames), f"Successfully sent {len(sent_frames)} frames."

    def _handle_test(self, event, frame) -> None | str:
        """
        Handle test cases for received frames.
        Tests contain a single check with dictionary parameters and conditional results.

        Returns:
            - The result of the test if it passed
            - None if no tests were found for that frame
        """
        test = frame.get('test', {})
        
        function_name = test.get('function')
        params = test.get('params', {})
        
        function = function_map.get(function_name)

        # Execute the function with unpacked dictionary parameters
        result = function(event, **params)
        
        # Return based on the test result and specified conditions
        if result == True:
            return test['if_true']
        elif result == False:
            return test['if_false']
        elif result is None:
            return None
    
    def receive_test_frames(self, test_frames) -> str:
        """Wait for test frames with adaptive timeout"""
        frames_received = []
        expected_frame_count = len(test_frames)
        last_frame_time = time.time()
        start_time = time.time()

        
        while len(frames_received) < expected_frame_count:
            # Check for overall timeout
            if time.time() - start_time > self.TIMEOUT * 2:  # Double timeout for overall operation
                return EventNames.TIMEOUT.name, f"Overall timeout after {self.TIMEOUT * 2}s. Received {len(frames_received)} of {expected_frame_count} expected frames.", str(frames_received)
            
            # Check for timeout since last frame
            if time.time() - last_frame_time > self.TIMEOUT:
                return EventNames.TIMEOUT.name, f"Timeout after {self.TIMEOUT}s since last frame. Received {len(frames_received)} of {expected_frame_count} expected frames.", str(frames_received)
            
            data = self._receive_frame()
            
            if data is not None:
                last_frame_time = time.time()
                events = self.conn.receive_data(data)
                
                for event in events:
                    if isinstance(event, h2.events.StreamReset):
                        return EventNames.RESET_RECEIVED.name, f"Stream {event.stream_id} reset after receiving {len(frames_received)}/{expected_frame_count} frames. Got error code {event.error_code}.", str(events)

                    if isinstance(event, h2.events.ConnectionTerminated):
                        return EventNames.GOAWAY_RECEIVED.name, f"Peer terminated connection after receiving {len(frames_received)}/{expected_frame_count} frames. Got error code {event.error_code}.", str(events)
                    
                    # Skip initial settings frame
                    if isinstance(event, h2.events.RemoteSettingsChanged):
                        settings = event.changed_settings.items()
                        if len(settings) >= 2:
                            continue
                    
                    # Skip initial settings ACK
                    if isinstance(event, h2.events.SettingsAcknowledged) \
                        or isinstance(event, h2.events.StreamEnded) \
                        or isinstance(event, h2.events.WindowUpdated):
                        continue

                    if isinstance(event, h2.events.DataReceived):
                        # Compare bytes to bytes
                        if event.data == b'Connection test from client':
                            continue

                    if isinstance(event, h2.events.ResponseReceived) or isinstance(event, h2.events.RequestReceived):
                        # check for 5xx status code
                        for header_name, header_value in event.headers:
                            if header_name == ':status' and int(header_value) >= 500:
                                return EventNames.REJECTED.name, f"Received 5xx status code {header_value} after receiving {len(frames_received)}/{expected_frame_count} frames.", str(event)

                    # Filter for connection-test headers
                    if isinstance(event, h2.events.RequestReceived):
                        for header_name, header_value in event.headers:
                            if header_name == ':path' and header_value == '/connection-test':
                                continue

                    frames_received.append(event)

                    # Move test handling before the frame count check
                    for frame in test_frames:
                        if frame.get('test'):
                            result = self._handle_test(event, frame)
                            if result is not None:
                                return EventNames.RECEIVED_FRAMES.name, f"Test result: {result}", str(frames_received)
                    
                    if len(frames_received) == expected_frame_count:
                        return EventNames.RECEIVED_FRAMES.name, f"Successfully received all {len(frames_received)}/{expected_frame_count} frames.", str(frames_received)

    def wait_for_preface(self):
        """Wait for peer SETTINGS (preface). Returns (event, msg, frames)."""
        socket_to_check = self.sock if not hasattr(self, 'client_socket') else self.client_socket
        frames = []
        start_time = time.time()
        while time.time() - start_time < self.TIMEOUT:
            ready_to_read, _, _ = select.select([socket_to_check], [], [], max(0, self.TIMEOUT - (time.time() - start_time)))
            if not ready_to_read:
                continue
            data = socket_to_check.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
            if not data:
                continue
            events = self.conn.receive_data(data)
            # Send any acknowledgements
            outbound_data = self.conn.data_to_send()
            if outbound_data:
                socket_to_check.sendall(outbound_data)
            for event in events:
                frames.append(event)
                if isinstance(event, h2.events.RemoteSettingsChanged):
                    return EventNames.RECEIVED_FRAMES.name, "Received peer SETTINGS preface.", str(frames)
        return EventNames.TIMEOUT.name, f"Timeout after {self.TIMEOUT}s waiting for peer preface.", str(frames)

    def wait_for_preface_ack(self):
        """Wait for peer SETTINGS ACK. Returns (event, msg)."""
        socket_to_check = self.sock if not hasattr(self, 'client_socket') else self.client_socket
        start_time = time.time()
        while time.time() - start_time < self.TIMEOUT:
            ready_to_read, _, _ = select.select([socket_to_check], [], [], max(0, self.TIMEOUT - (time.time() - start_time)))
            if not ready_to_read:
                continue
            data = socket_to_check.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
            if not data:
                continue
            events = self.conn.receive_data(data)
            outbound_data = self.conn.data_to_send()
            if outbound_data:
                socket_to_check.sendall(outbound_data)
            for event in events:
                if isinstance(event, h2.events.SettingsAcknowledged):
                    return EventNames.RECEIVED_FRAMES.name, "Received SETTINGS ACK from peer."
        return EventNames.TIMEOUT.name, f"Timeout after {self.TIMEOUT}s waiting for SETTINGS ACK."

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