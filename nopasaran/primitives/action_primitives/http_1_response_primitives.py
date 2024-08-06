from nopasaran.decorators import parsing_decorator
from nopasaran.tools.http_1_socket_server import HTTP1SocketServer

class HTTP1ResponsePrimitives:
    """
    Class containing HTTP server action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def add_http_1_route(inputs, outputs, state_machine):
        """
        Add a route to the HTTP server.

        Number of input arguments: 1
            - The dictionary with route parameters

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the dictionary with route parameters.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        route_params = state_machine.get_variable_value(inputs[0])
        
        path = route_params.get('path')
        method = route_params.get('method')
        response_body = route_params.get('body', '')
        status_code = int(route_params.get('status_code'))
        headers = route_params.get('headers', {})

        HTTP1SocketServer.routes[(path, method.upper())] = {
            'body': response_body,
            'status': status_code,
            'headers': headers
        }

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def remove_http_1_route(inputs, outputs, state_machine):
        """
        Remove a route from the HTTP server.

        Number of input arguments: 2
            - The path
            - The method (e.g., 'GET', 'POST')

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the path.
                - The name of the variable containing the method.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        path = state_machine.get_variable_value(inputs[0])
        method = state_machine.get_variable_value(inputs[1])

        if (path, method.upper()) in HTTP1SocketServer.routes:
            del HTTP1SocketServer.routes[(path, method.upper())]

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def wait_for_http_1_request(inputs, outputs, state_machine):
        """
        Wait for an HTTP request.

        Number of input arguments: 2
            - The port to run the server on.
            - The timeout duration in seconds.

        Number of output arguments: 1
            - The received request data or None if a timeout occurs.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the port.
                - The name of the variable containing the timeout duration.

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the received request data.

            state_machine: The state machine object.

        Returns:
            None
        """
        port = int(state_machine.get_variable_value(inputs[0]))
        timeout = int(state_machine.get_variable_value(inputs[1]))
        received_request_data, event = HTTP1SocketServer.wait_for_request(port=port, timeout=timeout)
        state_machine.set_variable_value(outputs[0], received_request_data)
        state_machine.trigger_event(event)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=0)
    def add_http_1_response_header(inputs, outputs, state_machine):
        """
        Add a header to a route on the HTTP server.

        Number of input arguments: 4
            - The path
            - The method (e.g., 'GET', 'POST')
            - The header name
            - The header value

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains four mandatory input arguments:
                - The name of the variable containing the path.
                - The name of the variable containing the method.
                - The name of the variable containing the header name.
                - The name of the variable containing the header value.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        path = state_machine.get_variable_value(inputs[0])
        method = state_machine.get_variable_value(inputs[1])
        header_name = state_machine.get_variable_value(inputs[2])
        header_value = state_machine.get_variable_value(inputs[3])

        route_key = (path, method.upper())
        if route_key in HTTP1SocketServer.routes:
            HTTP1SocketServer.routes[route_key]['headers'][header_name] = header_value

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def remove_http_1_response_header(inputs, outputs, state_machine):
        """
        Remove a header from a route on the HTTP server.

        Number of input arguments: 3
            - The path
            - The method (e.g., 'GET', 'POST')
            - The header name

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the path.
                - The name of the variable containing the method.
                - The name of the variable containing the header name.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        path = state_machine.get_variable_value(inputs[0])
        method = state_machine.get_variable_value(inputs[1])
        header_name = state_machine.get_variable_value(inputs[2])

        route_key = (path, method.upper())
        if route_key in HTTP1SocketServer.routes:
            if header_name in HTTP1SocketServer.routes[route_key]['headers']:
                del HTTP1SocketServer.routes[route_key]['headers'][header_name]

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def add_http_1_response_content_length_header(inputs, outputs, state_machine):
        """
        Add a Content-Length header to a route on the HTTP server.

        Number of input arguments: 2
            - The path
            - The method (e.g., 'GET', 'POST')

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the path.
                - The name of the variable containing the method.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        path = state_machine.get_variable_value(inputs[0])
        method = state_machine.get_variable_value(inputs[1])

        route_key = (path, method.upper())
        if route_key in HTTP1SocketServer.routes:
            response_body = HTTP1SocketServer.routes[route_key]['body']
            content_length = len(response_body.encode())
            HTTP1SocketServer.routes[route_key]['headers']['Content-Length'] = content_length
