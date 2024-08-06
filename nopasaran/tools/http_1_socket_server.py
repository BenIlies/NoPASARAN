import socket
import threading
from nopasaran.definitions.events import EventNames

class HTTP1SocketServer:
    """
    A simple HTTP/1.1 server using sockets.
    """

    routes = {}
    request_received = None
    received_request_data = None

    @staticmethod
    def handle_client_connection(client_socket):
        """
        Handle a client connection by processing the incoming request and sending the appropriate response.
        """
        request = client_socket.recv(4096).decode('utf-8')
        
        # Extract request line and headers
        headers_end_index = request.find("\r\n\r\n")
        headers_part = request[:headers_end_index] if headers_end_index != -1 else request
        request_line = headers_part.split("\r\n")[0]
        method, path, _ = request_line.split(" ", 2)

        route_key = (path, method)
        route_info = HTTP1SocketServer.routes.get(route_key)
        
        if route_info:
            response_body = route_info.get('body', '')
            status_code = route_info.get('status', 200)
            headers = route_info.get('headers', {})
        else:
            response_body = 'NoPASARAN HTTP/1.1 Server'
            status_code = 404
            headers = {}

        # Construct the HTTP response
        response = f"HTTP/1.1 {status_code} OK\r\n"
        for header_name, header_value in headers.items():
            response += f"{header_name}: {header_value}\r\n"
        response += f"\r\n{response_body}"
        
        # Send response to client
        client_socket.sendall(response.encode())
        client_socket.close()

        # Store the received request data
        HTTP1SocketServer.received_request_data = {
            'path': path,
            'method': method,
            'headers': headers_part,
            'body': "hello"  # Placeholder for body content
        }

        # Notify that a request has been received
        if HTTP1SocketServer.request_received:
            with HTTP1SocketServer.request_received:
                HTTP1SocketServer.request_received.notify_all()

    @staticmethod
    def wait_for_request(port, timeout):
        """
        Wait for an HTTP request or timeout.

        Args:
            port (int): The port to run the server on.
            timeout (int): The timeout duration in seconds.

        Returns:
            Tuple[dict, str]: The received request data or None if a timeout occurs, and the event name.
        """
        server_address = ('', port)
        HTTP1SocketServer.request_received = threading.Condition()
        HTTP1SocketServer.received_request_data = None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(server_address)
            server_socket.listen(1)

            def shutdown():
                server_socket.close()

            # Function to handle incoming connections
            def serve_forever():
                while HTTP1SocketServer.received_request_data is None:
                    client_socket, _ = server_socket.accept()
                    HTTP1SocketServer.handle_client_connection(client_socket)

            server_thread = threading.Thread(target=serve_forever)
            server_thread.start()

            # Start timer for timeout
            timer = threading.Timer(timeout, shutdown)
            timer.start()

            with HTTP1SocketServer.request_received:
                HTTP1SocketServer.request_received.wait()

            # Ensure the server is shut down after the wait
            timer.cancel()  # Cancel the timer if request is received
            server_socket.close()
            server_thread.join()

            if not HTTP1SocketServer.received_request_data:
                return None, EventNames.TIMEOUT.name
            return HTTP1SocketServer.received_request_data, EventNames.REQUEST_RECEIVED.name
