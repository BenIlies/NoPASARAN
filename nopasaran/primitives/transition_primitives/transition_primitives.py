from nopasaran.primitives.primitives import Primitives
from nopasaran.primitives.transition_primitives.assignment_transition_primitives import AssignmentTransitionPrimitives

class TransitionPrimitives(Primitives):
    """
    Class containing transition primitives for the state machine.
    """
    classes = [AssignmentTransitionPrimitives]
