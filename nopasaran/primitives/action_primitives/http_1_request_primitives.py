from datetime import datetime, timedelta
from email.utils import formatdate
from nopasaran import utils
from nopasaran.decorators import parsing_decorator
from nopasaran.definitions.events import EventNames

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
    
        host = params.get('host', '')
        path = params['path']
        method = params['method']
        headers = params.get('headers', [])
        body = params.get('body', '')

        # Construct the initial request line
        request_line = f"{method} {path} HTTP/1.1\r\n"

        # Add the Host header if provided
        if host:
            request_line += f"Host: {host}\r\n"

        # Add other headers
        headers_str = ''.join([f"{header[0]}: {header[1]}\r\n" for header in headers])
        
        # Add the body
        if body:
            request_packet = f"{request_line}{headers_str}\r\n{body}".encode()
        else:
            request_packet = f"{request_line}{headers_str}\r\n".encode()

        state_machine.set_variable_value(outputs[0], request_packet)

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
        request_packet = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        header_value = state_machine.get_variable_value(inputs[2])
        
        request_str = request_packet.decode()
        insert_pos = request_str.find("\r\n\r\n")
        if insert_pos != -1:
            request_str = request_str[:insert_pos] + f"\r\n{header_name}: {header_value}" + request_str[insert_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], request_packet)

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
        request_packet = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        
        request_str = request_packet.decode()
        header_line = f"{header_name}: "
        start_pos = request_str.find(header_line)
        if start_pos != -1:
            end_pos = request_str.find("\r\n", start_pos) + 2
            request_str = request_str[:start_pos] + request_str[end_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], request_packet)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_http_1_request_headers(inputs, outputs, state_machine):
        """
        Add multiple headers to an HTTP/1.1 request packet.

        Number of input arguments: 2
            - The request packet
            - The headers (list of header name-value pairs)

        Number of output arguments: 1
            - The modified request packet

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the headers list.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet = state_machine.get_variable_value(inputs[0])
        headers = state_machine.get_variable_value(inputs[1])
        
        request_str = request_packet.decode()
        insert_pos = request_str.find("\r\n\r\n")
        if insert_pos != -1:
            headers_str = ''.join([f"\r\n{header[0]}: {header[1]}" for header in headers])
            request_str = request_str[:insert_pos] + headers_str + request_str[insert_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], request_packet)

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
        request_packet = state_machine.get_variable_value(inputs[0])
        headers = state_machine.get_variable_value(inputs[1])
        
        request_str = request_packet.decode()
        for header_name in headers:
            header_line = f"{header_name}: "
            start_pos = request_str.find(header_line)
            if start_pos != -1:
                end_pos = request_str.find("\r\n", start_pos) + 2
                request_str = request_str[:start_pos] + request_str[end_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], request_packet)

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
        request_packet = state_machine.get_variable_value(inputs[0])
        seconds_ago = state_machine.get_variable_value(inputs[1])
        
        time_ago = datetime.utcnow() - timedelta(seconds=seconds_ago)
        if_modified_since = formatdate(timeval=time_ago.timestamp(), usegmt=True)
        
        request_str = request_packet.decode()
        insert_pos = request_str.find("\r\n\r\n")
        if insert_pos != -1:
            request_str = request_str[:insert_pos] + f"\r\nIf-Modified-Since: {if_modified_since}" + request_str[insert_pos:]
        request_packet = request_str.encode()

        state_machine.set_variable_value(outputs[0], request_packet)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def make_http_1_request(inputs, outputs, state_machine):
        """
        Make an HTTP/1.1 request using the request packet.

        Number of input arguments: 3
            - The request packet
            - The ip address to connect to
            - The port to connect to

        Number of output arguments: 1
            - The HTTP response

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the ip address or hostname.
                - The name of the variable containing the port number.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the HTTP response.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_packet = state_machine.get_variable_value(inputs[0])
        ip = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))
        
        response = utils.send_request(ip, port, request_packet)
        state_machine.set_variable_value(outputs[0], response)

        if response is not None:
            state_machine.trigger_event(EventNames.RESPONSE_RECEIVED.name)
        else:
            state_machine.trigger_event(EventNames.REQUEST_ERROR.name)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_body_from_http_1_response(inputs, outputs, state_machine):
        """
        Extract the body from an HTTP/1.1 response.

        Number of input arguments: 1
            - The HTTP response

        Number of output arguments: 1
            - The response body

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the HTTP response.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the response body.

            state_machine: The state machine object.

        Returns:
            None
        """
        response = state_machine.get_variable_value(inputs[0])
        
        response_str = response.decode()
        body_start = response_str.find("\r\n\r\n") + 4
        body = response_str[body_start:]

        state_machine.set_variable_value(outputs[0], body)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def get_header_from_http_1_response(inputs, outputs, state_machine):
        """
        Get a header value from an HTTP/1.1 response.

        Number of input arguments: 2
            - The HTTP response
            - The header name

        Number of output arguments: 1
            - The header value

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the HTTP response.
                - The name of the variable containing the header name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the header value.

            state_machine: The state machine object.

        Returns:
            None
        """
        response = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        
        response_str = response.decode()
        headers, _ = response_str.split("\r\n\r\n", 1)
        headers_lines = headers.split("\r\n")[1:]
        headers_list = [line.split(":", 1) for line in headers_lines if ":" in line]
        headers_dict = {}
        for header in headers_list:
            key = header[0].strip()
            value = header[1].strip()
            if key not in headers_dict:
                headers_dict[key] = []
            headers_dict[key].append(value)
        header_value = headers_dict.get(header_name, [None])

        state_machine.set_variable_value(outputs[0], header_value)
