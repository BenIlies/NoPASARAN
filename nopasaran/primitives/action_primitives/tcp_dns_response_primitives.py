from nopasaran.decorators import parsing_decorator
from nopasaran.tools.tcp_dns_socket_server import TCPDNSSocketServer

class TCPDNSResponsePrimitives:

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_tcp_dns_server(inputs, outputs, state_machine):
        server = TCPDNSSocketServer()
        state_machine.set_variable_value(outputs[0], server)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def start_tcp_dns_server(inputs, outputs, state_machine):
        server = state_machine.get_variable_value(inputs[0])
        listening_ip = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))
        server.start(listening_ip, port)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=1)
    def wait_and_respond_tcp_dns_query(inputs, outputs, state_machine):
        """
        Wait for a DNS query and respond based on provided spec.
        Inputs: [server_instance, port, timeout, response_spec]
        Outputs: [result_dict]
        Example response_spec:
        {"type": "CNAME", "value": "safe.com", "qname": "blocked.com."}
        """
        server = state_machine.get_variable_value(inputs[0])
        timeout = int(state_machine.get_variable_value(inputs[2]))
        response_spec = state_machine.get_variable_value(inputs[3])

        result, _ = server.wait_for_query(timeout, response_spec)
        state_machine.set_variable_value(outputs[0], result)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def close_tcp_dns_server(inputs, outputs, state_machine):
        server = state_machine.get_variable_value(inputs[0])
        server.close()
