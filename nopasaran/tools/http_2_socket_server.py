import h2.connection
import h2.config
from h2.settings import SettingCodes
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
        self.conn = None  # HTTP/2 connection object

    def start(self, tls_enabled=False, protocol='h2', connection_settings_server = {}, client_frames = []):
        """Start the HTTP/2 server"""

        # Create a listening socket
        self.sock = create_socket(self.host, self.port, is_server=True)
        self.sock.listen(5)
        self.sock.settimeout(self.TIMEOUT)

        try:
            self.client_socket, address = self.sock.accept()
        except TimeoutError:
            return EventNames.TIMEOUT.name, (
                f"Timeout occurred after {self.TIMEOUT}s while waiting for a client connection at {self.host}:{self.port}."
            )

        # Upgrade to TLS if enabled
        if tls_enabled == 'true':
            ssl_context = create_ssl_context(protocol=protocol, is_client=False)
            self.client_socket = ssl_context.wrap_socket(self.client_socket, server_side=True)

        # Merge connection settings
        settings = {
            SettingCodes.ENABLE_PUSH.value: 1  # Enable HTTP/2 Server Push
        }
        config_settings = H2_CONFIG_SETTINGS.copy()
        config_settings.update(connection_settings_server)

        # Create HTTP/2 connection object
        config = h2.config.H2Configuration(client_side=False)  # Avoid passing **kwargs
        self.conn = h2.connection.H2Connection(config=config)

        # Step 1: Initiate HTTP/2 Connection
        self.conn.initiate_connection()

        # Step 3: Serialize and send the connection preface along with settings
        self.client_socket.sendall(self.conn.data_to_send())

        return EventNames.SERVER_STARTED.name, (
            f"Server successfully started at {self.host}:{self.port} "
            f"with {'TLS' if tls_enabled == 'true' else 'non-TLS'} connection."
        )
