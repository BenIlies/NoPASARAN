import h2.connection
import h2.config
import nopasaran.tools.http_2_overwrite
from h2.settings import SettingCodes
from nopasaran.definitions.events import EventNames
from nopasaran.http_2_utils import (
    create_ssl_context,
    create_socket,
    H2_CONFIG_SETTINGS,
)
from nopasaran.tools.http_2_socket_base import HTTP2SocketBase
import socket

class HTTP2SocketClient(HTTP2SocketBase):
    def start(self, tls_enabled = False, protocol = 'h2', connection_settings_client = {}):
        """Handle IDLE state: Create connection and move to WAITING_PREFACE"""
        self.sock = create_socket(self.host, self.port)
        self.sock.settimeout(self.TIMEOUT)  # Set socket timeout
        
        try:
            # First attempt the connection
            self.sock.connect((self.host, self.port))
            
            if tls_enabled == 'true':
                ssl_context = create_ssl_context(
                    protocol=protocol,
                    is_client=True
                )
                
                self.sock = ssl_context.wrap_socket(
                    self.sock,
                    server_hostname=self.host
                )
            
        except TimeoutError as e:
            return EventNames.TIMEOUT.name, f"Timeout occurred after {self.TIMEOUT}s while trying to connect to server at {self.host}:{self.port}: {e}"
        except ConnectionRefusedError as e:
            return EventNames.TIMEOUT.name, f"Connection refused by server at {self.host}:{self.port}. Server may not be running or port may be blocked: {e}"
        
        config_settings = H2_CONFIG_SETTINGS.copy()
        config_settings.update(connection_settings_client)
        config = h2.config.H2Configuration(client_side=True, **config_settings)
        self.conn = h2.connection.H2Connection(config=config)
        # Send connection preface
        self.conn.initiate_connection()
        self.sock.sendall(self.conn.data_to_send())

        selected_protocol = self.sock.selected_alpn_protocol() if tls_enabled == 'true' else None
        
        # Send a test message to verify the connection
        try:
            # Create a new stream for our test message
            stream_id = self.conn.get_next_available_stream_id()
            
            # Send headers
            headers = [
                (':method', 'GET'),
                (':path', '/test-connection'),
                (':scheme', 'https' if tls_enabled == 'true' else 'http'),
                (':authority', self.host),
                ('user-agent', 'nopasaran-test-client'),
            ]
            self.conn.send_headers(stream_id, headers, end_stream=False)
            
            # Send a small data frame with test message
            test_data = "HTTP/2 connection test from nopasaran client"
            self.conn.send_data(stream_id, test_data.encode('utf-8'), end_stream=True)
            
            # Send the data to the server
            self.sock.sendall(self.conn.data_to_send())
            
            # Try to read a response (optional, with timeout)
            self.sock.settimeout(1.0)  # Short timeout for test response
            try:
                response_data = self.sock.recv(1024)
                # Process received data
                if response_data:
                    events = self.conn.receive_data(response_data)
                    for event in events:
                        if isinstance(event, h2.events.DataReceived):
                            return EventNames.CLIENT_STARTED.name, f"Client successfully connected to {self.host}:{self.port} with {f'TLS with ALPN protocol {selected_protocol}' if tls_enabled == 'true' else 'non-TLS'} connection. Received response from server: {len(event.data)} bytes."
            except socket.timeout:
                # No response is fine for this test
                pass
            finally:
                # Reset timeout to original value
                self.sock.settimeout(self.TIMEOUT)
        except Exception as e:
            # If test message fails, the connection was still established
            return EventNames.CLIENT_STARTED.name, f"Client connected to {self.host}:{self.port} but test message failed: {e}"
        
        return EventNames.CLIENT_STARTED.name, f"Client successfully connected to {self.host}:{self.port} with {f'TLS with ALPN protocol {selected_protocol}' if tls_enabled == 'true' else 'non-TLS'} connection. Test message sent."