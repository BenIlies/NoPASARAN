from nopasaran.definitions.events import EventNames
from nopasaran.decorators import parsing_decorator


class EventPrimitives:
    """
    Class containing event primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def trigger(inputs, outputs, state_machine):
        """
        Generate an event with a given name based on a local state variable.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the event to trigger.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.trigger_event(state_machine.get_variable_value(inputs[0]))

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0)
    def done(inputs, outputs, state_machine):
        """
        Triggers the event DONE when executed.

        Number of input arguments: 0

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names.

            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.trigger_event(EventNames.DONE.name)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def redirect(inputs, outputs, state_machine):
        """
        Redirect an event to a specific target state when triggered within the state machine.
        This primitive allows you to define a redirection rule for events, specifying the name of the event
        as the first mandatory input argument and the target state as the second mandatory input argument.

        Number of input arguments: 2

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the name of the event to redirect and the name of the target state.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.add_redirection(inputs[0], inputs[1])