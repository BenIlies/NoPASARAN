from nopasaran.decorators import parsing_decorator
from nopasaran.tools.http_1_response_handler import HTTP1ResponseHandler

class HTTP1ResponsePrimitives:
    """
    Class containing HTTP server action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_http_1_handler(inputs, outputs, state_machine):
        """
        Create an HTTP1ResponseHandler instance as the request handler.

        Number of input arguments: 0

        Number of output arguments: 1
            - The instance of the created HTTP1ResponseHandler.

        Args:
            inputs (List[str]): The list of input variable names. No input arguments for this method.
            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the created HTTP1ResponseHandler instance.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], HTTP1ResponseHandler())

    @staticmethod
    @parsing_decorator(input_args=6, output_args=0)
    def add_http_1_route(inputs, outputs, state_machine):
        """
        Add a route to a HTTP1ResponseHandler instance.

        Number of input arguments: 6
            - The response handler instance
            - The path
            - The method (e.g., 'GET', 'POST')
            - The response body
            - The status code (default: 200)
            - The headers (optional, dictionary format)

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains six mandatory input arguments:
                - The name of the variable containing the response handler instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.
                - The name of the variable containing the response body.
                - The name of the variable containing the status code.
                - The name of the variable containing the headers.
            outputs (List[str]): The list of output variable names. No output arguments for this method.
            state_machine: The state machine object.

        Returns:
            None
        """
        response_handler_instance = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])
        response_body = state_machine.get_variable_value(inputs[3])
        status_code = int(state_machine.get_variable_value(inputs[4]))
        headers = state_machine.get_variable_value(inputs[5])

        response_handler_instance.add_route(path, method, response_body, status_code, headers)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def remove_http_1_route(inputs, outputs, state_machine):
        """
        Remove a route from an HTTP1ResponseHandler instance.

        Number of input arguments: 3
            - The response handler instance
            - The path
            - The method (e.g., 'GET', 'POST')

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the response handler instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.
            outputs (List[str]): The list of output variable names. No output arguments for this method.
            state_machine: The state machine object.

        Returns:
            None
        """
        response_handler_instance = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])

        response_handler_instance.remove_route(path, method)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def wait_for_http_1_request(inputs, outputs, state_machine):
        """
        Wait for an HTTP request.

        Number of input arguments: 3
            - The handler instance
            - The server port
            - The timeout duration in seconds.

        Number of output arguments: 1
            - The received request data or None if a timeout occurs.

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the handler instance.
                - The name of the variable containing the server port.
                - The name of the variable containing the timeout duration.
            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the received request data.
            state_machine: The state machine object.

        Returns:
            None
        """
        handler = state_machine.get_variable_value(inputs[0])
        timeout = int(state_machine.get_variable_value(inputs[1]))
        received_request_data, event = handler.wait_for_request(port=port, timeout=timeout)
        state_machine.set_variable_value(outputs[0], received_request_data)
        state_machine.trigger_event(event)

    @staticmethod
    @parsing_decorator(input_args=5, output_args=0)
    def add_http_1_response_header(inputs, outputs, state_machine):
        """
        Add a header to a route on the HTTP handler.

        Number of input arguments: 5
            - The handler instance
            - The path
            - The method (e.g., 'GET', 'POST')
            - The header name
            - The header value

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains five mandatory input arguments:
                - The name of the variable containing the handler instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.
                - The name of the variable containing the header name.
                - The name of the variable containing the header value.
            outputs (List[str]): The list of output variable names. No output arguments for this method.
            state_machine: The state machine object.

        Returns:
            None
        """
        handler = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])
        header_name = state_machine.get_variable_value(inputs[3])
        header_value = state_machine.get_variable_value(inputs[4])

        handler.add_header(path, method, header_name, header_value)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=0)
    def remove_http_1_response_header(inputs, outputs, state_machine):
        """
        Remove a header from a route on the HTTP handler.

        Number of input arguments: 4
            - The handler instance
            - The path
            - The method (e.g., 'GET', 'POST')
            - The header name

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains four mandatory input arguments:
                - The name of the variable containing the handler instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.
                - The name of the variable containing the header name.
            outputs (List[str]): The list of output variable names. No output arguments for this method.
            state_machine: The state machine object.

        Returns:
            None
        """
        handler = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])
        header_name = state_machine.get_variable_value(inputs[3])

        handler.remove_header(path, method, header_name)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def add_http_1_response_content_length_header(inputs, outputs, state_machine):
        """
        Add a Content-Length header to a route on the HTTP handler.

        Number of input arguments: 3
            - The handler instance
            - The path
            - The method (e.g., 'GET', 'POST')

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the handler instance.
                - The name of the variable containing the path.
                - The name of the variable containing the method.
            outputs (List[str]): The list of output variable names. No output arguments for this method.
            state_machine: The state machine object.

        Returns:
            None
        """
        handler = state_machine.get_variable_value(inputs[0])
        path = state_machine.get_variable_value(inputs[1])
        method = state_machine.get_variable_value(inputs[2])

        handler.add_content_length_header(path, method)
