from enum import Enum


class NodeReplyStatus(Enum):
    INIT_REQ = 0
    LINK_ID_REQ = 1

class ProxyReplyStatus(Enum):
    INIT_ACK = 0
    LINK_ID_ACK = 1
    LINK_ID_REF = 2
    PEER_CONNECTED = 3
    PEER_DISCONNECTED = 4

class JSONMessage(Enum):
    STATUS = 0
    LOG = 1
    PARAMETERS = 2

class JSONLOGMessage(Enum):
    RECEIVED = 0
    SENT = 1