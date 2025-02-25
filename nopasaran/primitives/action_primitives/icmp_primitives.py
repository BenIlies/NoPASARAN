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

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_ICMP_type(inputs, outputs, state_machine):
        """
        Set the type field of an ICMP packet.

        Number of input arguments: 2
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): Contains two mandatory input arguments:
                - The name of the variable containing the ICMP packet.
                - The name of the variable containing the type value to set.
            outputs (List[str]): Contains one mandatory output argument to store the modified ICMP packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_ICMP_type(
            state_machine.get_variable_value(outputs[0]),
            state_machine.get_variable_value(inputs[1])
        )


    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_ICMP_code(inputs, outputs, state_machine):
        """
        Set the code field of an ICMP packet.

        Number of input arguments: 2
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): Contains two mandatory input arguments:
                - The name of the variable containing the ICMP packet.
                - The name of the variable containing the code value to set.
            outputs (List[str]): Contains one mandatory output argument to store the modified ICMP packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_ICMP_code(
            state_machine.get_variable_value(outputs[0]),
            state_machine.get_variable_value(inputs[1])
        )


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_ICMP_type(inputs, outputs, state_machine):
            """
            Get the type field from an ICMP packet.

            Number of input arguments: 1
            Number of output arguments: 1
            Optional input arguments: No
            Optional output arguments: No

            Args:
                inputs (List[str]): Contains one mandatory input argument:
                    - The name of the variable containing the ICMP packet.
                outputs (List[str]): Contains one mandatory output argument to store the type value.
                state_machine: The state machine object.

            Returns:
                None
            """
            icmp_type = utils.get_ICMP_type(state_machine.get_variable_value(inputs[0]))
            state_machine.set_variable_value(outputs[0], icmp_type)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_ICMP_code(inputs, outputs, state_machine):
            """
            Get the code field from an ICMP packet.

            Number of input arguments: 1
            Number of output arguments: 1
            Optional input arguments: No
            Optional output arguments: No

            Args:
                inputs (List[str]): Contains one mandatory input argument:
                    - The name of the variable containing the ICMP packet.
                outputs (List[str]): Contains one mandatory output argument to store the code value.
                state_machine: The state machine object.

            Returns:
                None
            """
            icmp_code = utils.get_ICMP_code(state_machine.get_variable_value(inputs[0]))
            state_machine.set_variable_value(outputs[0], icmp_code)

