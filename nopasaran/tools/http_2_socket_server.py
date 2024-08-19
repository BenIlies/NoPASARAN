import socket
import threading
import h2.connection
import h2.events
import h2.config
import time
import select

from nopasaran.definitions.events import EventNames
from nopasaran.tools.http_2_overwrite import *

class HTTP2SocketServer:
    """
    A basic HTTP/2 server implementation using the h2 library and sockets.
    """

    def __init__(self):
        self.routes = {}
        self.request_received = None
        self.received_request_data = None

    def handle_connection(self, client_socket):
        """
        Handle an incoming HTTP/2 connection.

        Args:
            client_socket (socket.socket): The client socket.
        """
        conn = h2.connection.H2Connection(config=h2.config.H2Configuration(client_side=False))
        conn.initiate_connection()
        client_socket.sendall(conn.data_to_send())

        while True:
            try:
                data = client_socket.recv(65535)
                if not data:
                    break

                events = conn.receive_data(data)
                for event in events:
                    if isinstance(event, h2.events.RequestReceived):
                        self.handle_request(event, conn)
                    elif isinstance(event, h2.events.DataReceived):
                        conn.acknowledge_received_data(event.flow_controlled_length, event.stream_id)
                    elif isinstance(event, h2.events.StreamEnded):
                        self.handle_stream_ended(event, conn, client_socket)

                client_socket.sendall(conn.data_to_send())
            except Exception as e:
                print(f"Error handling connection: {e}")
                break

        client_socket.close()

    def handle_request(self, event, conn):
        """
        Handle an HTTP/2 request.

        Args:
            event (h2.events.RequestReceived): The request received event.
            conn (h2.connection.H2Connection): The HTTP/2 connection.
        """
        headers = {key.decode('utf-8'): value.decode('utf-8') for key, value in event.headers}
        method = headers[':method']
        path = headers[':path']

        route_key = (path, method)
        if route_key in self.routes:
            route = self.routes[route_key]
            # Ensure the body is encoded as bytes
            body = route['body'].encode('utf-8') if isinstance(route['body'], str) else route['body']
            
            response_headers = [
                (b':status', str(route['status']).encode('utf-8'))
                ] + [(key.encode('utf-8'), value.encode('utf-8')) for key, value in route['headers']]

            conn.send_headers(event.stream_id, response_headers)
            conn.send_data(event.stream_id, body, end_stream=True)
        else:
            response_headers = [(b':status', b'404')]
            conn.send_headers(event.stream_id, response_headers, end_stream=True)

        # Store the raw received request data
        self.received_request_data = headers

        # Notify that a request has been received
        if self.request_received:
            with self.request_received:
                self.request_received.notify_all()

    def handle_stream_ended(self, event, conn, client_socket):
        """
        Handle a stream ended event (used to close the connection if necessary).

        Args:
            event (h2.events.StreamEnded): The stream ended event.
            conn (h2.connection.H2Connection): The HTTP/2 connection.
            client_socket (socket.socket): The client socket.
        """
        client_socket.sendall(conn.data_to_send())

    def wait_for_request(self, port, timeout):
        """
        Wait for an HTTP/2 request on a specified port with a timeout.

        Args:
            port (int): The port to listen on.
            timeout (int): The timeout duration in seconds.

        Returns:
            Tuple[dict, str]: The received request data or None if a timeout occurs, and the event name.
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
                if elapsed_time > timeout:
                    return None, EventNames.TIMEOUT.name

                ready_to_read, _, _ = select.select([server_socket], [], [], timeout - elapsed_time)

                if ready_to_read:
                    client_socket, _ = server_socket.accept()
                    self.handle_connection(client_socket)
                    return self.received_request_data, EventNames.REQUEST_RECEIVED.name
