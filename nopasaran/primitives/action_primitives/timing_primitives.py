import time
from nopasaran.decorators import parsing_decorator

class TimingPrimitives:
    """
    Class containing timing action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def wait(inputs, outputs, state_machine):
        """
        Wait for a specified number of seconds.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                which is the number of seconds to wait (float).

            outputs (List[str]): The list of output variable names. (None for this method)

            state_machine: The state machine object.

        Returns:
            None
        """
        seconds = float(state_machine.get_variable_value(inputs[0]))
        time.sleep(seconds)