from enum import Enum

class EventNames(Enum):
    STARTED = 0
    SYNC = 1
    PACKET_SENT = 2
    PACKET_AVAILABLE = 3
    DONE = 4
    TIMEOUT = 5
    READY = 6
    SYNC_SENT = 7
    SYNC_AVAILABLE = 8
