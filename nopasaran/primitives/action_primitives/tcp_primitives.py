import nopasaran.utils as utils
from nopasaran.decorators import parsing_decorator


class TCPPrimitives:
    """
    Class containing TCP action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_TCP_packet(inputs, outputs, state_machine):
        """
        Create a TCP packet and store it in an output variable in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the created TCP packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.create_TCP_packet())

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_sport(inputs, outputs, state_machine):
        """
        Set the source port of a TCP packet in the machine's state.

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
        utils.set_TCP_sport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_dport(inputs, outputs, state_machine):
        """
        Set the destination port of a TCP packet in the machine's state.

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
        utils.set_TCP_dport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_seq(inputs, outputs, state_machine):
        """
        Set the sequence number of a TCP packet in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new sequence number value and the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modified packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_seq(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_TCP_flags(inputs, outputs, state_machine):
        """
        Get the TCP flags from a TCP packet in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the TCP flags.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.get_TCP_flags(state_machine.get_variable_value(inputs[0])[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_flags(inputs, outputs, state_machine):
        """
        Set the TCP flags of a TCP packet in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new TCP flags value and the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modified TCP flags.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_flags(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_ack(inputs, outputs, state_machine):
        """
        Set the acknowledgment number of a TCP packet in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new acknowledgment number value and the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modified acknowledgment number.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_ack(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_payload(inputs, outputs, state_machine):
        """
        Set the payload of a TCP packet in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new payload value and the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modified payload.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_payload(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def remove_TCP_payload(inputs, outputs, state_machine):
        """
        Remove the payload from a TCP packet in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the payload removed.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.remove_TCP_payload(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set_TCP_automatic_packet_seq(inputs, outputs, state_machine):
        """
        Set the sequence number of a TCP packet in the machine's state to an automatically generated value.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the automatically generated sequence number.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_automatic_packet_seq(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_automatic_packet_ack(inputs, outputs, state_machine):
        """
        Set the acknowledgment number of a TCP packet in the machine's state to an automatically generated value.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the new acknowledgment number value, the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the automatically generated acknowledgment number.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_automatic_packet_ack(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1])[0])