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

    def start_and_wait_for_tcp_data(self, host, port, timeout):
        """
        Combine:
          - Creating a socket
          - Binding to (host, port)
          - Listening
          - Accepting exactly one client connection
          - Echoing data once
          - Returning the data and event

        Returns:
            (bytes or None, str):
                - The echoed data as bytes
                - The event name (REQUEST_RECEIVED or TIMEOUT)
        """
        self.request_received = threading.Condition()
        self.received_data = None

        # 1) Create and bind
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(1)
            server_socket.setblocking(False)

            start_time = time.time()

            # 2) Loop until we get one connection or timeout
            while True:
                if time.time() - start_time > timeout:
                    return None, EventNames.TIMEOUT.name

                ready_to_read, _, _ = select.select([server_socket], [], [], timeout)
                if ready_to_read:
                    # 3) Accept exactly one connection
                    client_socket, _ = server_socket.accept()
                    try:
                        data = client_socket.recv(4096)
                        if data:
                            # Echo it back
                            client_socket.sendall(data)
                            self.received_data = data
                            return data, EventNames.REQUEST_RECEIVED.name
                    finally:
                        client_socket.close()

    def start_and_wait_for_udp_data (self, host, port, timeout):
        """
        UDP version:
          - Create a socket (SOCK_DGRAM)
          - Bind
          - Wait for exactly one datagram
          - Echo that datagram to the sender
          - Return (data, event)
        """
        self.request_received = threading.Condition()
        self.received_data = None

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.setblocking(False)

            start_time = time.time()
            while True:
                if time.time() - start_time > timeout:
                    return None, EventNames.TIMEOUT.name

                ready_to_read, _, _ = select.select([server_socket], [], [], timeout)
                if ready_to_read:
                    # 3) Accept exactly one connection
                    data, client_addr = server_socket.recvfrom(4096)
                    if data:
                        # Echo back
                        server_socket.sendto(data, client_addr)
                        self.received_data = data
                        return data, EventNames.REQUEST_RECEIVED.name                    

    def close(self):
        if self.client_socket:
            self.client_socket.close()
        if self.sock:
            self.sock.close()
        self.client_socket = None
        self.sock = None
        return EventNames.CONNECTION_CLOSED.name
