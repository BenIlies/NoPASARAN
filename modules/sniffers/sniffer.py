import time

from scapy.all import AsyncSniffer, Ether, sniff

class Sniffer(AsyncSniffer):
    def __init__(self, stack, filter=''):
        super().__init__(prn=self.__handle_sniffer(), lfilter=lambda pkt: self.__filter_packet(pkt))
        self.stack = stack 
        self.__filter = filter

        
    def __handle_sniffer(self):
        def pkt_callback(packet):
            self.stack.append(packet)
        return pkt_callback
    
    def __filter_packet(self, packet):
        if 'Ether' in packet:
            if (packet[Ether].src != Ether().src):
                pkts_icmp = sniff(offline=packet, filter=self.__filter)
                if packet in pkts_icmp:
                    return True
        return False
    
    def set_filter(self, filter):
        self.__filter = filter
    
    def get_packet_layers(self, packet):
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