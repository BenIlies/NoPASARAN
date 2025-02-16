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

    def handle_client_connection(self, client_socket):
        """
        Handle a client connection by processing the incoming request and sending the appropriate response.
        """
        request = client_socket.recv(4096)
        request_str = request.decode('utf-8')
        # Extract request line and headers
        headers_end_index = request_str.find("\r\n\r\n")
        headers_part = request_str[:headers_end_index] if headers_end_index != -1 else request_str
        request_line = headers_part.split("\r\n")[0]
        method, path, _ = request_line.split(" ", 2)

        route_key = (path, method)
        route_info_list = self.routes.get(route_key)
        
        if route_info_list:
            response = ""
            for route_info in route_info_list:
                response_body = route_info.get('body', '')
                status_code = route_info.get('status', 200)
                headers = route_info.get('headers', [])

                # Construct each part of the response
                response_part = f"HTTP/1.1 {status_code} OK\r\n"
                for header_name, header_value in headers:
                    response_part += f"{header_name}: {header_value}\r\n"
                response_part += f"\r\n{response_body}\r\n\r\n"  # Double CRLF to separate responses

                # Append the response part to the full response
                response += response_part

            # Send the full combined response to the client
            client_socket.sendall(response.encode())

        else:
            response_body = 'NoPASARAN HTTP/1.1 Server'
            status_code = 404
            headers = []

            # Construct the HTTP response
            response = f"HTTP/1.1 {status_code} OK\r\n"
            for header_name, header_value in headers:
                response += f"{header_name}: {header_value}\r\n"
            response += f"\r\n{response_body}"

            # Send response to client
            client_socket.sendall(response.encode())

        client_socket.close()

        # Store the raw received request data
        self.received_request_data = request

        # Notify that a request has been received
        if self.request_received:
            with self.request_received:
                self.request_received.notify_all()



    def wait_for_request(self, port, timeout):
        """
        Wait for an HTTP request or timeout.

        Args:
            port (int): The port to run the server on.
            timeout (int): The timeout duration in seconds.

        Returns:
            Tuple[bytes, str]: The raw received request data or None if a timeout occurs, and the event name.
        """
        server_address = ('', port)
        self.request_received = threading.Condition()
        self.received_request_data = None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(server_address)
            server_socket.listen(1)
            server_socket.setblocking(False)

            # Initialize the timeout timer
            start_time = time.time()

            while True:
                # Check if the timeout has elapsed
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    return None, EventNames.TIMEOUT.name
                
                # Use select to wait for a connection with a timeout
                ready_to_read, _, _ = select.select([server_socket], [], [], timeout - elapsed_time)
                
                if ready_to_read:
                    client_socket, _ = server_socket.accept()
                    self.handle_client_connection(client_socket)
                    return self.received_request_data, EventNames.REQUEST_RECEIVED.name
