from nopasaran.interpreters.interpreter import Interpreter
from nopasaran.primitives.transition_primitives.transition_primitives import TransitionPrimitives


class TransitionInterpreter(Interpreter):
    """
    A custom TransitionInterpreter class that inherits from Interpreter.
    This class interprets transitions in the context of a command-line interface.
    """

    @classmethod
    def evaluate(cls, line, trans_tmp_dict):
        """
        Evaluate the transition line using the provided transition temporary dictionary.

        Args:
            line (str): The transition line to evaluate.
            trans_tmp_dict: The transition temporary dictionary to use during evaluation.

        Returns:
            The result of the evaluation.
        """
        transition_primitives = TransitionPrimitives()
        super().evaluate(line, trans_tmp_dict, transition_primitives)
