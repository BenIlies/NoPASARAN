from nopasaran.interpreters.interpreter import Interpreter
from nopasaran.primitives.condition_primitives import ConditionPrimitives


class ConditionInterpreter(Interpreter):
    """
    A custom ConditionInterpreter class that inherits from Interpreter.
    This class interprets conditions in the context of a command-line interface.
    """

    @classmethod
    def evaluate(cls, line, state_variables):
        return super().evaluate(line, state_variables, ConditionPrimitives)
