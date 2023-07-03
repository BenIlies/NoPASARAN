from enum import Enum

class JSONMessage(Enum):
    STATUS = 0
    SYNC = 1

class Status(Enum):
    DISCONNECTED = 0
    CONNECTED = 1
    READY = 2
    DISCONNECTING = 3

class Configuration(Enum):
    ROOT_CERTIFICATE = 0
    PRIVATE_CERTIFICATE = 1
    DESTINATION_IP = 2
    SERVER_PORT = 3
    