import h2.connection
import h2.config
import nopasaran.tools.http_2_overwrite
from h2.settings import SettingCodes
from h2.events import ResponseReceived, DataReceived
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
    def start(self, tls_enabled = False, connection_settings_client = {}, cloudflare_origin = False):
        """Start the HTTP/2 client"""
        self.cloudflare_origin = True if cloudflare_origin == 'true' else False

        self.sock = create_socket(self.host, self.port)
        self.sock.settimeout(self.TIMEOUT)  # Set socket timeout
        
        try:
            # First attempt the connection
            self.sock.connect((self.host, self.port))
            
            if tls_enabled == 'true':
                ssl_context = create_ssl_context(
                    is_client=True
                )
                
                self.sock = ssl_context.wrap_socket(
                    self.sock,
                    server_hostname=self.host
                )
            
        except TimeoutError as e:
            return EventNames.ERROR.name, f"Timeout occurred after {self.TIMEOUT}s while trying to connect to server at {self.host}:{self.port}: {e}"
        except ConnectionRefusedError as e:
            return EventNames.ERROR.name, f"Connection refused by server at {self.host}:{self.port}. Server may not be running or port may be blocked: {e}"
        
        config_settings = H2_CONFIG_SETTINGS.copy()
        config_settings.update(connection_settings_client)
        config = h2.config.H2Configuration(client_side=True, **config_settings)
        self.conn = h2.connection.H2Connection(config=config)
        
        # Add these attributes to the connection object
        self.conn.host = self.host
        self.conn.scheme = 'https' if tls_enabled == 'true' else 'http'
        
        # Send connection preface
        self.conn.initiate_connection()
        self.sock.sendall(self.conn.data_to_send())

        selected_protocol = self.sock.selected_alpn_protocol() if tls_enabled == 'true' else None
        
        # Wait for server settings first
        try:
            self.sock.settimeout(self.TIMEOUT)  # Short timeout for settings
            data = self.sock.recv(65535)
            if data:
                self.conn.receive_data(data)
                # Send acknowledgement if needed
                data_to_send = self.conn.data_to_send()
                if data_to_send:
                    self.sock.sendall(data_to_send)
        except socket.timeout:
            return EventNames.REJECTED.name, f"No initial settings received from peer at {self.host}:{self.port}"
        except Exception as e:
            return EventNames.ERROR.name, f"Error receiving initial settings from peer at {self.host}:{self.port}: {str(e)}"
        
        # Send a test HTTP/2 request and wait for response only if cloudflare_origin is true
        if self.cloudflare_origin:
            try:
                # Create a new stream for our test message
                stream_id = 1
                
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
                self.sock.settimeout(self.TIMEOUT)  # Timeout for test response
                response_received = False
                
                # Try up to 3 times to get a response
                for _ in range(self.MAX_RETRY_ATTEMPTS):
                    try:
                        data = self.sock.recv(65535)
                        if data:
                            events = self.conn.receive_data(data)
                            # Process events and check for response
                            for event in events:
                                if (hasattr(event, 'stream_id') and 
                                    event.stream_id == stream_id and
                                    (isinstance(event, ResponseReceived) or 
                                     isinstance(event, DataReceived))):
                                    response_received = True
                                    break
                            
                            # Send any necessary data to acknowledge
                            data_to_send = self.conn.data_to_send()
                            if data_to_send:
                                self.sock.sendall(data_to_send)
                            
                            if response_received:
                                break
                    except socket.timeout:
                        continue
                
                if not response_received:
                    return EventNames.TIMEOUT.name, f"No response received for test request from {self.host}:{self.port}"
                
            except Exception as e:
                return EventNames.ERROR.name, f"Error during HTTP/2 test request/response with {self.host}:{self.port}: {str(e)}"
            finally:
                # Reset timeout to original value
                self.sock.settimeout(self.TIMEOUT)
        
        return EventNames.CLIENT_STARTED.name, f"Client successfully connected to {self.host}:{self.port} with {f'TLS with ALPN protocol {selected_protocol}' if tls_enabled == 'true' else 'non-TLS'} connection."