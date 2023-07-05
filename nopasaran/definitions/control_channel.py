from enum import Enum


class JSONMessage(Enum):
    """
    Enum representing JSON messages.
    
    This enum represents different types of JSON messages.
    """

    STATUS = 0
    SYNC = 1


class Status(Enum):
    """
    Enum representing status values.
    
    This enum represents different status values.
    """

    DISCONNECTED = 0
    CONNECTED = 1
    READY = 2
    DISCONNECTING = 3


class Configuration(Enum):
    """
    Enum representing configuration values.
    
    This enum represents different configuration values.
    """

    ROOT_CERTIFICATE = 0
    PRIVATE_CERTIFICATE = 1
    DESTINATION_IP = 2
    SERVER_PORT = 3
