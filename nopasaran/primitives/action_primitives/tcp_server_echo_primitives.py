from nopasaran.decorators import parsing_decorator
from nopasaran.tools.tcp_echo_socket_server import EchoSocketServer
from nopasaran.definitions.events import EventNames

class TCPServerEchoPrimitives:
    """
    Class containing TCP Echo server action primitives for a state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_tcp_echo_server(inputs, outputs, state_machine):
        """
        Create an instance of EchoSocketServer.
        """
        server = EchoSocketServer()
        state_machine.set_variable_value(outputs[0], server)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=2)
    def start_echo_server(inputs, outputs, state_machine):
        """

        Number of input arguments: 3
          1) EchoSocketServer instance
          2) host (string)
          3) port (int)

        Number of output arguments: 2
          1) event (REQUEST_RECEIVED or TIMEOUT)
          2) response_data (string or None)

        This method uses a fixed TIMEOUT from your server or you can pass it as
        an input if you prefer.
        """
        server = state_machine.get_variable_value(inputs[0])
        host = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))

        # For demonstration, let's assume we want the server's self.TIMEOUT
        # Or define a separate input if you need a custom timeout
        data_bytes, event = server.start_and_wait_for_data(host, port, server.TIMEOUT)

        # Convert bytes to string if not None
        if data_bytes is not None:
            response_str = data_bytes.decode("utf-8", errors="ignore")
        else:
            response_str = None

        # Store in the state machine
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], response_str)
        state_machine.trigger_event(event)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_tcp_echo_server(inputs, outputs, state_machine):
        """
        Close the TCP Echo server (in case there's anything to close).
        """
        server = state_machine.get_variable_value(inputs[0])
        event = server.close()
        state_machine.set_variable_value(outputs[0], event)
