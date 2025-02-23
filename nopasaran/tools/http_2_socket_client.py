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
        settings = {
            SettingCodes.ENABLE_PUSH.value: 1  # Enable HTTP/2 Server Push
        }
        config_settings.update(settings)
        # Send connection preface
        self.conn.initiate_connection()
        self.sock.sendall(self.conn.data_to_send())
        
        return EventNames.CLIENT_STARTED.name, f"Client successfully connected to {self.host}:{self.port} with {'TLS' if tls_enabled == 'true' else 'non-TLS'} connection."