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
        
        # Send a minimal HTTP/2 ping to ensure connection establishment
        # This helps prevent server timeout without interfering with your state machine
        try:
            # Send a PING frame (lightweight, doesn't create a stream)
            ping_data = b'\x00\x00\x00\x00\x00\x00\x00\x00'  # 8 bytes of data
            self.conn.ping(ping_data)
            self.sock.sendall(self.conn.data_to_send())
            
            # Wait for ping acknowledgement
            self.sock.settimeout(2.0)  # Short timeout for ping response
            try:
                response_data = self.sock.recv(1024)
                if response_data:
                    self.conn.receive_data(response_data)
                    # We received some data, which is good enough to know the connection is alive
            except socket.timeout:
                # No response is concerning but we'll continue anyway
                pass
            finally:
                # Reset timeout to original value
                self.sock.settimeout(self.TIMEOUT)
        except Exception as e:
            # If ping fails, log but don't fail the connection
            return EventNames.ERROR.name, f"HTTP/2 ping failed: {e}"
        
        return EventNames.CLIENT_STARTED.name, f"Client successfully connected to {self.host}:{self.port} with {f'TLS with ALPN protocol {selected_protocol}' if tls_enabled == 'true' else 'non-TLS'} connection."