from nopasaran.primitives.primitives import Primitives
from nopasaran.primitives.transition_primitives.assignment_transitions import VariableAssignmentTransitions

class TransitionPrimitives(Primitives):
    """
    Class containing transition primitives for the state machine.
    """
    classes = [VariableAssignmentTransitions]
