from nopasaran.decorators import parsing_decorator
from nopasaran.tools.https_1_socket_server import HTTPS1SocketServer

class HTTPS1ResponsePrimitives:
    """
    Class containing HTTPS/1.1 server action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_https_1_server(inputs, outputs, state_machine):
        """
        Create an instance of HTTPS1SocketServer.

        Number of input arguments: 0

        Number of output arguments: 1
            - The created HTTPS1SocketServer instance

        Args:
            inputs (List[str]): The list of input variable names. No input arguments for this method.

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the HTTPS1SocketServer instance.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = HTTPS1SocketServer()
        state_machine.set_variable_value(outputs[0], server)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=2)
    def start_https_1_server(inputs, outputs, state_machine):
        """
        Start the HTTPS server.

        Number of input arguments: 3
            - The HTTPS1SocketServer instance
            - The host to run the server on.
            - The port to run the server on.

        Number of output arguments: 2
            - The event name
            - The message

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the HTTPS1SocketServer instance.
                - The name of the variable containing the host.
                - The name of the variable containing the port.

            outputs (List[str]): The list of output variable names. It contains two output arguments:
                - The name of the variable to store the event name.
                - The name of the variable to store the message.

            state_machine: The state machine object.
        """
        server = state_machine.get_variable_value(inputs[0])
        host = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))
        event, message = server.start(host, port)
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], message)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def add_https_1_route(inputs, outputs, state_machine):
        """
        Add a route to the HTTPS server.

        Number of input arguments: 2
            - The HTTPS1SocketServer instance
            - The dictionary or list with route parameters

        Number of output arguments: 0

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the HTTPS1SocketServer instance.
                - The name of the variable containing the dictionary or list with route parameters.

            outputs (List[str]): The list of output variable names. No output arguments for this method.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        route_params = state_machine.get_variable_value(inputs[1])

        if isinstance(route_params, dict):
            route_params = [route_params]

        for params in route_params:
            path = params.get("path")
            method = params.get("method")
            body = params.get("body", "")
            status = int(params.get("status_code"))
            headers = params.get("headers", [])

            route_key = (path, method.upper())
            if route_key not in server.routes:
                server.routes[route_key] = []

            server.routes[route_key].append({
                "body": body,
                "status": status,
                "headers": headers
            })

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def wait_for_https_1_request(inputs, outputs, state_machine):
        """
        Wait for an HTTPS request.

        Number of input arguments: 3
            - The HTTPS1SocketServer instance
            - The port to run the server on.
            - The timeout duration in seconds.

        Number of output arguments: 1
            - The received request data or None if a timeout occurs.

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the HTTPS1SocketServer instance.
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

        received_request_data, event = server.wait_for_request(port, timeout)
        state_machine.set_variable_value(outputs[0], received_request_data)
        state_machine.trigger_event(event)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_https_1_server(inputs, outputs, state_machine):
        """
        Close the HTTPS server.

        Number of input arguments: 1
            - The HTTPS1SocketServer instance

        Number of output arguments: 1
            - The event name

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the HTTPS1SocketServer instance.

            outputs (List[str]): The list of output variable names. It contains one output argument:
                - The name of the variable to store the event name.

            state_machine: The state machine object.

        Returns:
            None
        """
        server = state_machine.get_variable_value(inputs[0])
        event = server.close()
        state_machine.set_variable_value(outputs[0], event)
