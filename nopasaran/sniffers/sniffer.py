import logging
from nopasaran.utils import *
from scapy.all import AsyncSniffer, Ether, sniff


class Sniffer(AsyncSniffer):
    """
    Custom Sniffer class inheriting from the AsyncSniffer of Scapy.
    """

    def __init__(self, machine, filter=''):
        """
        Initialize the Sniffer.
        
        Args:
            machine (str): A string defining the machine to sniff.
            filter (str): A string defining the filter for packets.
        """
        super().__init__(prn=self.__handle_sniffer(), lfilter=lambda pkt: self.__filter_packet(pkt))
        self.machine = machine
        self.__filter = filter
        self.queue = None
        self.src = Ether().src
        logging.debug('[Sniffer] Machine ID: {}: Sniffer initialized'.format(machine.machine_id))

    def __handle_sniffer(self):
        """
        Handle the sniffer callback.
        
        Returns:
            function: The callback function to execute when a packet is sniffed.
        """
        def pkt_callback(packet):
            """
            Callback function for sniffed packets.
            
            Args:
                packet: The sniffed packet.
            """
            if self.queue is not None:
                self.queue.append(packet)
        return pkt_callback

    def __filter_packet(self, packet):
        """
        Filter the packets.
        
        Args:
            packet: The packet to filter.
        
        Returns:
            bool: True if the packet is accepted, False otherwise.
        """
        # Check if the packet is an IP packet
        if 'IP' not in packet:
            return False  # Reject if it's not an IP packet

        # Check if the source MAC address of the packet is different from the local machine's MAC
        if packet[Ether].src == self.src:
            return False  # Reject packets with the local machine's MAC address
        
        # Apply further filtering (e.g., using sniff)
        filtered_packets = sniff(offline=packet, filter=self.__filter)
        if packet in filtered_packets:
            logging.info("[Sniffer] Packet passed the filter: %s", packet)
            return True
        
        return False

    def set_filter(self, filter):
        """
        Set a new filter.
        
        Args:
            filter (str): The new filter string.
        """
        self.__filter = filter
        logging.debug("[Sniffer] Filter set to: %s", filter)