from scapy.all import AsyncSniffer, UDP, IP, conf
from nopasaran.decorators import parsing_decorator
from nopasaran.utils import group_ports
import logging
import time
class UDPProbeListener:
    """
    Helper class to listen for UDP probes using AsyncSniffer.
    """

    def __init__(self, source_ip, timeout):
        self.source_ip = source_ip
        self.timeout = timeout
        self.ports_received = set()
        self.sniffer = None

    def _packet_handler(self, packet):
        """
        Internal callback for each packet captured.
        """
        if packet.haslayer(UDP) and packet.haslayer(IP):
            if packet[IP].src == self.source_ip:
                self.ports_received.add(packet[UDP].dport)

    def run(self):
        """
        Start the sniffer and collect packets.
        """
        conf.verb = 0  # Silence Scapy
        self.sniffer = AsyncSniffer(
            filter=f"udp and src host {self.source_ip}",
            prn=self._packet_handler,
            store=False
        )
        self.sniffer.start()
        time.sleep(self.timeout)
        self.sniffer.stop()