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

        Input Args: 0
        Output Args: 1 - The HTTPS1SocketServer instance.
        """
        server = HTTPS1SocketServer()
        state_machine.set_variable_value(outputs[0], server)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=2)
    def start_https_1_server(inputs, outputs, state_machine):
        """
        Start the HTTPS server.

        Input Args:
            - HTTPS1SocketServer instance
            - host (str)
            - port (int)

        Output Args:
            - event name
            - message
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

        Input Args:
            - HTTPS1SocketServer instance
            - route parameters (dict or list)

        Output Args: 0
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
    @parsing_decorator(input_args=1, output_args=3)
    def receive_https_1_requests(inputs, outputs, state_machine):
        """
        Receive HTTPS/1.1 requests.

        Input Args:
            - HTTPS1SocketServer instance

        Output Args:
            - event name
            - message
            - received data
        """
        server = state_machine.get_variable_value(inputs[0])
        event, message, received = server.receive_test_frames()
        state_machine.set_variable_value(outputs[0], event)
        state_machine.set_variable_value(outputs[1], message)
        state_machine.set_variable_value(outputs[2], received)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def close_https_1_server(inputs, outputs, state_machine):
        """
        Close the HTTPS server.

        Input Args:
            - HTTPS1SocketServer instance

        Output Args:
            - event name
        """
        server = state_machine.get_variable_value(inputs[0])
        event = server.close()
        state_machine.set_variable_value(outputs[0], event)
