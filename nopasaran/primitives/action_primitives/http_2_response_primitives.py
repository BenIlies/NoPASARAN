from nopasaran.decorators import parsing_decorator
from nopasaran.tools.http_2_socket_server import HTTP2SocketServer

class HTTP2ResponsePrimitives:
    """
    Class containing HTTP/2 server action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_http_2_server(inputs, outputs, state_machine):
        """
        Create an instance of HTTP2SocketServer.

        Number of input arguments: 0

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
        server = HTTP2SocketServer()
        state_machine.set_variable_value(outputs[0], server)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def add_http_2_route(inputs, outputs, state_machine):
        """
        Add a route to the HTTP/2 server.

        Number of input arguments: 2
            - The HTTP2SocketServer instance
            - The dictionary with route parameters

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the HTTP2SocketServer instance.
                - The name of the variable containing the dictionary with route parameters.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        route_params = state_machine.get_variable_value(inputs[1])
        
        path = route_params.get(':path')
        method = route_params.get(':method')
        response_body = route_params.get('body', '')
        status_code = int(route_params.get(':status'))
        headers = route_params.get('headers', [])

        server.routes[(path, method.upper())] = {
            'body': response_body,
            'status': status_code,
            'headers': headers
        }


    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def wait_for_http_2_request(inputs, outputs, state_machine):
        """
        Wait for an HTTP/2 request.

        Number of input arguments: 3
            - The HTTP2SocketServer instance
            - The port to run the server on.
            - The timeout duration in seconds.

        Number of output arguments: 1
            - The received request data or None if a timeout occurs.

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the HTTP2SocketServer instance.
                - The name of the variable containing the port.
                - The name of the variable containing the timeout duration.

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the received request data.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        timeout = int(state_machine.get_variable_value(inputs[2]))
        received_request_data, event = server.wait_for_request(port=port, timeout=timeout)
        state_machine.set_variable_value(outputs[0], received_request_data)
        state_machine.trigger_event(event)