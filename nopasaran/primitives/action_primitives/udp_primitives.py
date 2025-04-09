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
        state_machine.set_variable_value(outputs[0], utils.create_UDP_packet())


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
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_UDP_sport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))


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
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_UDP_dport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

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
        sport = udp_packet['UDP'].sport

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
        dport = udp_packet['UDP'].dport

        state_machine.set_variable_value(outputs[0], dport)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_payload(inputs, outputs, state_machine):
        """
        Set/replace the payload of an existing UDP packet.

        Number of input arguments: 2
            inputs[0]: The variable name for the UDP packet.
            inputs[1]: The variable name for the payload bytes.
        Number of output arguments: 1
            outputs[0]: The variable name to store the updated packet.
        """
        packet = state_machine.get_variable_value(inputs[0])
        payload_bytes = state_machine.get_variable_value(inputs[1])
        # Update the payload in place
        utils.set_UDP_payload(packet, payload_bytes)
        # Now store the (updated) packet in the output variable.
        state_machine.set_variable_value(outputs[0], packet)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def fill_UDP_packet_with_placeholder (inputs, outputs, state_machine):
        """
        Attach a payload of repeated 'A' characters to a UDP packet.

        Number of input arguments: 2
            inputs[0]: The variable name for the UDP packet.
            inputs[1]: The size (number of bytes) to fill with 'A'.
        Number of output arguments: 1
            outputs[0]: The variable name to store the updated packet.
        """
        packet = state_machine.get_variable_value(inputs[0])
        size = state_machine.get_variable_value(inputs[1])
        # Update the packet's payload using the utility function.
        utils.set_UDP_packet_bytes(packet, size)
        state_machine.set_variable_value(outputs[0], packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_UDP_payload_size(inputs, outputs, state_machine):
        """
        Get the size (in bytes) of the UDP payload from a UDP packet.

        Number of input arguments: 1
            inputs[0]: The variable name for the UDP packet.
        Number of output arguments: 1
            outputs[0]: The variable name to store the UDP payload size.
        """
        packet = state_machine.get_variable_value(inputs[0])
        payload_size = utils.get_UDP_payload_size(packet)
        state_machine.set_variable_value(outputs[0], payload_size)
