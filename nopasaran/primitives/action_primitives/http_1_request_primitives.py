from nopasaran.decorators import parsing_decorator
from nopasaran.definitions.events import EventNames

from datetime import datetime, timedelta
from email.utils import formatdate
import requests_raw

class HTTP1RequestPrimitives:
    """
    Class containing HTTP/1.1 action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def construct_http_1_request_packet(inputs, outputs, state_machine):
        """
        Construct an HTTP/1.1 request packet from a dictionary of parameters.

        Number of input arguments: 1
            - The dictionary with the request parameters

        Number of output arguments: 1
            - The request packet

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the dictionary with request parameters.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the constructed request packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        params = state_machine.get_variable_value(inputs[0])
    
        host = params['host']
        path = params['path']
        protocol = params['protocol']
        method = params['method']
        ip = params['ip']
        headers = params.get('headers', {})  # Extract headers if present
        body = params.get('body', '')        # Extract body if present

        # Construct the initial request line
        request_line = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n"

        # Add headers
        headers_str = ''.join([f"{header_name}: {header_value}\r\n" for header_name, header_value in headers.items()])
        
        # Add the body
        if body:
            request_packet = f"{request_line}{headers_str}\r\n{body}".encode()
        else:
            request_packet = f"{request_line}{headers_str}\r\n".encode()

        state_machine.set_variable_value(outputs[0], (request_packet, path, protocol, ip))

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def add_http_1_request_header(inputs, outputs, state_machine):
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
        request_packet, path, protocol, ip = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        header_value = state_machine.get_variable_value(inputs[2])
        
        request_str = request_packet.decode()
        insert_pos = request_str.find("\r\n\r\n")
        if insert_pos != -1:
            request_str = request_str[:insert_pos] + f"\r\n{header_name}: {header_value}" + request_str[insert_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], (request_packet, path, protocol, ip))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def remove_http_1_request_header(inputs, outputs, state_machine):
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
        request_packet, path, protocol, ip = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        
        request_str = request_packet.decode()
        header_line = f"{header_name}: "
        start_pos = request_str.find(header_line)
        if start_pos != -1:
            end_pos = request_str.find("\r\n", start_pos) + 2
            request_str = request_str[:start_pos] + request_str[end_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], (request_packet, path, protocol, ip))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_http_1_request_headers(inputs, outputs, state_machine):
        """
        Add multiple headers to an HTTP/1.1 request packet.

        Number of input arguments: 2
            - The request packet
            - The headers (dictionary of header name-value pairs)

        Number of output arguments: 1
            - The modified request packet

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the headers dictionary.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet, path, protocol, ip = state_machine.get_variable_value(inputs[0])
        headers = state_machine.get_variable_value(inputs[1])
        
        request_str = request_packet.decode()
        insert_pos = request_str.find("\r\n\r\n")
        if insert_pos != -1:
            headers_str = ''.join([f"\r\n{header_name}: {header_value}" for header_name, header_value in headers.items()])
            request_str = request_str[:insert_pos] + headers_str + request_str[insert_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], (request_packet, path, protocol, ip))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def remove_http_1_request_headers(inputs, outputs, state_machine):
        """
        Remove multiple headers from an HTTP/1.1 request packet.

        Number of input arguments: 2
            - The request packet
            - The headers (list of header names to be removed)

        Number of output arguments: 1
            - The modified request packet

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the list of header names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet, path, protocol, ip = state_machine.get_variable_value(inputs[0])
        headers = state_machine.get_variable_value(inputs[1])
        
        request_str = request_packet.decode()
        for header_name in headers:
            header_line = f"{header_name}: "
            start_pos = request_str.find(header_line)
            if start_pos != -1:
                end_pos = request_str.find("\r\n", start_pos) + 2
                request_str = request_str[:start_pos] + request_str[end_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], (request_packet, path, protocol, ip))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def calculate_http_1_request_if_modified_since(inputs, outputs, state_machine):
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
        request_packet, path, protocol, ip = state_machine.get_variable_value(inputs[0])
        seconds_ago = state_machine.get_variable_value(inputs[1])
        
        time_ago = datetime.utcnow() - timedelta(seconds=seconds_ago)
        if_modified_since = formatdate(timeval=time_ago.timestamp(), usegmt=True)
        
        request_str = request_packet.decode()
        insert_pos = request_str.find("\r\n\r\n")
        if insert_pos != -1:
            request_str = request_str[:insert_pos] + f"\r\nIf-Modified-Since: {if_modified_since}" + request_str[insert_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], (request_packet, path, protocol, ip))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def make_http_1_request(inputs, outputs, state_machine):
        """
        Make an HTTP/1.1 request using the request packet.

        Number of input arguments: 2
            - The request packet
            - The port

        Number of output arguments: 1
            - The response

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the port.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the response.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet, path, protocol, ip = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        
        url = f'{protocol}://{ip}:{port}{path}'
        response = requests_raw.raw(url=url, data=request_packet)

        state_machine.set_variable_value(outputs[0], response)
        state_machine.trigger_event(EventNames.REQUEST_RECEIVED.name)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_body_from_http_1_response(inputs, outputs, state_machine):
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
        
        body = response.content.decode()

        state_machine.set_variable_value(outputs[0], body)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def get_header_from_http_1_response(inputs, outputs, state_machine):
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
