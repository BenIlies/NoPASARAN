from nopasaran.decorators import parsing_decorator
from nopasaran.tools.http_1_socket_server import HTTP1SocketServer

class HTTP1ResponsePrimitives:
    """
    Class containing HTTP server action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_http_1_server(inputs, outputs, state_machine):
        """
        Create an instance of HTTP1SocketServer.

        Number of input arguments: 0

        Number of output arguments: 1
            - The created HTTP1SocketServer instance

        Args:
            inputs (List[str]): The list of input variable names. No input arguments for this method.

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the HTTP1SocketServer instance.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = HTTP1SocketServer()
        state_machine.set_variable_value(outputs[0], server)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def add_http_1_route(inputs, outputs, state_machine):
        """
        Add a route to the HTTP server.

        Number of input arguments: 2
            - The HTTP1SocketServer instance
            - The dictionary with route parameters

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the HTTP1SocketServer instance.
                - The name of the variable containing the dictionary with route parameters.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        route_params = state_machine.get_variable_value(inputs[1])
        
        path = route_params.get('path')
        method = route_params.get('method')
        response_body = route_params.get('body', '')
        status_code = int(route_params.get('status_code'))
        headers = route_params.get('headers', [])

        server.routes[(path, method.upper())] = {
            'body': response_body,
            'status': status_code,
            'headers': headers
        }

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def remove_http_1_route(inputs, outputs, state_machine):
        """
        Remove a route from the HTTP server.

        Number of input arguments: 3
            - The HTTP1SocketServer instance
            - The path
            - The method (e.g., 'GET', 'POST')

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the HTTP1SocketServer instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])

        if (path, method.upper()) in server.routes:
            del server.routes[(path, method.upper())]

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def wait_for_http_1_request(inputs, outputs, state_machine):
        """
        Wait for an HTTP request.

        Number of input arguments: 3
            - The HTTP1SocketServer instance
            - The port to run the server on.
            - The timeout duration in seconds.

        Number of output arguments: 1
            - The received request data or None if a timeout occurs.

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the HTTP1SocketServer instance.
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

    @staticmethod
    @parsing_decorator(input_args=5, output_args=0)
    def add_http_1_response_header(inputs, outputs, state_machine):
        """
        Add a header to a route on the HTTP server.

        Number of input arguments: 5
            - The HTTP1SocketServer instance
            - The path
            - The method (e.g., 'GET', 'POST')
            - The header name
            - The header value

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains five mandatory input arguments:
                - The name of the variable containing the HTTP1SocketServer instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.
                - The name of the variable containing the header name.
                - The name of the variable containing the header value.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])
        header_name = state_machine.get_variable_value(inputs[3])
        header_value = state_machine.get_variable_value(inputs[4])

        route_key = (path, method.upper())
        if route_key in server.routes:
            headers = server.routes[route_key]['headers']
            headers.append((header_name, header_value))

    @staticmethod
    @parsing_decorator(input_args=4, output_args=0)
    def remove_http_1_response_header(inputs, outputs, state_machine):
        """
        Remove a header from a route on the HTTP server.

        Number of input arguments: 4
            - The HTTP1SocketServer instance
            - The path
            - The method (e.g., 'GET', 'POST')
            - The header name

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains four mandatory input arguments:
                - The name of the variable containing the HTTP1SocketServer instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.
                - The name of the variable containing the header name.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])
        header_name = state_machine.get_variable_value(inputs[3])

        route_key = (path, method.upper())
        if route_key in server.routes:
            headers = server.routes[route_key]['headers']
            headers = [header for header in headers if header[0] != header_name]
            server.routes[route_key]['headers'] = headers

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def add_http_1_response_content_length_header(inputs, outputs, state_machine):
        """
        Add a Content-Length header to a route on the HTTP server.

        Number of input arguments: 3
            - The HTTP1SocketServer instance
            - The path
            - The method (e.g., 'GET', 'POST')

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the HTTP1SocketServer instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])

        route_key = (path, method.upper())
        if route_key in server.routes:
            response_body = server.routes[route_key]['body']
            content_length = len(response_body.encode())
            headers = server.routes[route_key]['headers']
            headers.append(('Content-Length', str(content_length)))
