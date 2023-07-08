from nopasaran.decorators import parsing_decorator
from nopasaran.definitions.transitions import StateDuringTransition

class VariableAssignmentTransitions:
    """
    Class containing methods for assigning variables during state transitions in a state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def assign(inputs, outputs, trans_tmp_dict):
        """
        Assign the value of an input variable from the old state to an output variable in the new state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable in the old state to be assigned.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable in the new state to be assigned.
            
            trans_tmp_dict (dict): The dictionary containing the temporary variables during the transition.

        Returns:
            None
        """
        trans_tmp_dict[StateDuringTransition.NEW_STATE.name][outputs[0]] = trans_tmp_dict[StateDuringTransition.OLD_STATE.name][inputs[0]]