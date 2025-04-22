from nopasaran.decorators import parsing_decorator
from nopasaran.definitions.events import EventNames
import nopasaran.utils as utils


class ClientEchoPrimitives:

    """
    Class containing Echo client action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=4, output_args=1)
    def make_tcp_echo_request(inputs, outputs, state_machine):
        """
        Make a one-shot TCP echo request.

        Number of input arguments: 4
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains four mandatory input arguments:
                - The name of the variable containing the IP address.
                - The name of the variable containing the port number.
                - The name of the variable containing the message to be echoed.
                - The name of the variable containing the timeout duration.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the echoed response (or None).
            state_machine: The state machine object.

        Returns:
            None
        """
        ip = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        message = state_machine.get_variable_value(inputs[2])
        timeout = float(state_machine.get_variable_value(inputs[3]))

        response = utils.send_echo_once_tcp(ip, port, message, timeout)

        if response is not None:
            state_machine.trigger_event(EventNames.RESPONSE_RECEIVED.name)
        else:
            state_machine.trigger_event(EventNames.REQUEST_ERROR.name)

        state_machine.set_variable_value(outputs[0], response)

    @staticmethod
    @parsing_decorator(input_args=4, output_args=1)
    def make_udp_echo_request(inputs, outputs, state_machine):
        """
        Make a one-shot UDP echo request.

        Number of input arguments: 4
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains four mandatory input arguments:
                - The name of the variable containing the IP address.
                - The name of the variable containing the port number.
                - The name of the variable containing the message to be echoed.
                - The name of the variable containing the timeout duration.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the echoed response (or None).
            state_machine: The state machine object.

        Returns:
            None
        """
        ip = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        message = state_machine.get_variable_value(inputs[2])
        timeout = float(state_machine.get_variable_value(inputs[3]))

        response = utils.send_echo_once_udp(ip, port, message, timeout)

        if response is not None:
            state_machine.trigger_event(EventNames.RESPONSE_RECEIVED.name)
        else:
            state_machine.trigger_event(EventNames.REQUEST_ERROR.name)

        state_machine.set_variable_value(outputs[0], response)
