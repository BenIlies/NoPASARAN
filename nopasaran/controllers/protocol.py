import json
import logging
import base64
import pickle

from twisted.internet.protocol import Protocol

from nopasaran.definitions.control_channel import JSONMessage, Status


class WorkerProtocol(Protocol):
    """
    Base protocol for worker communication.
    
    This protocol handles the communication between workers and manages their status.
    """

    remote_status = Status.DISCONNECTED.name
    local_status = Status.DISCONNECTED.name
    is_active = True
    queue = []

    def get_current_state_json(self):
        """
        Get the current state as a JSON-encoded string.
        
        Returns:
            bytes: The JSON-encoded current state.
        """
        return json.dumps({JSONMessage.STATUS.name: self.local_status}).encode()

    def dataReceived(self, encoded_json_data):
        """
        Handle received data.
        
        This method is called when data is received from the remote endpoint.
        
        Args:
            encoded_json_data (bytes): The received data as bytes.
        """
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
            encoded_data = data[JSONMessage.SYNC.name]
            serialized_data = base64.b64decode(encoded_data)
            content = pickle.loads(serialized_data)
            self.queue.append(content)
        logging.info("[Control Channel] Status: %s, %s", self.local_status, self.remote_status)
        logging.info("[Control Channel] Received: %s", data)
        

    def disconnecting(self):
        """
        Initiate the disconnection process.
        
        This method sets the local status to DISCONNECTING and sends the current state to the remote endpoint.
        """
        self.local_status = Status.DISCONNECTING.name
        self.transport.write(self.get_current_state_json())
        logging.info("[Control Channel] Disconnecting...")

    def connectionLost(self, reason):
        """
        Handle the connection loss.
        
        This method is called when the connection is lost with the remote endpoint.
        
        Args:
            reason: The reason for the connection loss.
        """
        self.is_active = False
        logging.info("[Control Channel] Connection lost.")

    def send_sync(self, content):
        """
        Send a sync message to the remote endpoint.
        
        This method sends a sync message with the specified content to the remote endpoint.
        
        Args:
            content: The content of the sync message.
        """
        serialized_data = pickle.dumps(content)
        encoded_data = base64.b64encode(serialized_data).decode("utf-8")
        self.transport.write(json.dumps({JSONMessage.SYNC.name: encoded_data}).encode())
        logging.info("[Control Channel] Sync message sent: %s", content)


class WorkerClientProtocol(WorkerProtocol):
    """
    Protocol for worker clients.
    
    This protocol is used by worker clients to communicate with the server.
    """

    def connectionMade(self):
        """
        Handle the connection made event.
        
        This method is called when the connection is successfully established with the server.
        It sets the local status to CONNECTED, sends the current state to the server, and logs the event.
        """
        self.factory.stopTrying()
        self.factory.state_machine.set_variable_value(self.factory.variable, self)
        self.local_status = Status.CONNECTED.name
        self.transport.write(self.get_current_state_json())
        logging.info("[Control Channel] Connection made")


class WorkerServerProtocol(WorkerProtocol):
    """
    Protocol for worker servers.
    
    This protocol is used by worker servers to communicate with clients.
    """

    def connectionMade(self):
        """
        Handle the connection made event.
        
        This method is called when a client successfully establishes a connection with the server.
        It sets the local status to CONNECTED, sends the current state to the client, and logs the event.
        """
        self.factory.state_machine.set_variable_value(self.factory.variable, self)
        self.local_status = Status.CONNECTED.name
        self.transport.write(self.get_current_state_json())
        logging.info("[Control Channel] Connection made")
