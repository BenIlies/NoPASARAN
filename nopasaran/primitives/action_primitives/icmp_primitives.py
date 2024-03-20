import nopasaran.utils as utils
from nopasaran.decorators import parsing_decorator

class ICMPPrimitives:
    """
    Class containing ICMP action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_ICMP_packet(inputs, outputs, state_machine):
        """
        Create an ICMP packet and store it in an output variable in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. This method does not use input variables.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the created ICMP packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.create_ICMP_packet())

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_ICMP_payload(inputs, outputs, state_machine):
        """
        Extract the ICMP payload and store it in an output variable in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory output argument, which is
                the variable containing the ICMP packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the extracted ICMP payload.

            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.get_ICMP_payload(state_machine.get_variable_value(inputs[0])))
