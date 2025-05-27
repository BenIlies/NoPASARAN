from nopasaran.primitives.primitives import Primitives
from nopasaran.primitives.action_primitives.data_manipulation import DataManipulationPrimitives
from nopasaran.primitives.action_primitives.timing_primitives import TimingPrimitives
from nopasaran.primitives.action_primitives.nested_machine_utils import NestedMachinePrimitives
from nopasaran.primitives.action_primitives.data_channel_primitives import DataChannelPrimitives
from nopasaran.primitives.action_primitives.control_channel_primitives import ControlChannelPrimitives
from nopasaran.primitives.action_primitives.event_primitives import EventPrimitives
from nopasaran.primitives.action_primitives.signaling_primitive import SignalingPrimitives
from nopasaran.primitives.action_primitives.io_primitives import IOPrimitives
from nopasaran.primitives.action_primitives.ip_primitives import IPPrimitives
from nopasaran.primitives.action_primitives.tcp_primitives import TCPPrimitives
from nopasaran.primitives.action_primitives.udp_primitives import UDPPrimitives
from nopasaran.primitives.action_primitives.dns_primitives import DNSPrimitives
from nopasaran.primitives.action_primitives.icmp_primitives import ICMPPrimitives
from nopasaran.primitives.action_primitives.certificate_primitives import CertificatePrimitives
from nopasaran.primitives.action_primitives.tls_primitives import TLSPrimitives
from nopasaran.primitives.action_primitives.http_1_request_primitives import HTTP1RequestPrimitives
from nopasaran.primitives.action_primitives.http_1_response_primitives import HTTP1ResponsePrimitives
from nopasaran.primitives.action_primitives.http_2_server_primitives import HTTP2ServerPrimitives
from nopasaran.primitives.action_primitives.http_2_client_primitives import HTTP2ClientPrimitives
from nopasaran.primitives.action_primitives.server_echo_primitives import ServerEchoPrimitives
from nopasaran.primitives.action_primitives.https_1_response_primitives import HTTPS1ResponsePrimitives
from nopasaran.primitives.action_primitives.https_1_request_primitives import HTTPS1RequestPrimitives
from nopasaran.primitives.action_primitives.client_echo_primitives import ClientEchoPrimitives
from nopasaran.primitives.action_primitives.probing_primitives import PortProbingPrimitives
from nopasaran.primitives.action_primitives.replay_primitives import ReplayPrimitives
from nopasaran.primitives.action_primitives.http_simple_client_primitives import HTTPSimpleClientPrimitives
from nopasaran.primitives.action_primitives.tcp_dns_request_primitives import TCPDNSRequestPrimitives
from nopasaran.primitives.action_primitives.tcp_dns_response_primitives import TCPDNSResponsePrimitives
from nopasaran.primitives.action_primitives.udp_dns_request_primitives import UDPDNSRequestPrimitives
from nopasaran.primitives.action_primitives.udp_dns_response_primitives import UDPDNSResponsePrimitives


class ActionPrimitives(Primitives):
    """
    Class containing action primitives for the state machine.
    """
    classes = [
        DataManipulationPrimitives, 
        TimingPrimitives,
        NestedMachinePrimitives, 
        DataChannelPrimitives, 
        ControlChannelPrimitives, 
        EventPrimitives,
        SignalingPrimitives,
        IOPrimitives,
        IPPrimitives, 
        TCPPrimitives, 
        UDPPrimitives,
        DNSPrimitives,
        ICMPPrimitives,
        CertificatePrimitives,
        TLSPrimitives,
        HTTP1RequestPrimitives,
        HTTP1ResponsePrimitives,
        HTTP2ServerPrimitives,
        HTTP2ClientPrimitives,
        ServerEchoPrimitives,
        HTTPS1ResponsePrimitives,
        HTTPS1RequestPrimitives,
        ClientEchoPrimitives,
        PortProbingPrimitives,
        ReplayPrimitives,
        HTTPSimpleClientPrimitives,
        TCPDNSRequestPrimitives,
        TCPDNSResponsePrimitives,
        UDPDNSRequestPrimitives,
        UDPDNSResponsePrimitives
        ]
