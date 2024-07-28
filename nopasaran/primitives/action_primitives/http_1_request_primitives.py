from nopasaran.decorators import parsing_decorator

from datetime import datetime, timedelta
from email.utils import formatdate
import requests_raw

class HTTP1RequestPrimitives:
    """
    Class containing HTTP/1.1 action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=5, output_args=1)
    def construct_request_packet(inputs, outputs, state_machine):
        """
        Construct an HTTP/1.1 request packet with a specified method.

        Number of input arguments: 5
            - The host
            - The port
            - The path
            - The protocol ('http' or 'https')
            - The HTTP method (e.g., 'GET', 'POST')

        Number of output arguments: 1
            - The request packet

        Args:
            inputs (List[str]): The list of input variable names. It contains four mandatory input arguments:
                - The name of the variable containing the host.
                - The name of the variable containing the port.
                - The name of the variable containing the path.
                - The name of the variable containing the protocol.
                - The name of the variable containing the HTTP method.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the constructed request packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        host = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        path = state_machine.get_variable_value(inputs[2])
        protocol = state_machine.get_variable_value(inputs[3])
        method = state_machine.get_variable_value(inputs[4])
    
        request_packet = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()

        state_machine.set_variable_value(outputs[0], (request_packet, host, path, protocol, port))

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def add_header(inputs, outputs, state_machine):
        """
        Add a header to an HTTP/1.1 request packet.

        Number of input arguments: 3
            - The request packet
            - The header name
            - The header value

        Number of output arguments: 1
            - The modified request packet

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the header name.
                - The name of the variable containing the header value.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet, host, path, protocol, port = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        header_value = state_machine.get_variable_value(inputs[2])
        
        request_str = request_packet.decode()
        insert_pos = request_str.find("\r\n\r\n")
        if insert_pos != -1:
            request_str = request_str[:insert_pos] + f"\r\n{header_name}: {header_value}" + request_str[insert_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], (request_packet, host, path, protocol, port))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def remove_header(inputs, outputs, state_machine):
        """
        Remove a header from an HTTP/1.1 request packet.

        Number of input arguments: 2
            - The request packet
            - The header name

        Number of output arguments: 1
            - The modified request packet

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the header name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet, host, path, protocol, port = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        
        request_str = request_packet.decode()
        header_line = f"{header_name}: "
        start_pos = request_str.find(header_line)
        if start_pos != -1:
            end_pos = request_str.find("\r\n", start_pos) + 2
            request_str = request_str[:start_pos] + request_str[end_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], (request_packet, host, path, protocol, port))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def calculate_if_modified_since(inputs, outputs, state_machine):
        """
        Calculate the 'If-Modified-Since' header value for an HTTP/1.1 request packet.

        Number of input arguments: 2
            - The request packet
            - The number of seconds ago for the 'If-Modified-Since' header

        Number of output arguments: 1
            - The modified request packet

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the number of seconds ago.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet, host, path, protocol, port = state_machine.get_variable_value(inputs[0])
        seconds_ago = state_machine.get_variable_value(inputs[1])
        
        time_ago = datetime.utcnow() - timedelta(seconds=seconds_ago)
        if_modified_since = formatdate(timeval=time_ago.timestamp(), usegmt=True)
        
        request_str = request_packet.decode()
        insert_pos = request_str.find("\r\n\r\n")
        if insert_pos != -1:
            request_str = request_str[:insert_pos] + f"\r\nIf-Modified-Since: {if_modified_since}" + request_str[insert_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], (request_packet, host, path, protocol, port))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def make_request(inputs, outputs, state_machine):
        """
        Make an HTTP/1.1 request using the request packet.

        Number of input arguments: 1
            - The request packet

        Number of output arguments: 1
            - The response

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the request packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the response.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet, host, path, protocol, port = state_machine.get_variable_value(inputs[0])
        
        url = f'{protocol}://{host}:{port}{path}'
        response = requests_raw.raw(url=url, data=request_packet)

        state_machine.set_variable_value(outputs[0], response)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_body_from_response(inputs, outputs, state_machine):
        """
        Extract the body from an HTTP/1.1 response.

        Number of input arguments: 1
            - The response

        Number of output arguments: 1
            - The body

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the response.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the body.

            state_machine: The state machine object.

        Returns:
            None
        """
        response = state_machine.get_variable_value(inputs[0])
        
        body = response.content.split(b'\r\n\r\n', 1)[1].decode()

        state_machine.set_variable_value(outputs[0], body)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def get_header_from_response(inputs, outputs, state_machine):
        """
        Get a header value from an HTTP/1.1 response.

        Number of input arguments: 2
            - The response
            - The header name

        Number of output arguments: 1
            - The header value

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the response.
                - The name of the variable containing the header name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the header value.

            state_machine: The state machine object.

        Returns:
            None
        """
        response = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        
        headers = response.headers
        header_value = headers.get(header_name, None)

        state_machine.set_variable_value(outputs[0], header_value)
