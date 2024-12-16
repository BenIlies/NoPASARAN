import socket
import http_2_overwrite
import h2.config
import h2.connection
import h2.events
import ssl
from checks import function_map
from http2_utils import (
    create_ssl_context,
    create_socket,
    SSL_CONFIG,
    H2_CONFIG_SETTINGS,
    send_frame
)
import time

FRAME_TIMEOUT_SECONDS = 1  # Timeout when waiting for frames

class HTTP2SocketServer:
    def __init__(self, host, port):
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
        frame = self.client_socket.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
        return frame

    def wait_for_client_preface(self):
        """Wait for client's connection preface"""
        data = self._receive_frame()
        if data:
            events = self.conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.RemoteSettingsChanged):
                    outbound_data = self.conn.data_to_send()  # This will generate SETTINGS ACK
                    if outbound_data:
                        self.client_socket.sendall(outbound_data)

    def wait_for_client_ack(self):
        """Wait for server's SETTINGS_ACK frame"""
        data = self._receive_frame()
        if data:
            events = self.conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.SettingsAcknowledged):
                    outbound_data = self.conn.data_to_send()
                    if outbound_data:
                        self.client_socket.sendall(outbound_data)

    def receive_client_frames(self, client_frames):
        """Wait for client's frames"""
        for frame in client_frames:
            data = self._receive_frame()
            if data is None:  # Timeout occurred
                return
            
            else:
                events = self.conn.receive_data(data)
                self._handle_test(events[0], frame)

    def send_frames(self, server_frames):
        """Send frames based on test case"""
        for frame in server_frames:
            send_frame(self.conn, self.client_socket, frame)
        
        # Add a small delay to ensure frames are transmitted
        time.sleep(0.1)

    def _handle_test(self, event, frame):
        """
        Handle test cases for received frames.
        Each frame can have multiple tests, where each test contains multiple checks.
        A test passes if all its checks pass.
        We try each test until one passes completely, or all tests fail.
        """
        tests = frame.get('tests', [])

        if not tests:
            return
        
        for test_index, test in enumerate(tests, 1):
            all_checks_passed = True
            
            # Try all checks in this test
            for check in test:
                function_name = check['function']
                params = check['params']
                
                function = function_map.get(function_name)
                if not function:
                    all_checks_passed = False
                    break
                
                if not function(event, *params):
                    all_checks_passed = False
                    break
            
            if all_checks_passed:
                return  # Exit after first successful test
        
        # If we get here, all tests failed

    def close_connection(self):
        """Handle response waiting state."""        
        for i in range(1):
            data = self._receive_frame()
            events = self.conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.ConnectionTerminated):
                    self.client_socket.close()