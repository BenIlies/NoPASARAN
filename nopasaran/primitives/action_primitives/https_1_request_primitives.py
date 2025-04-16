from nopasaran.decorators import parsing_decorator
import nopasaran.utils  as utils
from nopasaran.definitions.events import EventNames

class HTTPS1RequestPrimitives:
    """
    Class containing HTTPS/1.1 action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=4, output_args=1)
    def make_https_1_sni_request(inputs, outputs, state_machine):
        """
        Make an HTTPS/1.1 request using a raw request packet with optional SNI.

        Input Args:
            - request_packet (bytes)
            - ip (str)
            - port (int)
            - sni (str, can be empty string)

        Output:
            - response (bytes)
        """
        request_packet = state_machine.get_variable_value(inputs[0])
        ip = state_machine.get_variable_value(inputs[1])
        port = int(state_machine.get_variable_value(inputs[2]))
        sni = state_machine.get_variable_value(inputs[3]) or None

        response = utils.send_https_sni_request(ip, port, request_packet, sni)

        state_machine.set_variable_value(outputs[0], response)

        if response is not None:
            state_machine.trigger_event(EventNames.RESPONSE_RECEIVED.name)
        else:
            state_machine.trigger_event(EventNames.REQUEST_ERROR.name)
