from nopasaran.decorators import parsing_decorator
import nopasaran.utils as utils

class MTUPrimitives:
    """
    Class containing MTU action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def get_MTU(inputs, outputs, state_machine):
        """
        Get the system's default MTU.

        Number of input arguments: 0
        Number of output arguments: 1

        Args:
            inputs (List[str]): Empty list.
            outputs (List[str]): List with one element—the name of the variable to store the default MTU.
            state_machine: The state machine object.
        """
        mtu_value = utils.get_default_mtu()
        state_machine.set_variable_value(outputs[0], mtu_value)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set_IP_df(inputs, outputs, state_machine):
        """
        Set the Don't Fragment (DF) flag on an IP packet.

        Number of input arguments: 1
            inputs[0]: The variable name for the IP packet.
        Number of output arguments: 1
            outputs[0]: The variable name to store the updated IP packet.
        """
        packet = state_machine.get_variable_value(inputs[0])
        updated_packet = utils.set_IP_df(packet)
        state_machine.set_variable_value(outputs[0], updated_packet)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_ICMP_payload(inputs, outputs, state_machine):
        """
        Set/replace the payload of an existing ICMP packet.

        Number of input arguments: 2
            inputs[0]: The variable name for the ICMP packet.
            inputs[1]: The variable name for the payload bytes.
        Number of output arguments: 1
            outputs[0]: The variable name to store the updated packet.
        """
        packet = state_machine.get_variable_value(inputs[0])
        payload_bytes = state_machine.get_variable_value(inputs[1])
        updated_packet = utils.set_ICMP_payload(packet, payload_bytes)
        state_machine.set_variable_value(outputs[0], updated_packet)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_ICMP_packet_bytes(inputs, outputs, state_machine):
        """
        Attach a payload of repeated 'A' characters to an ICMP packet.

        Number of input arguments: 2
            inputs[0]: The variable name for the ICMP packet.
            inputs[1]: The size (number of bytes) to fill with 'A'. 
                    (Can be an int, a string like "80", or bytes like b'80'.)
        Number of output arguments: 1
            outputs[0]: The variable name to store the updated packet.
        """
        # Retrieve packet and size from the state machine
        packet = state_machine.get_variable_value(inputs[0])
        size_val = state_machine.get_variable_value(inputs[1])

        # Convert size_val into an integer
        if isinstance(size_val, int):
            size = size_val
        elif isinstance(size_val, bytes):
            size = int(size_val.decode())
        elif isinstance(size_val, str):
            size = int(size_val)
        else:
            raise TypeError(f"Unsupported type for size: {type(size_val)}. Must be int, str, or bytes.")

        # Pass the final integer size to the utility function
        updated_packet = utils.set_ICMP_packet_bytes(packet, size)

        # Store the updated packet back into the state machine’s variable
        state_machine.set_variable_value(outputs[0], updated_packet)

 
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
    def set_UDP_packet_bytes(inputs, outputs, state_machine):
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
