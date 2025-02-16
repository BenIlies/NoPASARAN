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

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): This should be an empty list since there are no input arguments.

            outputs (List[str]): The list of output variable names. It contains one mandatory 
                output argument, which is the name of the variable to store the default MTU.

            state_machine: The state machine object.

        Returns:
            None
        """
        # Call the utility function that retrieves the default MTU.
        mtu_value = utils.get_default_mtu()

        # Store the MTU value in the specified output variable.
        state_machine.set_variable_value(outputs[0], mtu_value)
