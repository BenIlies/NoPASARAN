import socket
import select
import threading
import time
from nopasaran.definitions.events import EventNames

class EchoSocketServer:
    """
    A simple echo server using sockets that echoes back any data it receives.
    """

    def __init__(self):
        self.sock = None
        self.client_socket = None
        self.TIMEOUT = 5.0
        self.request_received = None
        self.received_data = None

    def handle_client_connection(self, client_socket):
        """
        Handle a client connection by echoing back whatever data is received.
        """
        try:
            data = client_socket.recv(4096)
            if data:
                client_socket.sendall(data)  # Echo back the same data
                self.received_data = data

                if self.request_received:
                    with self.request_received:
                        self.request_received.notify_all()
        finally:
            client_socket.close()

    def wait_for_data(self, port, timeout):
        """
        Wait for any TCP data (echoable content), or timeout.

        Args:
            port (int): Port to listen on.
            timeout (int): Timeout in seconds.

        Returns:
            Tuple[bytes, str]: Echoed data or None, and the event name.
        """
        server_address = ('', port)
        self.request_received = threading.Condition()
        self.received_data = None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(server_address)
            server_socket.listen(1)
            server_socket.setblocking(False)

            start_time = time.time()

            while True:
                if time.time() - start_time > timeout:
                    return None, EventNames.TIMEOUT.name

                ready_to_read, _, _ = select.select([server_socket], [], [], timeout)
                if ready_to_read:
                    client_socket, _ = server_socket.accept()
                    self.handle_client_connection(client_socket)
                    return self.received_data, EventNames.REQUEST_RECEIVED.name

    def start(self, host, port):
        """
        Start the echo server.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)
        return EventNames.SERVER_STARTED.name, f"Echo server started at {host}:{port}."

    def receive_echo_data(self):
        """
        Keep listening for incoming connections and echo back any received data.
        """
        if not self.sock:
            return EventNames.ERROR.name, "Echo server not started.", None

        responses = []
        start_time = time.time()
        self.sock.setblocking(False)

        while True:
            if time.time() - start_time > self.TIMEOUT:
                return EventNames.TIMEOUT.name, f"Timeout after {self.TIMEOUT}s with no data.", None

            try:
                ready_to_read, _, _ = select.select([self.sock], [], [], 0.5)
                if ready_to_read:
                    client_socket, _ = self.sock.accept()
                    client_socket.settimeout(1.0)
                    try:
                        data = client_socket.recv(4096)
                        if data:
                            client_socket.sendall(data)
                            responses.append(data.decode(errors='ignore'))
                    finally:
                        client_socket.close()
            except socket.timeout:
                continue
            except Exception as e:
                return EventNames.ERROR.name, f"Echo error: {str(e)}", str(responses)

        return EventNames.RECEIVED_REQUESTS.name, f"Received and echoed {len(responses)} messages.", str(responses)

    def close(self):
        """
        Close the echo server socket and cleanup.
        """
        try:
            if self.client_socket:
                self.client_socket.close()
            if self.sock:
                self.sock.close()
            self.client_socket = None
            self.sock = None
            return EventNames.CONNECTION_CLOSED.name
        except Exception:
            return EventNames.CONNECTION_CLOSED.name
