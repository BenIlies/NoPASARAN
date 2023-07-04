from nopasaran.decorators import parsing_decorator
from nopasaran.definitions.transitions import StateDuringTransition

class TransitionPrimitives:

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def assign(inputs, outputs, trans_tmp_dict):
        trans_tmp_dict[StateDuringTransition.NEW_STATE.name][outputs[0]] = trans_tmp_dict[StateDuringTransition.OLD_STATE.name][inputs[0]]