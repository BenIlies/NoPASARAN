from enum import Enum


class StateDuringTransition(Enum):
    """
    Enum representing state during transition.
    
    This enum represents the states during a transition, including the old state and the new state.
    """

    OLD_STATE = 0
    NEW_STATE = 1
