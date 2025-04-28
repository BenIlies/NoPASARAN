from scapy.all import AsyncSniffer, UDP, IP, conf
import logging
import time
from collections import defaultdict

class UDPProbeListener:
    """
    Helper class to listen for UDP probes and count packets per destination port.
    """
    def __init__(self, source_ip, timeout, dports=None):
        self.source_ip = source_ip
        self.timeout = timeout
        self.dports = dports if dports is not None else []
        self.port_counts = defaultdict(int)
        self.sniffer = None

    def _packet_handler(self, packet):
        """
        Internal callback for each packet captured.
        """
        if packet.haslayer(UDP) and packet.haslayer(IP):
            if packet[IP].src == self.source_ip:
                if not self.dports or packet[UDP].dport in self.dports:
                    self.port_counts[packet[UDP].dport] += 1

    def _build_filter(self):
        """
        Build the BPF filter string combining source IP and destination ports.
        """
        base_filter = f"udp and src host {self.source_ip}"
        if self.dports:
            port_filter = " or ".join([f"dst port {p}" for p in self.dports])
            return f"{base_filter} and ({port_filter})"
        return base_filter

    def run(self):
        """
        Start the sniffer and collect packets during the timeout.
        """
        conf.verb = 0  # Silence Scapy
        try:
            self.sniffer = AsyncSniffer(
                iface="any",  # Listen on all interfaces
                filter=self._build_filter(),
                prn=self._packet_handler,
                store=False
            )
            self.sniffer.start()
            time.sleep(self.timeout)
            self.sniffer.stop()
        except Exception as e:
            logging.exception(f"[UDPProbeListener] Error during sniffing: {e}")