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
        cert_path, key_path = self._generate_self_signed_cert()
        self.context.load_cert_chain(cert_path, key_path)

    def _generate_self_signed_cert(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"SA"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"NoPASARAN"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
        ])
        cert = x509.CertificateBuilder().subject_name(subject)\
            .issuer_name(issuer)\
            .public_key(key.public_key())\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.utcnow())\
            .not_valid_after(datetime.utcnow() + timedelta(days=1))\
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False)\
            .sign(key, hashes.SHA256())

        cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
        key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")

        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
        key_file.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
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
        request = tls_socket.recv(4096)
        request_str = request.decode("utf-8", errors="ignore")
        self.received_request_data = request

        # Parse request line
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

    def receive_test_frames(self):
        if not self.sock:
            return EventNames.ERROR.name, "Server not started", None

        requests_received = []
        start_time = time.time()
        self.sock.setblocking(False)

        while True:
            if time.time() - start_time > self.TIMEOUT:
                if not requests_received:
                    return EventNames.TIMEOUT.name, "Timeout with no request", None
                break

            try:
                ready_to_read, _, _ = select.select([self.sock], [], [], 0.5)
                if ready_to_read:
                    client_sock, _ = self.sock.accept()
                    tls_sock = self.context.wrap_socket(client_sock, server_side=True)
                    tls_sock.settimeout(1.0)
                    try:
                        self.handle_client_connection(tls_sock)
                        req_str = self.received_request_data.decode("utf-8", errors="ignore")
                        requests_received.append(req_str)
                    except Exception as e:
                        return EventNames.ERROR.name, f"TLS error: {e}", None
            except Exception as e:
                return EventNames.ERROR.name, str(e), None

        return EventNames.RECEIVED_REQUESTS.name, f"Received {len(requests_received)} HTTPS requests.", str(requests_received)

    def close(self):
        if self.client_socket:
            self.client_socket.close()
        if self.sock:
            self.sock.close()
        self.client_socket = None
        self.sock = None
        return EventNames.CONNECTION_CLOSED.name
