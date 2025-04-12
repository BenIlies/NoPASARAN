from nopasaran.decorators import parsing_decorator
from nopasaran.definitions.events import EventNames
import socket
import time

class TCPClientEchoPrimitives:
    """
    Class containing TCP Echo client action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_tcp_client(inputs, outputs, state_machine):
        """
        Create a TCP client socket.

        Number of input arguments: 0
        Number of output arguments: 1 (the created TCP client socket)
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        state_machine.set_variable_value(outputs[0], client_socket)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def connect_tcp_client(inputs, outputs, state_machine):
        """
        Connect the TCP client to a remote echo server.
        """
        client_socket = state_machine.get_variable_value(inputs[0])
        server_ip = state_machine.get_variable_value(inputs[1])
        server_port = int(state_machine.get_variable_value(inputs[2]))

        try:
            client_socket.connect((server_ip, server_port))
            event = EventNames.CONNECTION_ESTABLISHED.name
        except Exception:
            event = EventNames.CONNECTION_FAILED.name

        state_machine.set_variable_value(outputs[0], event)
        state_machine.trigger_event(event)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=2)
    def send_echo_request(inputs, outputs, state_machine):
        """
        Send a message to the echo server.
        """
        client_socket = state_machine.get_variable_value(inputs[0])
        payload = state_machine.get_variable_value(inputs[1])

        try:
            bytes_sent = client_socket.send(payload.encode())
            event = EventNames.PACKET_SENT.name
        except Exception:
            bytes_sent = 0
            event = EventNames.ERROR.name

        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], bytes_sent)
        state_machine.trigger_event(event)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=2)
    def receive_echo_response(inputs, outputs, state_machine):
        """
        Receive a response (echo) from the echo server.
        """
        client_socket = state_machine.get_variable_value(inputs[0])
        timeout = float(state_machine.get_variable_value(inputs[1]))
        client_socket.settimeout(timeout)

        try:
            data = client_socket.recv(4096).decode(errors='ignore')
            event = EventNames.PACKET_RECEIVED.name
        except socket.timeout:
            data = None
            event = EventNames.TIMEOUT.name
        except Exception:
            data = None
            event = EventNames.ERROR.name

        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], data)
        state_machine.trigger_event(event)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_tcp_client(inputs, outputs, state_machine):
        """
        Close the TCP client socket.
        """
        client_socket = state_machine.get_variable_value(inputs[0])
        try:
            client_socket.close()
            event = EventNames.CONNECTION_CLOSED.name
        except Exception:
            event = EventNames.ERROR.name

        state_machine.set_variable_value(outputs[0], event)
        state_machine.trigger_event(event)
