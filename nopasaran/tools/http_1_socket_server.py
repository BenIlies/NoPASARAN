import socket
import select
import threading
import time
from nopasaran.definitions.events import EventNames

class HTTP1SocketServer:
    """
    A simple HTTP/1.1 server using sockets.
    """

    def __init__(self):
        self.routes = {}
        self.request_received = None
        self.received_request_data = None
        self.sock = None
        self.client_socket = None
        self.TIMEOUT = 5.0

    def handle_client_connection(self, client_socket, timeout):
        """
        Handle a client connection by processing the incoming request and sending the appropriate response.
        """
        client_socket.setblocking(False)
        ready_to_read, _, _ = select.select([client_socket], [], [], timeout)
        
        if not ready_to_read:
            client_socket.close()
            return None, EventNames.TIMEOUT.name

        try:
            request = client_socket.recv(4096)
        except socket.timeout:
            client_socket.close()
            return None, EventNames.TIMEOUT.name
        except ConnectionResetError as e:
            client_socket.close()
            return str(e), EventNames.ERROR.name

        if not request:
            client_socket.close()
            return None, EventNames.TIMEOUT.name

        request_str = request.decode('utf-8', errors='ignore')

        # Extract request line and headers
        headers_end_index = request_str.find("\r\n\r\n")
        headers_part = request_str[:headers_end_index] if headers_end_index != -1 else request_str
        request_line = headers_part.split("\r\n")[0]

        try:
            method, path, _ = request_line.split(" ", 2)
        except ValueError:
            method, path = "GET", "/"

        route_key = (path, method)
        route_info_list = self.routes.get(route_key)

        if route_info_list:
            response = ""
            for route_info in route_info_list:
                response_body = route_info.get('body', '')
                status_code = route_info.get('status', 200)
                headers = route_info.get('headers', [])

                response_part = f"HTTP/1.1 {status_code} OK\r\n"
                for header_name, header_value in headers:
                    response_part += f"{header_name}: {header_value}\r\n"
                response_part += f"\r\n{response_body}\r\n\r\n"

                response += response_part

            client_socket.sendall(response.encode())
        else:
            response_body = 'NoPASARAN HTTP/1.1 Server'
            status_code = 404
            response = f"HTTP/1.1 {status_code} Not Found\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
            client_socket.sendall(response.encode())

        client_socket.close()

        self.received_request_data = request

        if self.request_received:
            with self.request_received:
                self.request_received.notify_all()

        return request, EventNames.REQUEST_RECEIVED.name

    def wait_for_request(self, port, timeout):
        """
        Wait for an HTTP request or timeout.

        Args:
            port (int): The port to run the server on.
            timeout (int): The timeout duration in seconds.

        Returns:
            Tuple[bytes or None, str]: The raw received request data or None if a timeout occurs, and the event name.
        """
        server_address = ('', port)
        self.request_received = threading.Condition()
        self.received_request_data = None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(server_address)
            server_socket.listen(1)
            server_socket.setblocking(False)

            start_time = time.time()

            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    return None, EventNames.TIMEOUT.name

                ready_to_read, _, _ = select.select([server_socket], [], [], timeout - elapsed_time)

                if ready_to_read:
                    client_socket, _ = server_socket.accept()
                    return self.handle_client_connection(client_socket, timeout - elapsed_time)

    def start(self, host, port):
        """
        Start the HTTP/1.1 server to receive HTTP/1.1 requests.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)

        return EventNames.SERVER_STARTED.name, f"Server successfully started at {host}:{port}."

    def close(self):
        """Close the HTTP/1.1 connection and clean up resources"""
        try:
            if self.client_socket:
                self.client_socket.close()
            if self.sock:
                self.sock.close()

            self.client_socket = None
            self.sock = None

            return EventNames.CONNECTION_ENDING.name
        except Exception as e:
            return EventNames.CONNECTION_ENDING.name
