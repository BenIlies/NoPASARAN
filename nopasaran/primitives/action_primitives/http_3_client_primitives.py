import asyncio
from nopasaran.decorators import parsing_decorator
from nopasaran.tools.http_3_socket_client import HTTP3SocketClient

class HTTP3ClientPrimitives:
    """
    Class containing HTTP/3 client action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def create_http_3_client(inputs, outputs, state_machine):
        """
        Create an instance of HTTP3SocketClient. 
        Number of input arguments: 2
            - The host
            - The port

        Number of output arguments: 1
            - The created HTTP3SocketServer instance

        Args:
            inputs (List[str]): The list of input variable names. No input arguments for this method.

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the HTTP3SocketServer instance.

            state_machine: The state machine object.

        Returns:
            None
        """
        host = state_machine.get_variable_value(inputs[0])
        port = state_machine.get_variable_value(inputs[1])
        port = int(port)
        client = HTTP3SocketClient(host, port)
        state_machine.set_variable_value(outputs[0], client)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=2)
    def start_http_3_client(inputs, outputs, state_machine):
        """
        Start the HTTP/3 client.

        Number of input arguments: 1
            - The HTTP3SocketClient instance

        Number of output arguments: 2
            - The event name
            - The message

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP3SocketClient instance variable

            outputs (List[str]): The list of output variable names. It contains two output arguments:
                - The name of the variable to store the event name
                - The name of the variable to store the message

            state_machine: The state machine object.

        Returns:
            None

        Possible events:
            - EventNames.TIMEOUT
            - EventNames.ERROR
            - EventNames.REJECTED
            - EventNames.CLIENT_STARTED
        """
        client = state_machine.get_variable_value(inputs[0])
        # Use persistent loop so the connection remains active across steps
        event, msg = client.start_sync()
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], msg)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=3)
    def send_http_3_client_frames(inputs, outputs, state_machine):
        """
        Send frames to the server.

        Number of input arguments: 2
            - The HTTP3SocketClient instance
            - The frames to send

        Number of output arguments: 3
            - The event name
            - The frames sent
            - The message

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP3SocketClient instance variable
                - The name of the client frames variable

            outputs (List[str]): The list of output variable names. It contains two output arguments:
                - The name of the variable to store the event name
                - The name of the variable to store the frames sent
                - The name of the variable to store the message

            state_machine: The state machine object.

        Returns:
            None

        Possible events:
            - EventNames.FRAMES_SENT
            - EventNames.GOAWAY_RECEIVED
            - EventNames.RESET_RECEIVED
            - EventNames.REJECTED
        """
        client = state_machine.get_variable_value(inputs[0])
        client_frames = state_machine.get_variable_value(inputs[1])
        # Set up frame specification for deterministic frame sending
        frame_spec = {"client_frames": client_frames}
        client.set_deterministic_frames(frame_spec)
        event, frames_sent, msg = client.send_deterministic_frames_sync("client_frames")
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], frames_sent)
        state_machine.set_variable_value(outputs[2], msg)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_http_3_client(inputs, outputs, state_machine):
        """
        Close the HTTP/3 client connection gracefully.
        
        Number of input arguments: 1
            - The HTTP3SocketClient instance
            
        Number of output arguments: 1
            - The event name
        """
        client = state_machine.get_variable_value(inputs[0])
        event = client.close_sync()
        state_machine.set_variable_value(outputs[0], event)
        state_machine.trigger_event(event)
