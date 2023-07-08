from nopasaran.interpreters.interpreter import Interpreter
from nopasaran.primitives.condition_primitives.condition_primitives import ConditionPrimitives


class ConditionInterpreter(Interpreter):
    """
    A custom ConditionInterpreter class that inherits from Interpreter.
    This class interprets conditions in the context of a command-line interface.
    """

    @classmethod
    def evaluate(cls, line, state_variables):
        """
        Evaluate the condition line using the provided state variables.

        Args:
            line (str): The condition line to evaluate.
            state_variables: The state variables to use during evaluation.

        Returns:
            The result of the evaluation.
        """
        condition_primitives = ConditionPrimitives()
        return super().evaluate(line, state_variables, condition_primitives)
