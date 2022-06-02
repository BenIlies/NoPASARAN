from utils import *
from scapy.all import send, sr, sr1, AsyncSniffer, Ether
from threading import Timer

class Machine:
    def __init__(self, xstate_json, variables = {}):
        self.__id = xstate_json['id']
        self.__initial = xstate_json['initial']
        self.__states = xstate_json['states']
        self.current_state = self.__initial
        self.__variables = variables
        self.__sniffer = AsyncSniffer(prn=self.__handle_sniffer(), lfilter=lambda pkt: pkt[Ether].src != Ether().src)
        self.__sniffer_last_packet = 'ans'


    def __handle_sniffer(self):
        def pkt_callback(packet):
            if 'TCP' in packet:
                self.__variables[self.__sniffer_last_packet] = packet
                if packet['TCP'].flags == 'S':
                    self.trigger('SYN_RECEIVED')
                elif packet['TCP'].flags == 'SA':
                    self.trigger('SYN_ACK_RECEIVED')
                elif packet['TCP'].flags == 'P':
                    self.trigger('PSH_RECEIVED')
                elif packet['TCP'].flags == 'PA':
                    self.trigger('PSH_ACK_RECEIVED')
                elif packet['TCP'].flags == 'F':
                    self.trigger('FIN_RECEIVED')
                elif packet['TCP'].flags == 'FA':
                    self.trigger('FIN_ACK_RECEIVED')
                elif packet['TCP'].flags == 'A':
                    self.trigger('ACK_RECEIVED')
        return pkt_callback

    def get_id(self):
        return self.__id

    def __transition(self, state):
        if state in self.__states:
            if 'exit' in self.__states[self.current_state]:
                for action in get_safe_array(self.__states[self.current_state]['exit']):
                    self.__handle_action(action)
            self.current_state = state
            if 'entry' in self.__states[self.current_state]:
                for action in get_safe_array(self.__states[self.current_state]['entry']):
                    self.__handle_action(action)

    def trigger(self, event):
        if event in self.__states[self.current_state]['on']:
            self.__transition(self.__states[self.current_state]['on'][event]['target'])
        else:
            print('SKIPPED: ' + event + ' triggered in state: ' + self.current_state + '. No matching event.')


    def __handle_action(self, action):
        parsed = action.split()
        if parsed[0] == 'listen':
            self.__sniffer.start()
            self.__sniffer_last_packet = parsed[1]
        elif parsed[0] == 'close':
            self.__sniffer.stop()
            self.trigger('LISTENER_STOPPED')
        elif parsed[0] == 'send':
            send(self.__variables[parsed[1]])
        elif parsed[0] == 'send_delayed':
            t = Timer(float(parsed[2]), send, [self.__variables[parsed[1]]])
            t.start()
        elif parsed[0] == 'create_TCP_packet':
            self.__variables[parsed[1]] = create_TCP_packet()
        elif parsed[0] == 'set_IP_dst':
            set_IP_dst(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'set_IP_src':
            set_IP_src(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'set_TCP_sport':
            set_TCP_sport(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'set_TCP_dport':
            set_TCP_dport(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'set_TCP_seq':
            set_TCP_seq(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'set_TCP_flags':
            set_TCP_flags(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'set_TCP_ack':
            set_TCP_ack(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'set_TCP_payload':
            set_TCP_payload(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'remove_TCP_payload':
            remove_TCP_payload(self.__variables[parsed[1]])
        elif parsed[0] == 'set_TCP_automatic_packet_seq':
            set_TCP_automatic_packet_seq(self.__variables[parsed[1]])
        elif parsed[0] == 'set_TCP_automatic_packet_ack':
            set_TCP_automatic_packet_ack(self.__variables[parsed[1]], self.__variables[parsed[2]])
        elif parsed[0] == 'print_TCP_payload':
            print(self.__variables[parsed[1]]['TCP'].payload)
        elif parsed[0] == 'done':
            self.trigger('DONE')
        elif parsed[0] == 'completed':
            self.trigger('COMPLETED')
        else:
            raise Exception('Parsing error: argument "' + parsed[0] + '" is unknown.')