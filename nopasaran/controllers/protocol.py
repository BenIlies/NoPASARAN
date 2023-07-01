import json

from twisted.internet.protocol import Protocol

from nopasaran.controllers.messages import JSONMessage, Status

class WorkerProtocol(Protocol):
    remote_status = Status.DISCONNECTED.name
    local_status = Status.DISCONNECTED.name
    is_active = True
    queue = []

    def get_current_state_json(self):
        return json.dumps({JSONMessage.STATUS.name: self.local_status}).encode()
        
    def dataReceived(self, encoded_json_data):
        data = json.loads(encoded_json_data.decode())
        if JSONMessage.STATUS.name in data:
            self.remote_status = data[JSONMessage.STATUS.name]
            if self.local_status == Status.CONNECTED.name and self.remote_status == Status.CONNECTED.name:
                self.local_status = Status.READY.name
                self.transport.write(self.get_current_state_json())
            if self.local_status == Status.DISCONNECTING.name and self.remote_status == Status.DISCONNECTING.name:
                self.is_active = False
                self.transport.loseConnection()
        if JSONMessage.SYNC.name in data:
            self.queue.append(data)
        print("Status: ", self.local_status, self.remote_status)
        print("Received:", data)

    def disconnecting(self):
        self.local_status = Status.DISCONNECTING.name
        self.transport.write(self.get_current_state_json())
        
    def connectionLost(self, reason):
        self.is_active = False

    def send_sync(self, content):
        self.transport.write(json.dumps({JSONMessage.SYNC.name: content}).encode())

class WorkerClientProtocol(WorkerProtocol):
    def connectionMade(self):
        self.factory.stopTrying()
        self.factory.state_machine.set_variable(self.factory.variable, self)
        self.local_status = Status.CONNECTED.name
        self.transport.write(self.get_current_state_json())
        

class WorkerServerProtocol(WorkerProtocol):
    def connectionMade(self):
        self.factory.state_machine.set_variable(self.factory.variable, self)
        self.local_status = Status.CONNECTED.name
        self.transport.write(self.get_current_state_json())