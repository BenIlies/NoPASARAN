
import time
import hashlib

from twisted.internet.threads import deferToThread

from modules.utils import *
from modules.interpreters.action_interpreter import ActionInterpreter
from modules.interpreters.condition_interpreter import ConditionInterpreter
from modules.interpreters.transition_interpreter import TransitionInterpreter
from modules.controllers.controller import ClientController, ServerController
from modules.sniffers.sniffer import Sniffer

class Machine:
    def __init__(self, xstate_json, parameters=[], main_state=True, controller_configuration=None):
        self.__id = xstate_json['id']
        self.__initial = xstate_json['initial']
        self.__states = xstate_json['states']
        self.__current_state = self.__initial
        self.__sniffer = Sniffer(self, filter='')
        self.__main_state = main_state
        self.__local_variables = {}
        self.__redirections = {}
        self.parameters = parameters
        if self.__main_state:
            self.root_machine = self
        else:
            self.root_machine = None     
        if controller_configuration and self.__main_state:
            if controller_configuration['role'] == 'client':
                self.controller = ClientController(self, controller_configuration['root_certificate'], controller_configuration['private_certificate'])
                self.controller.configure(controller_configuration['destination_ip'], int(controller_configuration['server_port']))
            elif controller_configuration['role'] == 'server':
                self.controller = ServerController(self, controller_configuration['root_certificate'], controller_configuration['private_certificate'])
                self.controller.configure(int(controller_configuration['server_port']))
        else:
            self.controller = None
        self.controller_protocol = None
        self.returned = None
        
    def start(self):
        if self.__main_state:
            deferToThread(self.controller.start)
        self.trigger('STARTED')
    
    def get_child_machine(self, nested_xstate_json , parameters):
        nested_machine = Machine(xstate_json=nested_xstate_json, main_state=False, parameters=parameters)
        nested_machine.root_machine = self.root_machine
        return nested_machine

    def get_id(self):
        return self.__id
    
    def get_state(self):
        return self.__current_state

    def start_sniffer(self):
        self.__sniffer.start()

    def stop_sniffer(self):
        self.__sniffer.stop()

    def get_variables(self):
        return self.__local_variables

    def get_variable(self, name):
        return self.__local_variables[name]

    def set_variable(self, name, new_value):
        self.__local_variables[name] = new_value
        
    def set_sniffer_filter(self, filter):
        self.__sniffer.set_filter(filter)

    def set_sniffer_queue(self, queue):
        self.__sniffer.queue = queue

    def add_redirection(self, event, state):
        self.__redirections[event] = state

    def trigger(self, event):
        if 'on' in self.__states[self.__current_state]:
            if event in self.__states[self.__current_state]['on']:
                self.__transition(get_safe_array(self.__states[self.__current_state]['on'][event]))
        elif event in self.__redirections:
            self.__exit_current_state()
            self.__current_state = self.__redirections[event]
            self.__enter_current_state()
        else:
            print('SKIPPED: ' + event + ' triggered in state: ' + self.__current_state + '. No matching event.')

    def __transition(self, possible_states):
        def check_conditions(possible_state):
            if 'cond' in possible_state:
                return ConditionInterpreter().onecmd(possible_state['cond'], self.__local_variables)
            else:
                return True
            
        for state in possible_states:
            if state['target'] in self.__states:
                if check_conditions(state):
                    self.__exit_current_state()
                    self.__assign_local_variables(state)
                    self.__current_state = state['target']
                    self.__enter_current_state()
                    break


    def __assign_local_variables(self, state):
        local_variables = {}
        if 'actions' in state:
            transition_actions = get_safe_array(state['actions'])
            for transition_action in transition_actions:
                TransitionInterpreter().onecmd(transition_action, self.__local_variables, local_variables)
        self.__local_variables = local_variables

    def __enter_current_state(self):
        if 'entry' in self.__states[self.__current_state]:
            for action in get_safe_array(self.__states[self.__current_state]['entry']):
                ActionInterpreter().onecmd(action, self)

    def __exit_current_state(self):
        if 'exit' in self.__states[self.__current_state]:
            for action in get_safe_array(self.__states[self.__current_state]['exit']):
                ActionInterpreter().onecmd(action, self)