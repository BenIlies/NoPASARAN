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

    def start(self, host, port):
        """
        Start the HTTP/1.1 server to receive HTTP/1.1 requests.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)
        
        return EventNames.SERVER_STARTED.name, f"Server successfully started at {host}:{port}."

    def receive_test_frames(self):
        """
        Listen for HTTP/1.1 requests until a timeout occurs, then process all received requests.
        
        Returns:
            Tuple[str, str, str]: (event_name, message, received_data)
                - event_name: The type of event that occurred (from EventNames)
                    - TIMEOUT: Timeout occurred before all requests were received
                    - REJECTED: Received a 4xx or 5xx status code
                    - RECEIVED_REQUESTS: All requests have been received
                    - ERROR: Error occurred while receiving requests
                - message: A descriptive message about what happened
                - received_data: String representation of the received requests or None
        """
        if not self.sock:
            return EventNames.ERROR.name, "Server not started", None
        
        requests_received = []
        start_time = time.time()
        
        # Make the server socket non-blocking for accepting connections
        self.sock.setblocking(False)
        
        # Keep accepting connections until we hit a timeout
        while True:
            # Check for overall timeout
            elapsed_time = time.time() - start_time
            if elapsed_time > self.TIMEOUT:
                if len(requests_received) == 0:
                    return EventNames.TIMEOUT.name, f"Timeout after {self.TIMEOUT}s and received no requests.", None
                else:
                    break  # We've received some requests, so consider it done
            
            try:
                # Try to accept a new connection
                ready_to_read, _, _ = select.select([self.sock], [], [], 0.5)
                
                if ready_to_read:
                    client_socket, _ = self.sock.accept()
                    client_socket.settimeout(0.5)
                    
                    try:
                        data = client_socket.recv(4096)
                        
                        if data:
                            # Parse the HTTP/1.1 request
                            request_str = data.decode('utf-8', errors='ignore')
                            requests_received.append(request_str)
                            
                            # Check for error status codes
                            if "HTTP/1.1 5" in request_str or "HTTP/1.1 4" in request_str:
                                try:
                                    status_line = request_str.split("\r\n")[0]
                                    status_code = status_line.split(" ")[1]
                                    client_socket.close()
                                    return EventNames.REJECTED.name, f"Received {status_code} status code.", request_str
                                except (IndexError, ValueError):
                                    client_socket.close()
                                    return EventNames.REJECTED.name, "Received 4xx or 5xx status code.", request_str
                    finally:
                        client_socket.close()
            except socket.timeout:
                continue
            except Exception as e:
                return EventNames.ERROR.name, f"Error while receiving requests: {str(e)}", \
                       str(requests_received) if requests_received else None
        
        # If we get here, we've either collected all requests or hit the timeout
        if len(requests_received) == 0:
            return EventNames.TIMEOUT.name, "No requests received before timeout.", None
        
        return EventNames.RECEIVED_REQUESTS.name, f"Received {len(requests_received)} HTTP/1.1 requests.", str(requests_received)

    def close(self):
        """Close the HTTP/1.1 connection and clean up resources"""
        try:
            if self.client_socket:
                self.client_socket.close()
            if self.sock:
                self.sock.close()
            
            # Clear references
            self.client_socket = None
            self.sock = None
            
            return EventNames.CONNECTION_CLOSED.name
        except Exception as e:
            return EventNames.CONNECTION_CLOSED.name
