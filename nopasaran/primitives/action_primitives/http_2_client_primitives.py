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
    @parsing_decorator(input_args=4, output_args=0)
    def start_http_2_client(inputs, outputs, state_machine):
        """
        Start the HTTP/2 client.

        Number of input arguments: 4
            - The HTTP2SocketClient instance
            - The tls_enabled flag
            - The TLS protocol to use
            - The connection settings for the client

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable
                - The name of the tls_enabled flag variable
                - The name of the TLS protocol variable
                - The name of the connection settings variable

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        client = state_machine.get_variable_value(inputs[0])
        tls_enabled = state_machine.get_variable_value(inputs[1])
        protocol = state_machine.get_variable_value(inputs[2])
        connection_settings_client = state_machine.get_variable_value(inputs[3])

        if tls_enabled == 'true':
            tls_enabled = True
        else:
            tls_enabled = False

        client.start(tls_enabled, protocol, connection_settings_client)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def wait_for_server_preface(inputs, outputs, state_machine):
        """
        Wait for the server's SETTINGS frame.

        Number of input arguments: 1
            - The HTTP2SocketClient instance

        Number of output arguments: 1
            - The event name

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the event name

            state_machine: The state machine object.

        Returns:
            None
        """
        client = state_machine.get_variable_value(inputs[0])
        event = client.wait_for_server_preface()
        state_machine.set_variable_value(outputs[0], event)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def wait_for_server_ack(inputs, outputs, state_machine):
        """
        Wait for the server's SETTINGS_ACK frame.

        Number of input arguments: 1
            - The HTTP2SocketClient instance

        Number of output arguments: 1
            - The event name

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the event name

            state_machine: The state machine object.

        Returns:
            None
        """
        client = state_machine.get_variable_value(inputs[0])
        event = client.wait_for_server_ack()
        state_machine.set_variable_value(outputs[0], event)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=2)
    def receive_server_frames(inputs, outputs, state_machine):
        """
        Wait for server's frames.

        Number of input arguments: 2
            - The HTTP2SocketClient instance
            - The server frames to receive

        Number of output arguments: 2
            - The result of the test
            - The event name
            - The message to output

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable
                - The name of the server frames variable

            outputs (List[str]): The list of output variable names. It contains two output arguments:
                - The name of the variable to store the result of the test
                - The name of the variable to store the event name
                - The name of the variable to store the message

            state_machine: The state machine object.

        Returns:
            None
        """
        client = state_machine.get_variable_value(inputs[0])
        server_frames = state_machine.get_variable_value(inputs[1])
        result, event, msg = client.receive_server_frames(server_frames)
        state_machine.set_variable_value(outputs[0], result)
        state_machine.set_variable_value(outputs[1], event)
        state_machine.set_variable_value(outputs[2], msg)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def send_client_frames(inputs, outputs, state_machine):
        """
        Send frames to the server.

        Number of input arguments: 2
            - The HTTP2SocketClient instance
            - The frames to send

        Number of output arguments: 1
            - The event name

        Args:
            inputs (List[str]): The list of input variable names containing:
                - The name of the HTTP2SocketClient instance variable
                - The name of the client frames variable

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the event name

            state_machine: The state machine object.

        Returns:
            None
        """
        client = state_machine.get_variable_value(inputs[0])
        client_frames = state_machine.get_variable_value(inputs[1])
        event = client.send_frames(client_frames)
        state_machine.set_variable_value(outputs[0], event)
