from nopasaran.decorators import parsing_decorator
from nopasaran.tools.tcp_echo_socket_server import EchoSocketServer
from nopasaran.definitions.events import EventNames

class TCPServerEchoPrimitives:
    """
    Class containing TCP Echo server action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_tcp_echo_server(inputs, outputs, state_machine):
        """
        Create an instance of EchoSocketServer.

        Number of input arguments: 0
        Number of output arguments: 1 (EchoSocketServer instance)
        """
        server = EchoSocketServer()
        state_machine.set_variable_value(outputs[0], server)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=2)
    def start_tcp_echo_server(inputs, outputs, state_machine):
        """
        Start the TCP Echo server.

        Inputs:
            - EchoSocketServer instance
            - Host
            - Port

        Outputs:
            - Event name
            - Message
        """
        server = state_machine.get_variable_value(inputs[0])
        host = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))
        event, message = server.start(host, port)
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], message)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=3)
    def receive_tcp_echo_data(inputs, outputs, state_machine):
        """
        Receive and echo TCP data.

        Inputs:
            - EchoSocketServer instance

        Outputs:
            - Event name
            - Message
            - Received data
        """
        server = state_machine.get_variable_value(inputs[0])
        event, message, received_data = server.receive_echo_data()
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], message)
        state_machine.set_variable_value(outputs[2], received_data)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_tcp_echo_server(inputs, outputs, state_machine):
        """
        Close the TCP Echo server.

        Inputs:
            - EchoSocketServer instance

        Outputs:
            - Event name
        """
        server = state_machine.get_variable_value(inputs[0])
        event = server.close()
        state_machine.set_variable_value(outputs[0], event)
