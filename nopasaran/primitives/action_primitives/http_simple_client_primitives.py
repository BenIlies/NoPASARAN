import http.client
import ssl
import logging

from nopasaran.decorators import parsing_decorator


class HTTPSimpleClientPrimitives:
    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def request_by_ip(inputs, outputs, state_machine):
        """
        Make an HTTP or HTTPS request to a given IP address using a specified hostname.

        Number of input arguments: 3
            - IP address (str)
            - Hostname (str)
            - use_https (str): "1" for HTTPS, "0" for HTTP

        Number of output arguments: 1
            - A dictionary containing the result and any logged errors

        Args:
            inputs (List[str]): [ip_address, hostname, use_https]
            outputs (List[str]): [result_var_name]
            state_machine: The state machine object.

        Returns:
            None
        """
        ip_address = state_machine.get_variable_value(inputs[0])
        hostname = state_machine.get_variable_value(inputs[1])
        use_https = state_machine.get_variable_value(inputs[2])

        results = {}
        errors = []

        scheme = "UNKNOWN"

        try:
            if use_https == "1":
                scheme = "HTTPS"
                context = ssl._create_unverified_context()
                conn = http.client.HTTPSConnection(ip_address, 443, context=context, timeout=5)
            elif use_https == "0":
                scheme = "HTTP"
                conn = http.client.HTTPConnection(ip_address, 80, timeout=5)
            else:
                error_msg = "use_https must be '1' for HTTPS or '0' for HTTP"
                logging.debug(error_msg)
                errors.append(error_msg)
                conn = None

            if conn:
                headers = {"Host": hostname}
                path = "/"

                conn.request("GET", path, headers=headers)
                response = conn.getresponse()
                body = response.read(300).decode(errors='replace')  # Truncate body to 300 bytes

                results[scheme] = {
                    'status': response.status,
                    'reason': response.reason,
                    'body': body
                }

                conn.close()
        except Exception as e:
            error_msg = f"{scheme} request failed: {e}"
            logging.debug(error_msg)
            errors.append(error_msg)

        output_value = {
            "results": results,
            "errors": errors
        }

        state_machine.set_variable_value(outputs[0], output_value)