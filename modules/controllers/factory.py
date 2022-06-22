from twisted.internet.protocol import ClientFactory, ServerFactory
from twisted.internet.defer import Deferred

from modules.controllers.protocol import NodeProtocol, ProxyProtocol

class NodeFactory(ClientFactory):
    protocol = NodeProtocol

    def __init__(self, link_id):
        self.link_id = link_id
        self.deferred = Deferred()

    def connectionLost(self, reason):
        self.deferred.callback("done")

class ProxyFactory(ServerFactory):
    protocol = ProxyProtocol
    
    def __init__(self):
        self.deferred = Deferred()

    def connectionLost(self, reason):
        pass
        #self.deferred.callback("done")