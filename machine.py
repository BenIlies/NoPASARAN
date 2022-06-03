import time
from utils import *
from scapy.all import send, AsyncSniffer, Ether
import hashlib

class Machine:
    def __init__(self, xstate_json, variables = {}):
        self.__id = xstate_json['id']
        self.__initial = xstate_json['initial']
        self.__states = xstate_json['states']
        self.__current_state = self.__initial
        self.__variables = variables
        self.__sniffer = AsyncSniffer(prn=self.__handle_sniffer(), lfilter=lambda pkt: pkt[Ether].src != Ether().src)
        self.__sniffer_stack = 'ans'
        self.__variables[self.__sniffer_stack] = []
        self.__complete_chain_states = [{self.__initial: hashlib.sha256(repr(time.time()).encode()).hexdigest()}]
        self.__chain_states = [self.__complete_chain_states[0]]

    def start(self):
        self.__trigger('STARTED')


    def __handle_sniffer(self):
        def pkt_callback(packet):
            if 'TCP' in packet:
                self.__variables[self.__sniffer_stack].append(packet)
        return pkt_callback

    def get_id(self):
        return self.__id

    def get_chain(self):
        return self.__chain_states

    def get_full_chain(self):
        return self.__complete_chain_states
    
    def get_state(self):
        return self.__current_state

    def __transition(self, state):
        if state in self.__states:
            self.__exit_current_state()
            self.__current_state = state
            self.__complete_chain_states.append({self.__current_state: hashlib.sha256(repr(time.time()).encode()).hexdigest()})
            self.__chain_states.append(self.__complete_chain_states[len(self.__complete_chain_states) - 1])
            self.__enter_current_state()


    def __enter_current_state(self):
        if 'entry' in self.__states[self.__current_state]:
            for action in get_safe_array(self.__states[self.__current_state]['entry']):
                self.__handle_action(action)

    def __exit_current_state(self):
        if 'exit' in self.__states[self.__current_state]:
            for action in get_safe_array(self.__states[self.__current_state]['exit']):
                self.__handle_action(action)

    def __return_to_previous_state(self):
        if len(self.__chain_states) > 1:
            self.__chain_states.pop(len(self.__chain_states) - 1)
            self.__complete_chain_states.append(self.__chain_states[len(self.__chain_states) - 1])
            self.__current_state = list(self.__chain_states[len(self.__chain_states) - 1].keys())[0]
            self.__enter_current_state()
        else:
            print('DEBUG: Cannot go back from initial state ' + self.__initial + '.')


    def __trigger(self, event):
        if event in self.__states[self.__current_state]['on']:
            self.__transition(self.__states[self.__current_state]['on'][event]['target'])
        else:
            print('SKIPPED: ' + event + ' triggered in state: ' + self.__current_state + '. No matching event.')


    def __handle_action(self, action):
        parsed = action.split()
        if parsed[0] == 'listen':
            self.__sniffer.start()
            self.__sniffer_stack = parsed[1]
        elif parsed[0] == 'close':
            self.__sniffer.stop()
            self.__trigger('LISTENER_STOPPED')
        elif parsed[0] == 'send':
            send(self.__variables[parsed[1]])
            self.__trigger('PACKET_SENT')
        elif parsed[0] == 'handle_packets':
            timeout = False
            start_time = time.time()
            while (True):
                if len(self.__variables[self.__sniffer_stack]) >= 1:
                    if self.__variables[self.__sniffer_stack][0]['TCP'].flags in ['S', 'SA', 'P', 'PA', 'F', 'FA', 'A']:
                        if self.__variables[self.__sniffer_stack][0]['TCP'].flags == 'S':
                            self.__trigger('SYN_RECEIVED')
                        elif self.__variables[self.__sniffer_stack][0]['TCP'].flags == 'SA':
                            self.__trigger('SYN_ACK_RECEIVED')
                        elif self.__variables[self.__sniffer_stack][0]['TCP'].flags == 'P':
                            self.__trigger('PSH_RECEIVED')
                        elif self.__variables[self.__sniffer_stack][0]['TCP'].flags == 'PA':
                            self.__trigger('PSH_ACK_RECEIVED')
                        elif self.__variables[self.__sniffer_stack][0]['TCP'].flags == 'F':
                            self.__trigger('FIN_RECEIVED')
                        elif self.__variables[self.__sniffer_stack][0]['TCP'].flags == 'FA':
                            self.__trigger('FIN_ACK_RECEIVED')
                        elif self.__variables[self.__sniffer_stack][0]['TCP'].flags == 'A':
                            self.__trigger('ACK_RECEIVED')
                        break
                    else:
                        self.__variables[self.__sniffer_stack].pop(0)
                if (time.time() - start_time > float(self.__variables[parsed[1]])):
                    timeout = True
                    break
            if (timeout):
                self.__trigger('TIMEOUT')
        elif parsed[0] == 'pop':
            self.__variables[parsed[1]].pop(0)
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
            set_TCP_automatic_packet_ack(self.__variables[parsed[1]], self.__variables[parsed[2]][0])
        elif parsed[0] == 'print_TCP_payload':
            print(self.__variables[parsed[1]][0]['TCP'].payload)
        elif parsed[0] == 'set_random_int':
            self.__variables[parsed[1]] = set_random_int(parsed[2], parsed[3])
        elif parsed [0] == 'set_random_float':
            self.__variables[parsed[1]] = set_random_float(parsed[2], parsed[3])
        elif parsed[0] == 'return':
            self.__return_to_previous_state()
        else:
            raise Exception('Parsing error: argument "' + parsed[0] + '" is unknown.')