import codecs
import json
import logging
import pickle
import time
import hashlib

from scapy.all import AsyncSniffer, Ether



from modules.utils import *
from modules.interpreters.action_interpreter import ActionInterpreter
from modules.interpreters.condition_interpreter import ConditionInterpreter
from modules.controllers.messages import JSONLOGMessage, JSONMessage

class Machine:
    def __init__(self, xstate_json, variables = {}, main_state=True):
        self.__id = xstate_json['id']
        self.__initial = xstate_json['initial']
        self.__states = xstate_json['states']
        self.__current_state = self.__initial
        self.__variables = variables
        self.filter_sport = []
        self.filter_dport = []
        self.__sniffer = AsyncSniffer(prn=self.__handle_sniffer(), lfilter=lambda pkt: self.__filter_packet(pkt))
        self.__sniffer_stack = 'ans'
        self.__variables[self.__sniffer_stack] = []
        self.__complete_chain_states = [{self.__initial: hashlib.sha256(repr(time.time()).encode()).hexdigest()}]
        self.__chain_states = [self.__complete_chain_states[0]]
        self.controller_protocol = None
        self.finishing_event = "FINISHED"
        self.__main_state=main_state

    def start(self, controller_protocol):
        self.controller_protocol = controller_protocol
        self.trigger('STARTED')
        if self.__main_state:
            self.controller_protocol.transport.loseConnection()
        return self.finishing_event

    def get_id(self):
        return self.__id

    def get_chain(self):
        return self.__chain_states

    def get_full_chain(self):
        return self.__complete_chain_states
    
    def get_state(self):
        return self.__current_state

    def start_sniffer(self):
        self.__sniffer.start()

    def stop_sniffer(self):
        self.__sniffer.stop()

    def set_stack(self, stack):
        self.__sniffer_stack = stack

    def get_stack(self):
        return self.__variables[self.__sniffer_stack]

    def get_stack_top(self):
        return self.__variables[self.__sniffer_stack][0]

    def discard_stack_packet(self, stack):
        stack.pop(0)

    def get_variables(self):
        return self.__variables

    def get_variable(self, name):
        return self.__variables[name]

    def set_variable(self, name, new_value):
        self.__variables[name] = new_value

    def return_to_previous_state(self):
        if len(self.__chain_states) > 1:
            self.__chain_states.pop(len(self.__chain_states) - 1)
            self.__complete_chain_states.append(self.__chain_states[len(self.__chain_states) - 1])
            self.__current_state = list(self.__chain_states[len(self.__chain_states) - 1].keys())[0]
            self.__enter_current_state()
        else:
            print('DEBUG: Cannot go back from initial state ' + self.__initial + '.')

    def trigger(self, event):
        if event in self.__states[self.__current_state]['on']:
            self.__transition(get_safe_array(self.__states[self.__current_state]['on'][event]))
        else:
            print('SKIPPED: ' + event + ' triggered in state: ' + self.__current_state + '. No matching event.')

    def __handle_sniffer(self):
        def pkt_callback(packet):
            serializable_packet = codecs.encode(pickle.dumps(packet), "base64").decode()
            self.controller_protocol.transport.write(json.dumps({JSONMessage.LOG.name: JSONLOGMessage.RECEIVED.name, JSONMessage.PARAMETERS.name: serializable_packet}).encode())
            logging.info('LOCAL RECEIVED ' + get_packet_info(packet))
            self.__variables[self.__sniffer_stack].append(packet)
        return pkt_callback

    def __filter_packet(self, packet):
        if 'Ether' in packet:
            if (packet[Ether].src != Ether().src) and ('TCP' in packet):
                if (packet['TCP'].sport in self.filter_sport) or (packet['TCP'].dport in self.filter_dport):
                    return True
        return False

    def __transition(self, possible_states):
        def check_conditions(possible_state):
            if 'cond' in possible_state:
                return ConditionInterpreter().onecmd(possible_state['cond'], self.__variables)
            else:
                return True

            
        for state in possible_states:
            if state['target'] in self.__states:
                if check_conditions(state):
                    self.__exit_current_state()
                    self.__current_state = state['target']
                    self.__complete_chain_states.append({self.__current_state: hashlib.sha256(repr(time.time()).encode()).hexdigest()})
                    self.__chain_states.append(self.__complete_chain_states[len(self.__complete_chain_states) - 1])
                    self.__enter_current_state()
                    break

    def __enter_current_state(self):
        if 'entry' in self.__states[self.__current_state]:
            for action in get_safe_array(self.__states[self.__current_state]['entry']):
                ActionInterpreter().onecmd(action, self)

    def __exit_current_state(self):
        if 'exit' in self.__states[self.__current_state]:
            for action in get_safe_array(self.__states[self.__current_state]['exit']):
                ActionInterpreter().onecmd(action, self)