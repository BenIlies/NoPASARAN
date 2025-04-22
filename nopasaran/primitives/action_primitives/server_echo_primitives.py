from nopasaran.decorators import parsing_decorator
from nopasaran.tools.echo_socket_server import EchoSocketServer
from nopasaran.definitions.events import EventNames

class ServerEchoPrimitives:
    """
    Class containing Echo server action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_echo_server(inputs, outputs, state_machine):
        """
        Create a TCP Echo server instance.

        Number of input arguments: 0
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): No input arguments.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the EchoSocketServer instance.
            state_machine: The state machine object.

        Returns:
            None
        """
        server = EchoSocketServer()
        state_machine.set_variable_value(outputs[0], server)
    
    @staticmethod
    @parsing_decorator(input_args=4, output_args=2)
    def start_udp_echo_server(inputs, outputs, state_machine):
        """
        Start the UDP Echo server and wait for a datagram.

        Number of input arguments: 4
        Number of output arguments: 2
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the EchoSocketServer instance.
                - The name of the variable containing the host address.
                - The name of the variable containing the port number.
                - The name of the variable containing the timeout in seconds.

            outputs (List[str]): The list of output variable names. It contains two mandatory output arguments:
                - The name of the variable to store the triggered event (REQUEST_RECEIVED or TIMEOUT).
                - The name of the variable to store the response data (string or None).
            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        host = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))
        timeout = int(state_machine.get_variable_value(inputs[3]))

        data_bytes, event = server.start_and_wait_for_udp_data(host, port, timeout)

        response_str = data_bytes.decode("utf-8", errors="ignore") if data_bytes is not None else None

        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], response_str)
        state_machine.trigger_event(event)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_udp_echo_server(inputs, outputs, state_machine):
        """
        Close the UDP Echo server.

        Number of input arguments: 1
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the EchoSocketServer instance.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the close event result.
            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        event = server.close()
        state_machine.set_variable_value(outputs[0], event)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=2)
    def start_tcp_echo_server(inputs, outputs, state_machine):
        """
        Start the TCP Echo server and wait for a connection.

        Number of input arguments: 4
        Number of output arguments: 2
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the EchoSocketServer instance.
                - The name of the variable containing the host address.
                - The name of the variable containing the port number.
                - The name of the variable containing the timeout in seconds.

            outputs (List[str]): The list of output variable names. It contains two mandatory output arguments:
                - The name of the variable to store the triggered event (REQUEST_RECEIVED or TIMEOUT).
                - The name of the variable to store the response data (string or None).
            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        host = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))
        timeout= int(state_machine.get_variable_value(inputs[3]))

        data_bytes, event = server.start_and_wait_for_tcp_data(host, port, timeout)

        response_str = data_bytes.decode("utf-8", errors="ignore") if data_bytes is not None else None

        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], response_str)
        state_machine.trigger_event(event)

   
    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_tcp_echo_server(inputs, outputs, state_machine):
        """
        Close the TCP Echo server.

        Number of input arguments: 1
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the EchoSocketServer instance.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the close event result.
            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        event = server.close()
        state_machine.set_variable_value(outputs[0], event)


    