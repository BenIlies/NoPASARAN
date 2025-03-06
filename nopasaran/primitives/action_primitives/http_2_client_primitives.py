from nopasaran.decorators import parsing_decorator
from nopasaran.tools.http_2_socket_client import HTTP2SocketClient

class HTTP2ClientPrimitives:
    """
    Class containing HTTP/2 client action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def create_http_2_client(inputs, outputs, state_machine):
        """
        Create an instance of HTTP2SocketClient. 
        Number of input arguments: 2
            - The host
            - The port

        Number of output arguments: 1
            - The created HTTP2SocketServer instance

        Args:
            inputs (List[str]): The list of input variable names. No input arguments for this method.

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the HTTP2SocketServer instance.

            state_machine: The state machine object.

        Returns:
            None
        """
        host = state_machine.get_variable_value(inputs[0])
        port = state_machine.get_variable_value(inputs[1])
        port = int(port)
        client = HTTP2SocketClient(host, port)
        state_machine.set_variable_value(outputs[0], client)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=2)
    def start_http_2_client(inputs, outputs, state_machine):
        """
        Start the HTTP/2 client.

        Number of input arguments: 4
            - The HTTP2SocketClient instance
            - The tls_enabled flag
            - The connection settings for the client
            - The cloudflare_origin flag

        Number of output arguments: 2
            - The event name
            - The message

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable
                - The name of the tls_enabled flag variable
                - The name of the connection settings variable
                - The name of the cloudflare_origin flag variable

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
        tls_enabled = state_machine.get_variable_value(inputs[1])
        connection_settings_client = state_machine.get_variable_value(inputs[2])
        cloudflare_origin = state_machine.get_variable_value(inputs[3])

        event, msg = client.start(tls_enabled, connection_settings_client, cloudflare_origin)
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], msg)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=3)
    def wait_for_server_preface(inputs, outputs, state_machine):
        """
        Wait for the server's SETTINGS frame.

        Number of input arguments: 1
            - The HTTP2SocketClient instance

        Number of output arguments: 3
            - The event name
            - The message
            - The frames received

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable

            outputs (List[str]): The list of output variable names. It contains three output arguments:
                - The name of the variable to store the event name
                - The name of the variable to store the message
                - The name of the variable to store the frames received

            state_machine: The state machine object.

        Returns:
            None
        """
        client = state_machine.get_variable_value(inputs[0])
        event, msg, frames = client.wait_for_preface()
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], msg)
        state_machine.set_variable_value(outputs[2], frames)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=2)
    def wait_for_server_ack(inputs, outputs, state_machine):
        """
        Wait for the server's SETTINGS_ACK frame.

        Number of input arguments: 1
            - The HTTP2SocketClient instance

        Number of output arguments: 2
            - The event name
            - The message

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable

            outputs (List[str]): The list of output variable names. It contains two output arguments:
                - The name of the variable to store the event name
                - The name of the variable to store the message

            state_machine: The state machine object.

        Returns:
            None
        """
        client = state_machine.get_variable_value(inputs[0])
        event, msg = client.wait_for_preface_ack()
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], msg)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=3)
    def receive_server_frames(inputs, outputs, state_machine):
        """
        Wait for server's frames.

        Number of input arguments: 2
            - The HTTP2SocketClient instance
            - The server frames to receive

        Number of output arguments: 3
            - The event name
            - The message
            - The frames received

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable
                - The name of the server frames variable

            outputs (List[str]): The list of output variable names. It contains three output arguments:
                - The name of the variable to store the event name
                - The name of the variable to store the message
                - The name of the variable to store the frames received

            state_machine: The state machine object.

        Returns:
            None

        Possible events:
            - EventNames.TIMEOUT
            - EventNames.RESET_RECEIVED
            - EventNames.GOAWAY_RECEIVED
            - EventNames.REJECTED
            - EventNames.RECEIVED_FRAMES
        """
        client = state_machine.get_variable_value(inputs[0])
        test_frames = state_machine.get_variable_value(inputs[1])
        event, msg, frames_received = client.receive_test_frames(test_frames)
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], msg)
        state_machine.set_variable_value(outputs[2], frames_received)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=3)
    def send_client_frames(inputs, outputs, state_machine):
        """
        Send frames to the server.

        Number of input arguments: 2
            - The HTTP2SocketClient instance
            - The frames to send

        Number of output arguments: 3
            - The event name
            - The frames sent
            - The message

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable
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
        event, frames_sent, msg = client.send_frames(client_frames)
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], frames_sent)
        state_machine.set_variable_value(outputs[2], msg)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_http_2_client(inputs, outputs, state_machine):
        """
        Close the HTTP/2 client connection gracefully.
        
        Number of input arguments: 1
            - The HTTP2SocketClient instance
            
        Number of output arguments: 1
            - The event name
        """
        client = state_machine.get_variable_value(inputs[0])
        event = client.close()
        state_machine.set_variable_value(outputs[0], event)
        state_machine.trigger_event(event)
