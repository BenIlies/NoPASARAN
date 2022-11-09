from enum import Enum

class JSONMessage(Enum):
    STATUS = 0
    LOG = 1
    PARAMETERS = 2
    SYNC = 3

class JSONLOGMessage(Enum):
    RECEIVED = 0
    SENT = 1

class Status(Enum):
    DISCONNECTED = 0
    CONNECTED = 1
    READY = 2
    DISCONNECTING = 3