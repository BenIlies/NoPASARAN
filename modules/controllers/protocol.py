import codecs
import json
import logging
import pickle

from twisted.internet.protocol import Protocol
from twisted.internet.threads import deferToThread

from modules.controllers.messages import JSONLOGMessage, NodeReplyStatus, ProxyReplyStatus, JSONMessage
from modules.utils import get_packet_info

class NodeProtocol(Protocol):
    connected_to_peer = False

    def connectionMade(self):
        self.status = None
        init_msg = json.dumps({JSONMessage.STATUS.name: NodeReplyStatus.INIT_REQ.name}).encode()
        self.transport.write(init_msg)
        
    def dataReceived(self, encoded_json_data):
        data = json.loads(encoded_json_data.decode())
        if JSONMessage.STATUS.name in data:
            status = data[JSONMessage.STATUS.name]
            if status in [e.name for e in ProxyReplyStatus]:
                content = None
                if status == ProxyReplyStatus.INIT_ACK.name:
                    content = {JSONMessage.STATUS.name: NodeReplyStatus.LINK_ID_REQ.name, JSONMessage.PARAMETERS.name: self.factory.link_id}
                elif status == ProxyReplyStatus.LINK_ID_REF.name:
                    self.transport.loseConnection()
                elif status == ProxyReplyStatus.PEER_DISCONNECTED.name:
                    self.connected_to_peer = False
                self.status = status
                if content != None:
                    answer = json.dumps(content).encode()
                    self.transport.write(answer)     
        if self.status == ProxyReplyStatus.PEER_CONNECTED.name:
            if not self.connected_to_peer:
                self.connected_to_peer = True
                deferred_state_machine = deferToThread(self.factory.state_machine.start, self)
        if JSONMessage.LOG.name in data:
            if data[JSONMessage.LOG.name] == JSONLOGMessage.SENT.name:
                logging.info('REMOTE SENT ' + get_packet_info(pickle.loads(codecs.decode(data[JSONMessage.PARAMETERS.name].encode(), "base64"))))
            elif data[JSONMessage.LOG.name] == JSONLOGMessage.RECEIVED.name:
                logging.info('REMOTE RECEIVED ' + get_packet_info(pickle.loads(codecs.decode(data[JSONMessage.PARAMETERS.name].encode(), "base64"))))
        print("Status: ", self.status)
        print("Received:", data)

    def connectionLost(self, reason):
        self.factory.connectionLost(reason)

class ProxyProtocol(Protocol):
    clients = {}

    def connectionMade(self):
        self.clients[self] = None
        
    def dataReceived(self, encoded_json_data):
        data = json.loads(encoded_json_data.decode())
        if JSONMessage.STATUS.name in data:
            status = data[JSONMessage.STATUS.name]
            if status in [e.name for e in NodeReplyStatus]:
                content = None
                if status == NodeReplyStatus.INIT_REQ.name:
                    content = {JSONMessage.STATUS.name: ProxyReplyStatus.INIT_ACK.name}
                elif status == NodeReplyStatus.LINK_ID_REQ.name:
                    if len([key for key, value in self.clients.items() if value == data[JSONMessage.PARAMETERS.name]]) in [0,1]:
                        self.clients[self] = data[JSONMessage.PARAMETERS.name]
                        self.transport.write(json.dumps({JSONMessage.STATUS.name: ProxyReplyStatus.LINK_ID_ACK.name}).encode())
                        if len([key for key, value in self.clients.items() if value == self.clients[self]]) == 2:
                            for connected_peer in [key for key, value in self.clients.items() if value == self.clients[self]]:
                                connected_peer.transport.write(json.dumps({JSONMessage.STATUS.name: ProxyReplyStatus.PEER_CONNECTED.name}).encode())
                    else: 
                        self.transport.write(json.dumps({JSONMessage.STATUS.name: ProxyReplyStatus.LINK_ID_REF.name}).encode()) 
                        self.transport.loseConnection()
                self.status = status
                if content != None:
                    answer = json.dumps(content).encode()
                    self.transport.write(answer)     
        if JSONMessage.LOG.name in data:
            recipients = [key for key, value in self.clients.items() if value == self.clients[self] and key != self and value != None]
            for recipient in recipients:
                recipient.transport.write(encoded_json_data)
        print("Received:", data)

    def connectionLost(self, reason):
        self.factory.connectionLost(reason)
        for connected_peer in [key for key, value in self.clients.items() if value == self.clients[self] and key != self and value != None]:
            connected_peer.transport.write(json.dumps({JSONMessage.STATUS.name: ProxyReplyStatus.PEER_DISCONNECTED.name}).encode())
        self.clients.pop(self)