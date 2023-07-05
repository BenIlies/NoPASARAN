from enum import Enum


class Command(Enum):
    """
    Enum representing commands.
    
    This enum represents different commands used in state transitions.
    """

    EXECUTE_ACTION = 0
    ASSIGN_VARIABLES = 1
    SET_STATE = 2
