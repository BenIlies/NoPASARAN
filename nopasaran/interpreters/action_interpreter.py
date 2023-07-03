from nopasaran.interpreters.interpreter import Interpreter
from nopasaran.primitives.action_primitives import ActionPrimitives

class ActionInterpreter(Interpreter):
    """
    A custom ActionInterpreter class that inherits from Interpreter.
    This class interprets actions in the context of a command-line interface.
    """

    @classmethod
    def evaluate(cls, line, state_variables):
        super().evaluate(line, state_variables, ActionPrimitives)
