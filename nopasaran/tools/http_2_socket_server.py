import h2.connection
import h2.config
import nopasaran.tools.http_2_overwrite
from nopasaran.definitions.events import EventNames
from nopasaran.http_2_utils import (
    create_ssl_context,
    create_socket,
    H2_CONFIG_SETTINGS,
)
from nopasaran.tools.http_2_socket_base import HTTP2SocketBase

class HTTP2SocketServer(HTTP2SocketBase):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.client_socket = None

    def start(self, tls_enabled = False, protocol = 'h2', connection_settings_server = {}, client_frames = []):
        """Start the HTTP/2 server"""
        self.sock = create_socket(self.host, self.port, is_server=True)
        self.sock.listen(5)
        
        self.sock.settimeout(self.TIMEOUT)
        
        try:
            self.client_socket, address = self.sock.accept()
        except TimeoutError:
            if client_frames:
                return EventNames.TIMEOUT.name, "Timeout occurred while waiting for client connection. Proxy dropped client's frames."
            else:
                return EventNames.TIMEOUT.name, "Timeout occurred while waiting for client connection"
        
        if tls_enabled == 'true':
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
        
        return EventNames.SERVER_STARTED.name, "Server started"