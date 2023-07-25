from nopasaran.decorators import parsing_decorator

class IPPrimitives:
    """
    Class containing IP action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_src(inputs, outputs, state_machine):
        """
        Set the source IP address of an IP packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the IP packet.
                - The name of the variable containing the source IP address to set.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified IP packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        ip_packet = state_machine.get_variable_value(inputs[0])
        src_ip = state_machine.get_variable_value(inputs[1])

        ip_packet['IP'].src = src_ip

        state_machine.set_variable_value(outputs[0], ip_packet)


    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_dst(inputs, outputs, state_machine):
        """
        Set the destination IP address of an IP packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the IP packet.
                - The name of the variable containing the destination IP address to set.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified IP packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        ip_packet = state_machine.get_variable_value(inputs[0])
        dst_ip = state_machine.get_variable_value(inputs[1])

        ip_packet['IP'].dst = dst_ip

        state_machine.set_variable_value(outputs[0], ip_packet)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_IP_src(inputs, outputs, state_machine):
        """
        Get the source IP address from an IP packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the IP packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the source IP address.

            state_machine: The state machine object.

        Returns:
            None
        """
        ip_packet = state_machine.get_variable_value(inputs[0])
        src_ip = ip_packet['IP'].src

        state_machine.set_variable_value(outputs[0], src_ip)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_IP_dst(inputs, outputs, state_machine):
        """
        Get the destination IP address from an IP packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the IP packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the destination IP address.

            state_machine: The state machine object.

        Returns:
            None
        """
        ip_packet = state_machine.get_variable_value(inputs[0])
        dst_ip = ip_packet['IP'].dst

        state_machine.set_variable_value(outputs[0], dst_ip)


    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_ttl(inputs, outputs, state_machine):
        """
        Set the TTL (Time To Live) value of an IP packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the IP packet.
                - The name of the variable containing the TTL value to set.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the modified IP packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        ip_packet = state_machine.get_variable_value(inputs[0])
        ttl_value = state_machine.get_variable_value(inputs[1])

        ip_packet['IP'].ttl = ttl_value

        state_machine.set_variable_value(outputs[0], ip_packet)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_IP_ttl(inputs, outputs, state_machine):
        """
        Get the TTL (Time To Live) value from an IP packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the IP packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the TTL value.

            state_machine: The state machine object.

        Returns:
            None
        """
        ip_packet = state_machine.get_variable_value(inputs[0])
        ttl_value = ip_packet['IP'].ttl

        state_machine.set_variable_value(outputs[0], ttl_value)
