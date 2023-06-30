from twisted.internet.protocol import ReconnectingClientFactory, ServerFactory

from nopasaran.controllers.protocol import NodeClientProtocol, NodeServerProtocol

class NodeClientFactory(ReconnectingClientFactory):
    protocol = NodeClientProtocol
    
    def __init__(self, state_machine, variable):
        self.state_machine = state_machine
        self.variable = variable
    


class NodeServerFactory(ServerFactory):
    protocol = NodeServerProtocol

    def __init__(self, state_machine, variable):
        self.state_machine = state_machine
        self.variable = variable