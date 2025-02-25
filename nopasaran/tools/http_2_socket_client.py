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
import time

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
        
        # Send a test HTTP/2 request to ensure connection establishment
        try:
            # Create a new stream for our test message
            stream_id = self.conn.get_next_available_stream_id()
            
            # Send headers
            headers = [
                (':method', 'GET'),
                (':path', '/connection-test'),
                (':scheme', 'https' if tls_enabled == 'true' else 'http'),
                (':authority', self.host),
                ('user-agent', 'nopasaran-http2-client'),
            ]
            self.conn.send_headers(stream_id, headers, end_stream=False)
            
            # Send a small data frame with test message
            test_data = "Connection test from client"
            self.conn.send_data(stream_id, test_data.encode('utf-8'), end_stream=True)
            
            # Send the data to the server
            self.sock.sendall(self.conn.data_to_send())
            
            # Wait for response with timeout
            self.sock.settimeout(5.0)  # Longer timeout for response
            response_received = False
            start_time = time.time()
            
            # Keep trying to receive data until we get a response or timeout
            while not response_received and (time.time() - start_time) < 5.0:
                try:
                    response_data = self.sock.recv(1024)
                    if response_data:
                        events = self.conn.receive_data(response_data)
                        # Look for any data or headers on our stream
                        for event in events:
                            if (hasattr(event, 'stream_id') and event.stream_id == stream_id) or \
                               isinstance(event, h2.events.ResponseReceived) or \
                               isinstance(event, h2.events.DataReceived):
                                response_received = True
                                break
                        
                        # Send any necessary data in response
                        data_to_send = self.conn.data_to_send()
                        if data_to_send:
                            self.sock.sendall(data_to_send)
                        
                        # If we got data but no relevant response yet, keep trying
                        if not response_received:
                            continue
                except socket.timeout:
                    # Timeout on this receive attempt, but we'll try again if time remains
                    pass
            
            if not response_received:
                return EventNames.ERROR.name, "HTTP/2 test request received no response"
        except Exception as e:
            # If test request fails, log but don't fail the connection
            return EventNames.ERROR.name, f"HTTP/2 test request failed: {e}"
        finally:
            # Reset timeout to original value
            self.sock.settimeout(self.TIMEOUT)
        
        return EventNames.CLIENT_STARTED.name, f"Client successfully connected to {self.host}:{self.port} with {f'TLS with ALPN protocol {selected_protocol}' if tls_enabled == 'true' else 'non-TLS'} connection."