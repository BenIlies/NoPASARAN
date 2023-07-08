import nopasaran.utils as utils
from nopasaran.decorators import parsing_decorator


class IPPrimitives:
    """
    Class containing IP action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_src(inputs, outputs, state_machine):
        """
        Set the source IP address of a packet in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new IP address and the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modified packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_IP_src(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_dst(inputs, outputs, state_machine):
        """
        Set the destination IP address of a packet in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new IP address and the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modified packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_IP_dst(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_packet_IP(inputs, outputs, state_machine):
        """
        Get the source IP address from a packet in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the source IP address.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.get_IP_src(state_machine.get_variable_value(inputs[0])[0]))