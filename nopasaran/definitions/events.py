from enum import Enum


class EventNames(Enum):
    """
    Enum representing event names.
    
    This enum represents different event names.
    """

    STARTED = 0
    SYNC = 1
    PACKET_SENT = 2
    PACKET_AVAILABLE = 3
    DONE = 4
    ERROR = 5
    TIMEOUT = 6
    READY = 7
    SYNC_SENT = 8
    SYNC_AVAILABLE = 9
    CONNECTION_ENDING = 10
