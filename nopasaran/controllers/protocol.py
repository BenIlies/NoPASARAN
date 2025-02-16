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
        try:
            return json.dumps({JSONMessage.STATUS.name: self.local_status}).encode()
        except (TypeError, json.JSONDecodeError) as e:
            logging.error("[Control Channel] Error encoding current state to JSON: %s", e)
            return b''

    def send_encoded_data(self, data):
        """
        Send encoded data through the transport.
        
        This method encodes the provided data to JSON, base64, and sends it.
        
        Args:
            data (dict): The data to encode and send.
        """
        try:
            json_data = json.dumps(data).encode()
            base64_data = base64.b64encode(json_data).decode("utf-8")
            self.transport.write(base64_data.encode())
            logging.info("[Control Channel] Data sent: %s", data)
        except (TypeError, json.JSONDecodeError) as e:
            logging.error("[Control Channel] Error encoding data to JSON: %s", e)
        except Exception as e:
            logging.error("[Control Channel] Unexpected error in send_encoded_data: %s", e)

    def dataReceived(self, encoded_json_data):
        """
        Handle received data.
        
        This method is called when data is received from the remote endpoint.
        
        Args:
            encoded_json_data (bytes): The received data as bytes.
        """
        try:
            decoded_data = base64.b64decode(encoded_json_data).decode()
            data = json.loads(decoded_data)
            if JSONMessage.STATUS.name in data:
                self.remote_status = data[JSONMessage.STATUS.name]
                if self.local_status == Status.CONNECTED.name and self.remote_status == Status.CONNECTED.name:
                    self.local_status = Status.READY.name
                    self.remote_status = Status.READY.name
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

        except (json.JSONDecodeError, KeyError) as e:
            logging.error("[Control Channel] Error processing received data: %s", e)
        except (pickle.PickleError) as e:
            logging.error("[Control Channel] Error decoding sync message: %s", e)
        except Exception as e:
            logging.error("[Control Channel] Unexpected error in dataReceived: %s", e)

    def disconnecting(self):
        """
        Initiate the disconnection process.
        
        This method sets the local status to DISCONNECTING and sends the current state to the remote endpoint.
        """
        try:
            self.local_status = Status.DISCONNECTING.name
            self.send_encoded_data({JSONMessage.STATUS.name: self.local_status})
            logging.info("[Control Channel] Disconnecting...")
        except Exception as e:
            logging.error("[Control Channel] Error during disconnection: %s", e)

    def connectionLost(self, reason):
        """
        Handle the connection loss.
        
        This method is called when the connection is lost with the remote endpoint.
        
        Args:
            reason: The reason for the connection loss.
        """
        try:
            self.is_active = False
            logging.info("[Control Channel] Connection lost.")
            logging.info(reason)
        except Exception as e:
            logging.error("[Control Channel] Error handling connection lost: %s", e)

    def send_sync(self, content):
        """
        Send a sync message to the remote endpoint.
        
        This method sends a sync message with the specified content to the remote endpoint.
        
        Args:
            content: The content of the sync message.
        """
        try:
            serialized_data = pickle.dumps(content)
            encoded_data = base64.b64encode(serialized_data).decode("utf-8")
            self.send_encoded_data({JSONMessage.SYNC.name: encoded_data})
            logging.info("[Control Channel] Sync message sent: %s", content)
        except (pickle.PickleError) as e:
            logging.error("[Control Channel] Error serializing or encoding sync message: %s", e)
        except (TypeError, json.JSONDecodeError) as e:
            logging.error("[Control Channel] Error encoding sync message to JSON: %s", e)
        except Exception as e:
            logging.error("[Control Channel] Unexpected error in send_sync: %s", e)


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
        try:
            self.factory.stopTrying()
            self.factory.state_machine.set_variable_value(self.factory.variable, self)
            self.local_status = Status.CONNECTED.name
            self.send_encoded_data({JSONMessage.STATUS.name: self.local_status})
            logging.info("[Control Channel] Connection made")
        except Exception as e:
            logging.error("[Control Channel] Error during client connection setup: %s", e)


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
        try:
            self.factory.state_machine.set_variable_value(self.factory.variable, self)
            self.local_status = Status.CONNECTED.name
            self.send_encoded_data({JSONMessage.STATUS.name: self.local_status})
            logging.info("[Control Channel] Connection made")
        except Exception as e:
            logging.error("[Control Channel] Error during server connection setup: %s", e)
