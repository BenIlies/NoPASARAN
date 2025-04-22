from nopasaran.decorators import parsing_decorator
import nopasaran.utils as utils
from nopasaran.definitions.events import EventNames

class HTTPS1RequestPrimitives:
    """
    Class containing HTTPS/1.1 action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=4, output_args=1)
    def make_https_1_sni_request(inputs, outputs, state_machine):
        """
        Make an HTTPS/1.1 request using the request packet and optional SNI.

        Number of input arguments: 4
            - The request packet
            - The IP address to connect to
            - The port to connect to
            - The SNI (Server Name Indication); 

        Number of output arguments: 1
            - The HTTPS response

        Args:
            inputs (List[str]): The list of input variable names. It contains four mandatory input arguments:
                - The name of the variable containing the request packet.
                - The name of the variable containing the IP address or hostname.
                - The name of the variable containing the port number.
                - The name of the variable containing the SNI string.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the HTTPS response.

            state_machine: The state machine object.

        Returns:
            None
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
