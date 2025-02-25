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
import ssl

class HTTP2SocketServer(HTTP2SocketBase):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.client_socket = None

    def start(self, tls_enabled = False, protocol = 'h2', connection_settings_server = {}, cloudflare_origin = False):
        """Start the HTTP/2 server"""
        self.sock = create_socket(self.host, self.port, is_server=True)
        self.sock.listen(5)
        
        self.sock.settimeout(self.TIMEOUT)
        
        try:
            self.client_socket, address = self.sock.accept()
        except TimeoutError:
            return EventNames.TIMEOUT.name, f"Timeout occurred after {self.TIMEOUT}s while waiting for client connection at {self.host}:{self.port}. No client connection was established."

        if tls_enabled == 'true':
            ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            
            # Force TLS 1.2 only (like OpenSSL's -tls1_2 flag)
            ssl_context.options |= (
                ssl.OP_NO_SSLv2 | 
                ssl.OP_NO_SSLv3 | 
                ssl.OP_NO_TLSv1 | 
                ssl.OP_NO_TLSv1_1 |
                ssl.OP_NO_TLSv1_3  # Exclude TLS 1.3
            )
            
            # Set ALPN to only advertise h2
            ssl_context.set_alpn_protocols(['h2'])
            
            # Load certificate and key from specific paths (like -cert and -key flags)
            if cloudflare_origin == 'true':
                cert_path = "certs/cloudflare/server.crt"
                key_path = "certs/cloudflare/server.key"
            else:
                cert_path = "/certs/server.crt"
                key_path = "/certs/server.key"
            
            ssl_context.load_cert_chain(cert_path, key_path)
            
            try:
                self.client_socket = ssl_context.wrap_socket(
                    self.client_socket,
                    server_side=True
                )
            except Exception as e:
                return EventNames.ERROR.name, f"TLS handshake failed: {str(e)}"
            
            # Verify ALPN negotiation
            selected_protocol = self.client_socket.selected_alpn_protocol()
            if selected_protocol != 'h2':
                return EventNames.ERROR.name, f"Client negotiated {selected_protocol or 'no protocol'} instead of HTTP/2"
        
        config_settings = H2_CONFIG_SETTINGS.copy()
        config_settings.update(connection_settings_server)
        config = h2.config.H2Configuration(client_side=False, **config_settings)
        self.conn = h2.connection.H2Connection(config=config)
        
        # Send connection preface
        self.conn.initiate_connection()
        self.client_socket.sendall(self.conn.data_to_send())

        selected_protocol = self.client_socket.selected_alpn_protocol() if tls_enabled == 'true' else None

        return EventNames.SERVER_STARTED.name, f"Server successfully started at {self.host}:{self.port} with a {f'TLS with ALPN protocol {selected_protocol}' if tls_enabled == 'true' else 'non-TLS'} connection from {address}."