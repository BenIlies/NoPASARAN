from twisted.internet.protocol import ReconnectingClientFactory, ServerFactory

from nopasaran.controllers.protocol import WorkerClientProtocol, WorkerServerProtocol

class WorkerClientFactory(ReconnectingClientFactory):
    protocol = WorkerClientProtocol
    
    def __init__(self, state_machine, variable):
        self.state_machine = state_machine
        self.variable = variable
    


class WorkerServerFactory(ServerFactory):
    protocol = WorkerServerProtocol

    def __init__(self, state_machine, variable):
        self.state_machine = state_machine
        self.variable = variable