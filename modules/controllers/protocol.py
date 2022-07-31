import codecs
import json
import logging
import pickle

from twisted.internet.protocol import Protocol
from twisted.internet.threads import deferToThread

from modules.controllers.messages import JSONLOGMessage, JSONMessage, Status
from modules.utils import get_packet_info

class NodeClientProtocol(Protocol):
    remote_status = Status.DISCONNECTED.name
    local_status = Status.DISCONNECTED.name

    def get_current_state_json(self):
        return json.dumps({JSONMessage.STATUS.name: self.local_status}).encode()

    def connectionMade(self):
        self.factory.stopTrying()
        deferred_state_machine = deferToThread(self.factory.state_machine.start, self)
        self.local_status = Status.CONNECTED.name
        self.transport.write(self.get_current_state_json())
        
    def dataReceived(self, encoded_json_data):
        data = json.loads(encoded_json_data.decode())
        if JSONMessage.STATUS.name in data:
            self.remote_status = data[JSONMessage.STATUS.name]
            if self.local_status == Status.CONNECTED.name and self.remote_status == Status.CONNECTED.name:
                self.local_status = Status.READY.name
                self.transport.write(self.get_current_state_json())
        if JSONMessage.LOG.name in data:
            if data[JSONMessage.LOG.name] == JSONLOGMessage.SENT.name:
                logging.info('REMOTE SENT ' + get_packet_info(pickle.loads(codecs.decode(data[JSONMessage.PARAMETERS.name].encode(), "base64"))))
            elif data[JSONMessage.LOG.name] == JSONLOGMessage.RECEIVED.name:
                logging.info('REMOTE RECEIVED ' + get_packet_info(pickle.loads(codecs.decode(data[JSONMessage.PARAMETERS.name].encode(), "base64"))))
        print("Status: ", self.local_status, self.remote_status)
        print("Received:", data)

class NodeServerProtocol(Protocol):
    remote_status = Status.DISCONNECTED.name
    local_status = Status.DISCONNECTED.name

    def get_current_state_json(self):
        return json.dumps({JSONMessage.STATUS.name: self.local_status}).encode()

    def connectionMade(self):
        deferred_state_machine = deferToThread(self.factory.state_machine.start, self)
        self.local_status = Status.CONNECTED.name
        self.transport.write(self.get_current_state_json())
        
    def dataReceived(self, encoded_json_data):
        data = json.loads(encoded_json_data.decode())
        if JSONMessage.STATUS.name in data:
            self.remote_status = data[JSONMessage.STATUS.name]
            if self.local_status == Status.CONNECTED.name and self.remote_status == Status.CONNECTED.name:
                self.local_status = Status.READY.name
                self.transport.write(self.get_current_state_json())
        if JSONMessage.LOG.name in data:
            if data[JSONMessage.LOG.name] == JSONLOGMessage.SENT.name:
                logging.info('REMOTE SENT ' + get_packet_info(pickle.loads(codecs.decode(data[JSONMessage.PARAMETERS.name].encode(), "base64"))))
            elif data[JSONMessage.LOG.name] == JSONLOGMessage.RECEIVED.name:
                logging.info('REMOTE RECEIVED ' + get_packet_info(pickle.loads(codecs.decode(data[JSONMessage.PARAMETERS.name].encode(), "base64"))))
        print("Status: ", self.local_status, self.remote_status)
        print("Received:", data)

    def connectionLost(self, reason):
        self.remote_status = Status.DISCONNECTED.name
        self.local_status = Status.DISCONNECTED.name
        self.factory.connectionLost(reason)