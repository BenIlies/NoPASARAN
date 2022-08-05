import codecs
import json
import pickle
import logging
import time

from scapy.all import AsyncSniffer, Ether


from modules.controllers.messages import JSONLOGMessage, JSONMessage

class Sniffer(AsyncSniffer):
    def __init__(self):
        super().__init__(prn=self.__handle_sniffer(), lfilter=lambda pkt: self.__filter_packet(pkt))
        self.__variables = {}
        self.protocols_l3 = []
        self.protocols_l4 = []
        self.protocols_l7 = []
        self.filter_src = []
        self.filter_dst = []
        self.filter_sport = []
        self.filter_dport = []
        self.stack = 'ans'
        self.__variables[self.stack] = []
        

    def __filter_packet(self, packet):
        if 'Ether' in packet:
            if (packet[Ether].src != Ether().src) and ('TCP' in packet):
                
                
                
                
                
                if (packet['TCP'].sport in self.filter_sport) or (packet['TCP'].dport in self.filter_dport):
                    return True
        return False


    def __handle_sniffer(self):
        def pkt_callback(packet):
            print(packet)
            self.__variables[self.stack].append(packet)
        return pkt_callback
    
    
    def trigger(self, str):
        print(str)
        
    
    def get_stack(self):
        return self.__variables[self.stack]
    
    def get_stack_top(self):
        return self.__variables[self.stack][0]
    
    def discard_stack_packet(self, stack):
        stack.pop(0)
    
    def do_handle_packets(self, time_to_wait=3):
        timeout = False
        start_time = time.time()
        while (True):
            if len(self.get_stack()) >= 1:
                if self.get_stack_top()['TCP'].flags in ['S', 'SA', 'P', 'PA', 'F', 'FA', 'A']:
                    if self.get_stack_top()['TCP'].flags == 'S':
                        self.trigger('SYN_RECEIVED')
                    elif self.get_stack_top()['TCP'].flags == 'SA':
                        self.trigger('SYN_ACK_RECEIVED')
                    elif self.get_stack_top()['TCP'].flags == 'P':
                        self.trigger('PSH_RECEIVED')
                    elif self.get_stack_top()['TCP'].flags == 'PA':
                        self.trigger('PSH_ACK_RECEIVED')
                    elif self.get_stack_top()['TCP'].flags == 'F':
                        self.trigger('FIN_RECEIVED')
                    elif self.get_stack_top()['TCP'].flags == 'FA':
                        self.trigger('FIN_ACK_RECEIVED')
                    elif self.get_stack_top()['TCP'].flags == 'A':
                        self.trigger('ACK_RECEIVED')
                    break
                else:
                    self.discard_stack_packet(self.get_stack())
            if (time.time() - start_time > time_to_wait):
                timeout = True
                break
        if (timeout):
            self.trigger('TIMEOUT')

