from enum import Enum

from twisted.internet.threads import deferToThread

from modules.utils import *
from modules.interpreters.action_interpreter import ActionInterpreter
from modules.interpreters.condition_interpreter import ConditionInterpreter
from modules.interpreters.transition_interpreter import TransitionInterpreter
from modules.controllers.controller import ClientController, ServerController
from modules.sniffers.sniffer import Sniffer

class Command(Enum):
    EXECUTE_ACTION = 0
    ASSIGN_VARIABLES = 1
    SET_STATE = 2

class Machine:
    def __init__(self, xstate_json, parameters=[], main_state=True, controller_configuration=None):
        self.__id = xstate_json['id']
        self.__initial = xstate_json['initial']
        self.__states = xstate_json['states']
        self.__current_state = self.__initial
        self.__sniffer = Sniffer(self, filter='')
        self.__main_state = main_state
        self.__variables = {}
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
        self.__actions = []
        
    def start(self):
        if self.__main_state:
            deferToThread(self.controller.start)
        self.trigger('STARTED')
        while (len(self.__actions) > 0):
            self.execute(self.__actions[0])
            self.__actions.pop(0)

    def execute(self, action):
        if Command.EXECUTE_ACTION.name in action:
            ActionInterpreter().onecmd(action[Command.EXECUTE_ACTION], self)
        elif Command.ASSIGN_VARIABLES.name in action:
            self.set_variables(action[Command.ASSIGN_VARIABLES.name])
        elif Command.SET_STATE.name in action:
            self.set_state(action[Command.SET_STATE.name])

    def get_child_machine(self, nested_xstate_json , parameters):
        nested_machine = Machine(xstate_json=nested_xstate_json, main_state=False, parameters=parameters)
        nested_machine.root_machine = self.root_machine
        return nested_machine

    def get_id(self):
        return self.__id
    
    def get_state(self):
        return self.__current_state

    def set_state(self, state):
        self.__current_state = state

    def start_sniffer(self):
        self.__sniffer.start()

    def stop_sniffer(self):
        self.__sniffer.stop()

    def get_variables(self):
        return self.__variables

    def set_variables(self, variables):
        self.__variables = variables

    def get_variable(self, name):
        return self.__variables[name]

    def set_variable(self, name, new_value):
        self.__variables[name] = new_value
        
    def set_sniffer_filter(self, filter):
        self.__sniffer.set_filter(filter)

    def set_sniffer_queue(self, queue):
        self.__sniffer.queue = queue

    def add_redirection(self, event, state):
        self.__redirections[event] = state

    def trigger(self, event):
        if 'on' in self.__states[self.get_state()]:
            if event in self.__states[self.get_state()]['on']:
                self.__transition(get_safe_array(self.__states[self.get_state()]['on'][event]))
        elif event in self.__redirections:
            self.__append_exit_actions()
            self.__append_state(self.__redirections[event])
            self.__append_enter_actions(self.__redirections[event])
        else:
            print('SKIPPED: ' + event + ' triggered in state: ' + self.get_state() + '. No matching event.')

    def __transition(self, possible_states):
        def check_conditions(possible_state):
            if 'cond' in possible_state:
                return ConditionInterpreter().onecmd(possible_state['cond'], self.__variables)
            else:
                return True
            
        for state in possible_states:
            if state['target'] in self.__states:
                if check_conditions(state):
                    self.__append_exit_actions()
                    self.__append_variables(state)
                    self.__append_state(state['target'])
                    self.__append_enter_actions(state['target'])
                    break

    def __append_enter_actions(self, state):
        if 'entry' in self.__states[state]:
            for action in get_safe_array(self.__states[state]['entry']):
                self.__actions.append({Command.EXECUTE_ACTION.name: action})

    def __append_exit_actions(self):
        if 'exit' in self.__states[self.get_state()]:
            for action in get_safe_array(self.__states[self.get_state()]['exit']):
                self.__actions.append({Command.EXECUTE_ACTION.name: action})

    def __append_variables(self, state):
        variables = {}
        if 'actions' in state:
            transition_actions = get_safe_array(state['actions'])
            for transition_action in transition_actions:
                TransitionInterpreter().onecmd(transition_action, self.__variables, variables)
        self.__actions.append({Command.ASSIGN_VARIABLES.name: variables})

    def __append_state(self, state):
        self.__actions.append({Command.SET_STATE.name: state})