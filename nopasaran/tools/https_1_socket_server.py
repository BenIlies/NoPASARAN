import socket
import ssl
import tempfile
import time
import select
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from nopasaran.definitions.events import EventNames
import os

class HTTPS1SocketServer:
    """
    HTTPS/1.1 server with self-signed TLS and route-based request handling.
    """

    def __init__(self):
        self.routes = {}
        self.request_received = None
        self.received_request_data = None
        self.sock = None
        self.client_socket = None
        self.TIMEOUT = 5.0
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self._cert_path = None
        self._key_path = None

    def generate_and_load_cert(self, identifier):
        cert_path, key_path = self.generate_self_signed_cert(identifier)

        if not cert_path or not os.path.exists(cert_path):
            raise FileNotFoundError(f"[HTTPS1SocketServer] Certificate file not found at {cert_path}")
        if not key_path or not os.path.exists(key_path):
            raise FileNotFoundError(f"[HTTPS1SocketServer] Key file not found at {key_path}")
        if os.path.getsize(cert_path) == 0:
            raise ValueError(f"[HTTPS1SocketServer] Certificate file is empty at {cert_path}")
        if os.path.getsize(key_path) == 0:
            raise ValueError(f"[HTTPS1SocketServer] Key file is empty at {key_path}")

        try:
            self.context.load_cert_chain(cert_path, key_path)
        except Exception as e:
            raise RuntimeError(f"[HTTPS1SocketServer] Failed to load cert chain: {e}")

        self._cert_path = cert_path
        self._key_path = key_path

    def generate_self_signed_cert(self, identifier):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, identifier),
        ])

        alt_names = [x509.DNSName(identifier)]
        try:
            import ipaddress
            alt_names.append(x509.IPAddress(ipaddress.ip_address(identifier)))
        except ValueError:
            pass

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.utcnow())
            .not_valid_after(datetime.utcnow() + timedelta(days=1))
            .add_extension(
                x509.SubjectAlternativeName(alt_names),
                critical=False,
            )
            .sign(key, hashes.SHA256())
        )

        cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
        key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")

        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
        key_file.write(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption()
            )
        )
        cert_file.close()
        key_file.close()
        return cert_file.name, key_file.name

    def start(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)
        return EventNames.SERVER_STARTED.name, f"HTTPS server started at {host}:{port}"

    def handle_client_connection(self, tls_socket):
        try:
            request = tls_socket.recv(4096)
            if not request:
                return  # Client closed connection or sent nothing
        except socket.timeout:
            return  # Timed out waiting for client data

        request_str = request.decode("utf-8", errors="ignore")
        self.received_request_data = request

        headers_end_index = request_str.find("\r\n\r\n")
        headers_part = request_str[:headers_end_index] if headers_end_index != -1 else request_str
        request_line = headers_part.split("\r\n")[0]
        try:
            method, path, _ = request_line.split(" ", 2)
        except ValueError:
            method, path = "GET", "/"  # fallback

        route_key = (path, method.upper())
        route_info_list = self.routes.get(route_key)

        if route_info_list:
            response = ""
            for route_info in route_info_list:
                body = route_info.get("body", "")
                status = route_info.get("status", 200)
                headers = route_info.get("headers", [])

                response += f"HTTP/1.1 {status} OK\r\n"
                for header_name, header_value in headers:
                    response += f"{header_name}: {header_value}\r\n"
                response += f"\r\n{body}\r\n\r\n"

            tls_socket.sendall(response.encode())
        else:
            body = "NoPASARAN HTTPS/1.1 Server"
            response = f"HTTP/1.1 404 Not Found\r\nContent-Length: {len(body)}\r\n\r\n{body}"
            tls_socket.sendall(response.encode())

        tls_socket.close()

        if self.request_received:
            with self.request_received:
                self.request_received.notify_all()

    def wait_for_request(self, port, timeout):
        """
        Wait for a single HTTPS request with TLS handshake and user-defined timeout.
        """
        self.received_request_data = None
        self.request_received = None
        context = self.context
        start_time = time.time()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('', port))
            server_socket.listen(1)
            server_socket.setblocking(False)

            while True:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    return None, EventNames.TIMEOUT.name

                try:
                    remaining = timeout - elapsed
                    ready, _, _ = select.select([server_socket], [], [], remaining)
                    if ready:
                        client_sock, _ = server_socket.accept()
                        client_sock.settimeout(2.0)  # Important: Timeout for TLS handshake and recv
                        try:
                            with context.wrap_socket(client_sock, server_side=True) as tls_sock:
                                tls_sock.settimeout(2.0)  # Also set after TLS handshake
                                self.handle_client_connection(tls_sock)
                                if self.received_request_data:
                                    return self.received_request_data, EventNames.REQUEST_RECEIVED.name
                                else:
                                    return None, EventNames.TIMEOUT.name
                        except (ssl.SSLError, socket.timeout):
                            return None, EventNames.TIMEOUT.name
                        except Exception:
                            return None, EventNames.ERROR.name
                except Exception:
                    return None, EventNames.ERROR.name

    def close(self):
        try:
            if self.client_socket:
                self.client_socket.close()
            if self.sock:
                self.sock.close()

            self.client_socket = None
            self.sock = None

            try:
                if self._cert_path and os.path.exists(self._cert_path):
                    os.remove(self._cert_path)
                if self._key_path and os.path.exists(self._key_path):
                    os.remove(self._key_path)
            except Exception as e:
                return EventNames.ERROR.name, f"Certificate cleanup error: {str(e)}"

            return EventNames.CONNECTION_ENDING.name
        except Exception:
            return EventNames.CONNECTION_ENDING.name
