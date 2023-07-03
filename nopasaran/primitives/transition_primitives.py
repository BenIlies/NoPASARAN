from nopasaran.decorators import parsing_decorator

class TransitionPrimitives:
    OLD_STATE_KEY = "old-state"
    NEW_STATE_KEY = "new-state"

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def assign(inputs, outputs, trans_tmp_dict):
        trans_tmp_dict[TransitionPrimitives.NEW_STATE_KEY][outputs[0]] = trans_tmp_dict[TransitionPrimitives.OLD_STATE_KEY][inputs[0]]