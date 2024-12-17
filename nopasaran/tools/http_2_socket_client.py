import time
import http_2_overwrite
import h2.connection
import h2.config
import h2.events
import ssl
from nopasaran.http_2_utils import (
    setup_logging,
    create_ssl_context,
    create_socket,
    SSL_CONFIG,
    log_h2_frame,
    H2_CONFIG_SETTINGS,
    send_frame
)
import socket
from checks import function_map

# Add at the top with other constants
FRAME_TIMEOUT_SECONDS = 2  # Increased from 1 to 2 seconds
MAX_RETRY_ATTEMPTS = 3

class HTTP2Client:
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
        data = self.sock.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
        return data

    def wait_for_server_preface(self):
        """Wait for server's SETTINGS frame"""
        data = self._receive_frame()
        if data:
            events = self.conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.RemoteSettingsChanged):
                    outbound_data = self.conn.data_to_send()  # This will generate SETTINGS ACK
                    if outbound_data:
                        self.sock.sendall(outbound_data)

    def wait_for_server_ack(self):
        """Wait for server's SETTINGS_ACK frame"""
        data = self._receive_frame()
        if data:
            events = self.conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.SettingsAcknowledged):
                    outbound_data = self.conn.data_to_send()
                    if outbound_data:
                        self.sock.sendall(outbound_data)


    def send_frames(self, client_frames):
        """Send frames based on test case"""
        for frame in client_frames:
            send_frame(self.conn, self.sock, frame)

        # Add a small delay to ensure frames are transmitted
        time.sleep(0.1)

    def receive_frames(self, server_frames):
        """Wait for server's frames"""
        retry_count = 0
                
        for frame in server_frames:
            data = self._receive_frame()
            if data is None:  # Timeout occurred
                retry_count += 1
                if retry_count >= MAX_RETRY_ATTEMPTS:
                    return
                continue
            
            else:
                retry_count = 0  # Reset retry counter on successful receive
                events = self.conn.receive_data(data)
                self._handle_test(events[0], frame)

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

    # def close_connection(self):
    #     """Handle CLOSING state: Send GOAWAY if needed and close the connection"""
    #     try:
    #         # Only send GOAWAY if it wasn't the last frame sent
    #         last_frame = self.test_case.get('client_frames', [])[-1] if self.test_case else None
    #         if not last_frame or last_frame.get('type') != 'GOAWAY':
    #             self.conn.close_connection()
    #             self.sock.sendall(self.conn.data_to_send())
            
    #         # Wait briefly for any final messages
    #         try:
    #             self.sock.settimeout(0.1)
    #             while not self.conn.state_machine.state == h2.connection.ConnectionState.CLOSED:
    #                 data = self.sock.recv(SSL_CONFIG.MAX_BUFFER_SIZE)
    #                 if not data:
    #                     break
    #                 events = self.conn.receive_data(data)
    #                 for event in events:
    #                     self._handle_frame(event)
    #     finally:
    #         self.state = ClientState.CLOSED
    #         if self.sock:
    #             self.sock.close()
    #             self.sock = None
    #             self.conn = None