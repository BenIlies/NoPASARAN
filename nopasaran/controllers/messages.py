from enum import Enum

class JSONMessage(Enum):
    STATUS = 0
    SYNC = 1

class Status(Enum):
    DISCONNECTED = 0
    CONNECTED = 1
    READY = 2
    DISCONNECTING = 3