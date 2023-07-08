from nopasaran.primitives.primitives import Primitives
from nopasaran.primitives.action_primitives.tcp_action_primitives import TCPActionPrimitives

class ActionPrimitives(Primitives):
    """
    Class containing action primitives for the state machine.
    """
    classes = [TCPActionPrimitives]
