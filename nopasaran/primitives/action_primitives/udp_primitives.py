import nopasaran.utils as utils
from nopasaran.decorators import parsing_decorator


class UDPPrimitives:
    """
    Class containing UDP action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_UDP_packet(inputs, outputs, state_machine):
        """
        Create a UDP packet and store it in an output variable in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the created UDP packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.create_UDP_packet())

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_sport(inputs, outputs, state_machine):
        """
        Set the source port of a UDP packet in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new source port value and the name of a variable representing the packet.
           
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modified packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_UDP_sport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_dport(inputs, outputs, state_machine):
        """
        Set the destination port of a UDP packet in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new destination port value and the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modified packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_UDP_dport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))