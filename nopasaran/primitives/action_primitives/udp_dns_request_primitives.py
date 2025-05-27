from nopasaran.decorators import parsing_decorator
from nopasaran.definitions.events import EventNames
import nopasaran.utils as utils

class UDPDNSRequestPrimitives:
    @staticmethod
    @parsing_decorator(input_args=4, output_args=1)
    def make_udp_dns_query(inputs, outputs, state_machine):
        """
        Make a DNS query over UDP with user-defined domain and query type.
        inputs: [domain, query_type, server_ip, server_port]
        outputs: [dns_response_dict]
        """
        domain = state_machine.get_variable_value(inputs[0])
        query_type = state_machine.get_variable_value(inputs[1])
        server_ip = state_machine.get_variable_value(inputs[2])
        server_port = int(state_machine.get_variable_value(inputs[3]))

        # Call utility function with provided parameters
        result = utils.send_udp_dns_query(server_ip, server_port, domain, query_type)

        # Store result and trigger events accordingly
        if not result or result.get("response") is None:
            state_machine.set_variable_value(outputs[0], {"received": None})
            state_machine.trigger_event(EventNames.REQUEST_ERROR.name)
        else:
            state_machine.set_variable_value(outputs[0], {"received": result})
            state_machine.trigger_event(EventNames.RESPONSE_RECEIVED.name)

