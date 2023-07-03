from nopasaran.interpreters.interpreter import Interpreter
from nopasaran.primitives.transition_primitives import TransitionPrimitives

class TransitionInterpreter(Interpreter):
    """
    A custom TransitionInterpreter class that inherits from Interpreter.
    This class interprets transitions in the context of a command-line interface.
    """

    OLD_STATE_KEY = TransitionPrimitives.OLD_STATE_KEY
    NEW_STATE_KEY = TransitionPrimitives.NEW_STATE_KEY

    @classmethod
    def evaluate(cls, line, trans_tmp_dict):
        super().evaluate(line, trans_tmp_dict, TransitionPrimitives)
