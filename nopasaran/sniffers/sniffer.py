from nopasaran.utils import *
from scapy.all import AsyncSniffer, Ether, sniff

class Sniffer(AsyncSniffer):
    """
    Custom Sniffer class inheriting from the AsyncSniffer of Scapy.
    """
    def __init__(self, machine, filter=''):
        """
        Initializer for the Sniffer class.
        Args:
            machine (str): A string defining the machine to sniff.
            filter (str): A string defining the filter for packets.
        """
        super().__init__(prn=self.__handle_sniffer(), lfilter=lambda pkt: self.__filter_packet(pkt))
        self.machine = machine 
        self.__filter = filter
        self.queue = None
        
    def __handle_sniffer(self):
        """
        Internal method to handle the sniffer. A callback for packets sniffed.
        Returns:
            pkt_callback (func): Function to execute when a packet is sniffed.
        """
        def pkt_callback(packet):
            if self.queue != None:
                self.queue.append(packet)
        return pkt_callback
    
    def __filter_packet(self, packet):
        """
        Internal method to filter the packets.
        Args:
            packet (Packet): Packet to filter.
        Returns:
            bool: True if the packet is accepted, False otherwise.
        """
        if 'Ether' in packet:
            if (packet[Ether].src != Ether().src):
                filtered_packets = sniff(offline=packet, filter=self.__filter)
                if packet in filtered_packets:
                    return True
        return False
    
    def set_filter(self, filter):
        """
        Method to set a new filter.
        Args:
            filter (str): String defining the new filter.
        """
        self.__filter = filter
    
    def get_packet_layers(self, packet):
        """
        Method to get all the layers in a packet.
        Args:
            packet (Packet): Packet to analyze.
        Returns:
            list: List of layers in the packet.
        """
        layers = []
        counter = 0
        while True:
            layer = packet.getlayer(counter)
            if layer is None:
                break
            else:
                layers.append(layer)
            counter += 1
        return layers
