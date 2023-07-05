from twisted.internet.protocol import ReconnectingClientFactory, ServerFactory

from nopasaran.controllers.protocol import WorkerClientProtocol, WorkerServerProtocol


class WorkerClientFactory(ReconnectingClientFactory):
    """
    A factory for creating WorkerClientProtocol instances.
    
    This factory is responsible for creating client protocols and managing reconnection.
    """

    protocol = WorkerClientProtocol
    
    def __init__(self, state_machine, variable):
        """
        Initialize the WorkerClientFactory.
        
        Args:
            state_machine: The state machine object.
            variable: The variable object.
        """
        self.state_machine = state_machine
        self.variable = variable
    


class WorkerServerFactory(ServerFactory):
    """
    A factory for creating WorkerServerProtocol instances.
    
    This factory is responsible for creating server protocols.
    """

    protocol = WorkerServerProtocol

    def __init__(self, state_machine, variable):
        """
        Initialize the WorkerServerFactory.
        
        Args:
            state_machine: The state machine object.
            variable: The variable object.
        """
        self.state_machine = state_machine
        self.variable = variable
