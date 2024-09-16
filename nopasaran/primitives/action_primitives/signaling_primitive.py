from nopasaran.definitions.events import EventNames
from nopasaran.decorators import parsing_decorator
import socket
import json
import logging


class SignalingPrimitives:
    """
    Class containing signaling event primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=4, output_args=0)
    def signal_ready_connection(inputs, outputs, state_machine):
        """
        Send a 'signal_ready_connection' event to the signaling server. 
        If there's a timeout, trigger the 'TIMEOUT' event.

        Args:
            inputs (List[str]): A list containing the signaling server address, port, client ID, and timeout duration.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        client_id = state_machine.get_variable_value(inputs[2])
        timeout = int(state_machine.get_variable_value(inputs[3]))
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(float(timeout))  # Apply the timeout
                sock.connect((server, int(port)))
                message = {
                    'type': 'signal_ready_connection',
                    'id': client_id
                }
                sock.send(json.dumps(message).encode())
                response = sock.recv(1024).decode()

                logging.info(f"[Signaling] Received: {response}")
                state_machine.trigger_event(EventNames.SIGNAL_READY_CONNECTION.name)

        except (socket.timeout, socket.error) as e:
            logging.warning(f"[Signaling] Timeout or error: {e}")
            state_machine.trigger_event(EventNames.TIMEOUT.name)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=0)
    def signal_ready_listen(inputs, outputs, state_machine):
        """
        Send a 'signal_ready_listen' event to the signaling server.
        If there's a timeout, trigger the 'TIMEOUT' event.

        Args:
            inputs (List[str]): A list containing the signaling server address, port, client ID, and timeout duration.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        client_id = state_machine.get_variable_value(inputs[2])
        timeout = int(state_machine.get_variable_value(inputs[3]))
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(float(timeout))
                sock.connect((server, int(port)))
                message = {
                    'type': 'signal_ready_listen',
                    'id': client_id
                }
                sock.send(json.dumps(message).encode())
                response = sock.recv(1024).decode()

                logging.info(f"[Signaling] Received: {response}")
                state_machine.trigger_event(EventNames.SIGNAL_READY_LISTEN.name)

        except (socket.timeout, socket.error) as e:
            logging.warning(f"[Signaling] Timeout or error: {e}")
            state_machine.trigger_event(EventNames.TIMEOUT.name)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=0)
    def signal_listening(inputs, outputs, state_machine):
        """
        Send a 'signal_listening' event to the signaling server.
        If there's a timeout, trigger the 'TIMEOUT' event.

        Args:
            inputs (List[str]): A list containing the signaling server address, port, client ID, and timeout duration.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        client_id = state_machine.get_variable_value(inputs[2])
        timeout = int(state_machine.get_variable_value(inputs[3]))
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(float(timeout))
                sock.connect((server, int(port)))
                message = {
                    'type': 'signal_listening',
                    'id': client_id
                }
                sock.send(json.dumps(message).encode())
                response = sock.recv(1024).decode()

                logging.info(f"[Signaling] Received: {response}")
                state_machine.trigger_event(EventNames.SIGNAL_LISTENING.name)

        except (socket.timeout, socket.error) as e:
            logging.warning(f"[Signaling] Timeout or error: {e}")
            state_machine.trigger_event(EventNames.TIMEOUT.name)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=0)
    def signal_ready_stop(inputs, outputs, state_machine):
        """
        Send a 'signal_ready_stop' event to the signaling server.
        If there's a timeout, trigger the 'TIMEOUT' event.

        Args:
            inputs (List[str]): A list containing the signaling server address, port, client ID, and timeout duration.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        client_id = state_machine.get_variable_value(inputs[2])
        timeout = int(state_machine.get_variable_value(inputs[3]))
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(float(timeout))
                sock.connect((server, int(port)))
                message = {
                    'type': 'signal_ready_stop',
                    'id': client_id
                }
                sock.send(json.dumps(message).encode())
                response = sock.recv(1024).decode()

                logging.info(f"[Signaling] Received: {response}")
                state_machine.trigger_event(EventNames.SIGNAL_READY_STOP.name)

        except (socket.timeout, socket.error) as e:
            logging.warning(f"[Signaling] Timeout or error: {e}")
            state_machine.trigger_event(EventNames.TIMEOUT.name)
