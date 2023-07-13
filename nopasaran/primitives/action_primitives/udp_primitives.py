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

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the created UDP packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        udp_packet = UDP()
        state_machine.set_variable_value(outputs[0], udp_packet)


    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_sport(inputs, outputs, state_machine):
        """
        Set the source port of a UDP packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the UDP packet.
                - The name of the variable containing the source port to set.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified UDP packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        udp_packet = state_machine.get_variable_value(inputs[0])
        sport = state_machine.get_variable_value(inputs[1])

        udp_packet.sport = sport

        state_machine.set_variable_value(outputs[0], udp_packet)


    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_dport(inputs, outputs, state_machine):
        """
        Set the destination port of a UDP packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the UDP packet.
                - The name of the variable containing the destination port to set.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified UDP packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        udp_packet = state_machine.get_variable_value(inputs[0])
        dport = state_machine.get_variable_value(inputs[1])

        udp_packet.dport = dport

        state_machine.set_variable_value(outputs[0], udp_packet)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_UDP_sport(inputs, outputs, state_machine):
        """
        Get the source port from a UDP packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the UDP packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the source port.

            state_machine: The state machine object.

        Returns:
            None
        """
        udp_packet = state_machine.get_variable_value(inputs[0])
        sport = udp_packet.sport

        state_machine.set_variable_value(outputs[0], sport)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_UDP_dport(inputs, outputs, state_machine):
        """
        Get the destination port from a UDP packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the UDP packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the destination port.

            state_machine: The state machine object.

        Returns:
            None
        """
        udp_packet = state_machine.get_variable_value(inputs[0])
        dport = udp_packet.dport

        state_machine.set_variable_value(outputs[0], dport)
