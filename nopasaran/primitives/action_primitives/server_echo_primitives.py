from nopasaran.decorators import parsing_decorator
from nopasaran.tools.echo_socket_server import EchoSocketServer
from nopasaran.definitions.events import EventNames

class ServerEchoPrimitives:
    """
    Class containing TCP Echo server action primitives for the state machine.
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