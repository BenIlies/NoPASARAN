from nopasaran.interpreters.interpreter import Interpreter
from nopasaran.primitives.action_primitives.action_primitives import ActionPrimitives


class ActionInterpreter(Interpreter):
    """
    A custom ActionInterpreter class that inherits from Interpreter.
    This class interprets actions in the context of a command-line interface.
    """

    @classmethod
    def evaluate(cls, line, state_variables):
        """
        Evaluate the action line using the provided state variables.

        Args:
            line (str): The action line to evaluate.
            state_variables: The state variables to use during evaluation.

        Returns:
            The result of the evaluation.
        """
        action_primitives = ActionPrimitives()
        super().evaluate(line, state_variables, action_primitives)
