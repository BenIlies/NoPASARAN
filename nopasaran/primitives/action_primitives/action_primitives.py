from nopasaran.primitives.primitives import Primitives
from nopasaran.primitives.action_primitives.tmp import TmpPrimitives
from nopasaran.primitives.action_primitives.data_manipulation import DataManipulationPrimitives
from nopasaran.primitives.action_primitives.nested_machine_utils import NestedMachinePrimitives
from nopasaran.primitives.action_primitives.control_channel_primitives import ControlChannelPrimitives
from nopasaran.primitives.action_primitives.ip_primitives import IPPrimitives
from nopasaran.primitives.action_primitives.tcp_primitives import TCPPrimitives
from nopasaran.primitives.action_primitives.udp_primitives import UDPPrimitives

class ActionPrimitives(Primitives):
    """
    Class containing action primitives for the state machine.
    """
    classes = [TmpPrimitives, DataManipulationPrimitives, NestedMachinePrimitives, ControlChannelPrimitives, IPPrimitives, TCPPrimitives, UDPPrimitives]
