from twisted.internet.protocol import ClientFactory, ServerFactory
from twisted.internet.defer import Deferred

from modules.controllers.protocol import NodeClientProtocol, NodeServerProtocol

class NodeClientFactory(ClientFactory):
    protocol = NodeClientProtocol

    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.deferred = Deferred()

    def connectionLost(self, reason):
        self.deferred.callback("done")

class NodeServerFactory(ServerFactory):
    protocol = NodeServerProtocol
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.deferred = Deferred()

    def connectionLost(self, reason):
        pass
        #self.deferred.callback("done")