import socket
import h2.connection
import h2.events

from nopasaran.definitions.events import EventNames
from nopasaran.decorators import parsing_decorator

from nopasaran.tools.http_2_overwrite import *

class HTTP2RequestPrimitives:
    """
    Class containing HTTP/2 action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def construct_http_2_request_packet(inputs, outputs, state_machine):
        """
        Construct an HTTP/2 request packet (headers frame) from a dictionary of parameters.

        Number of input arguments: 1
            - The dictionary with the request parameters

        Number of output arguments: 1
            - The request packet (headers list)

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the dictionary with request parameters.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the constructed request packet (headers list).

            state_machine: The state machine object.

        Returns:
            None
        """
        params = state_machine.get_variable_value(inputs[0])
        
        method = params.get(':method', 'GET')
        path = params.get(':path', '/')
        authority = params.get(':authority', 'localhost')
        scheme = params.get(':scheme', 'http')
        headers = params.get('headers', [])
        body = params.get('body', '').encode()

        # Construct the initial request headers
        request_headers = [
            (':method', method),
            (':path', path),
            (':authority', authority),
            (':scheme', scheme),
        ] + headers

        state_machine.set_variable_value(outputs[0], (request_headers, body))

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def add_http_2_request_header(inputs, outputs, state_machine):
        """
        Add a header to an HTTP/2 request packet.

        Number of input arguments: 3
            - The request headers list
            - The header name
            - The header value

        Number of output arguments: 1
            - The modified request headers list

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the request headers list.
                - The name of the variable containing the header name.
                - The name of the variable containing the header value.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request headers list.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_headers, body = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])
        header_value = state_machine.get_variable_value(inputs[2])

        # Add the new header
        request_headers.append((header_name, header_value))

        state_machine.set_variable_value(outputs[0], (request_headers, body))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def remove_http_2_request_header(inputs, outputs, state_machine):
        """
        Remove a header from an HTTP/2 request packet.

        Number of input arguments: 2
            - The request headers list
            - The header name

        Number of output arguments: 1
            - The modified request headers list

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request headers list.
                - The name of the variable containing the header name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request headers list.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_headers, body = state_machine.get_variable_value(inputs[0])
        header_name = state_machine.get_variable_value(inputs[1])

        # Remove the header
        request_headers = [header for header in request_headers if header[0] != header_name]

        state_machine.set_variable_value(outputs[0], (request_headers, body))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_http_2_request_headers(inputs, outputs, state_machine):
        """
        Add multiple headers to an HTTP/2 request packet.

        Number of input arguments: 2
            - The request headers list
            - The headers (list of header name-value pairs)

        Number of output arguments: 1
            - The modified request headers list

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request headers list.
                - The name of the variable containing the headers list.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request headers list.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_headers, body = state_machine.get_variable_value(inputs[0])
        headers_to_add = state_machine.get_variable_value(inputs[1])

        # Add the new headers
        request_headers.extend(headers_to_add)

        state_machine.set_variable_value(outputs[0], (request_headers, body))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def remove_http_2_request_headers(inputs, outputs, state_machine):
        """
        Remove multiple headers from an HTTP/2 request packet.

        Number of input arguments: 2
            - The request headers list
            - The headers (list of header names to be removed)

        Number of output arguments: 1
            - The modified request headers list

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the request headers list.
                - The name of the variable containing the list of header names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified request headers list.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_headers, body = state_machine.get_variable_value(inputs[0])
        headers_to_remove = state_machine.get_variable_value(inputs[1])

        # Remove the specified headers
        request_headers = [header for header in request_headers if header[0] not in headers_to_remove]

        state_machine.set_variable_value(outputs[0], (request_headers, body))

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def make_http_2_request(inputs, outputs, state_machine):
        """
        Make an HTTP/2 request using the headers list and body.

        Number of input arguments: 3
            - The request headers list and body tuple
            - The IP address to connect to
            - The port to connect to

        Number of output arguments: 1
            - The HTTP/2 response body

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the request headers list and body tuple.
                - The name of the variable containing the IP address or hostname.
                - The name of the variable containing the port number.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the HTTP/2 response body.

            state_machine: The state machine object.

        Returns:
            None
        """
        request_headers, body = state_machine.get_variable_value(inputs[0])
        ip = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))

        # Set up the socket and connection
        s = socket.create_connection((ip, port))
        c = h2.connection.H2Connection()
        c.initiate_connection()
        s.sendall(c.data_to_send())

        # Send headers
        c.send_headers(1, request_headers, end_stream=not bool(body))
        s.sendall(c.data_to_send())

        # Send body if exists
        if body:
            c.send_data(1, body, end_stream=True)
            s.sendall(c.data_to_send())

        response_body = b''
        response_stream_ended = False

        # Handle the response
        while not response_stream_ended:
            data = s.recv(65536 * 1024)
            if not data:
                break

            events = c.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.DataReceived):
                    c.acknowledge_received_data(event.flow_controlled_length, event.stream_id)
                    response_body += event.data
                if isinstance(event, h2.events.StreamEnded):
                    response_stream_ended = True
                    break

            s.sendall(c.data_to_send())

        # Close the connection
        c.close_connection()
        s.sendall(c.data_to_send())
        s.close()

        state_machine.set_variable_value(outputs[0], response_body)
        state_machine.trigger_event(EventNames.REQUEST_RECEIVED.name)