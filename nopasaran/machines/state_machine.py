import logging

from nopasaran.utils import *
from nopasaran.machines.action_queue import ActionQueue
from nopasaran.interpreters.action_interpreter import ActionInterpreter
from nopasaran.interpreters.condition_interpreter import ConditionInterpreter
from nopasaran.sniffers.sniffer import Sniffer
from nopasaran.parsers.state_machine_parser import StateMachineParser
from nopasaran.definitions.events import EventNames
from nopasaran.definitions.commands import Command


class StateMachine:
    def __init__(self, state_json, parameters=[], root_state_machine=None):
        self.state_machine_parser = StateMachineParser(state_json)
        self.machine_id = self.state_machine_parser.get_id()
        self.current_state = self.state_machine_parser.get_initial_state()
        self.sniffer = Sniffer(self, filter='')
        self.variables = {}
        self.redirections = {}
        self.parameters = parameters
        self.root_state_machine = self if root_state_machine is None else root_state_machine
        self.returned_value = None
        self.actions = ActionQueue()
        logging.info('Parameters received: {}'.format(parameters))
        logging.debug('Machine ID: {}. Initialized.'.format(self.machine_id))

    def start(self):
        logging.debug('Machine ID: {}. Starting machine.'.format(self.machine_id))
        self.trigger_event(EventNames.STARTED.name)
        while True:
            next_action = self.actions.dequeue_next_action()
            if next_action is None:
                logging.warning('Machine ID: {}. Dequeue returned None. Stopping.'.format(self.machine_id))
                break
            logging.debug('Executing action: {}'.format(next_action))
            self.execute_action(next_action)

    def execute_action(self, action):
        logging.debug('Machine ID: {}: Executing action: {}'.format(self.machine_id, action))
        if Command.EXECUTE_ACTION.name in action:
            ActionInterpreter.evaluate(action[Command.EXECUTE_ACTION.name], self)
        elif Command.ASSIGN_VARIABLES.name in action:
            self.assign_variables(action[Command.ASSIGN_VARIABLES.name])
            logging.info('Machine ID: {}: Variables assigned: {}'.format(self.machine_id, self.variables))
        elif Command.SET_STATE.name in action:
            self.update_state(action[Command.SET_STATE.name])

    def get_nested_machine(self, nested_state_json, parameters):
        logging.debug('Machine ID: {}: Getting nested finite state machine.'.format(self.machine_id))
        nested_machine = StateMachine(state_json=nested_state_json, parameters=parameters, root_state_machine=self.root_state_machine)
        return nested_machine

    def update_state(self, state):
        logging.debug('Machine ID: {}: Setting state to: {}'.format(self.machine_id, state))
        self.current_state = state

    def start_sniffer(self):
        logging.debug('Starting sniffer for machine with ID: {}'.format(self.machine_id))
        self.sniffer.start()

    def stop_sniffer(self):
        logging.debug('Stopping sniffer for machine with ID: {}'.format(self.machine_id))
        self.sniffer.stop()

    def assign_variables(self, variables):
        logging.debug('Machine ID: {}: Setting variables: {}'.format(self.machine_id, variables))
        self.variables = variables

    def set_variable_value(self, name, new_value):
        logging.info('Machine ID: {}: Setting variable {} to: {}'.format(self.machine_id, name, new_value))
        self.variables[name] = new_value

    def get_variable_value(self, variable_name):
        if variable_name not in self.variables:
            logging.error('Machine ID: {}: Variable {} does not exist.'.format(self.machine_id, variable_name))
        return self.variables[variable_name]

    def update_variable_value(self, variable_name, new_value):
        logging.info('Machine ID: {}: Updating variable {} to: {}'.format(self.machine_id, variable_name, new_value))
        self.variables[variable_name] = new_value

    def update_sniffer_filter(self, filter):
        self.sniffer.set_filter(filter)

    def update_sniffer_queue(self, queue):
        self.sniffer.queue = queue

    def add_redirection(self, event, state):
        logging.debug('Machine ID: {}: Adding redirection from event {} to state {}.'.format(self.machine_id, event, state))
        self.redirections[event] = state

    def trigger_event(self, event):
        logging.debug('Machine ID: {}: Event {} triggered'.format(self.machine_id, event))
        next_states = self.state_machine_parser.get_next_states_on_event(self.current_state, event)
        if next_states is not None:
            self.make_transition(next_states)
        elif event in self.redirections:
            self.add_transition_actions(self.redirections[event])
        else:
            logging.warning('Machine ID: {}: No matching event for {}. Skipping.'.format(self.machine_id, event))

    def add_transition_actions(self, next_state_name, assignable=False, state=None):
        self.actions.add_exit_actions(self.state_machine_parser.get_exit_actions(self.current_state))
        if assignable and state is not None:
            self.actions.assign_transition_variables(self.variables, self.state_machine_parser.get_transition_actions(state))
        self.actions.update_state(next_state_name)
        self.actions.add_entry_actions(self.state_machine_parser.get_entry_actions(next_state_name))

    def make_transition(self, possible_states):
        def validate_conditions(conditions):
            if conditions is not None:
                return ConditionInterpreter.evaluate(conditions, self.variables)
            else:
                return True

        for state in possible_states:
            next_state_name = self.state_machine_parser.get_next_state_name(state)
            if next_state_name is not None and next_state_name in self.state_machine_parser.get_states():
                conditions = self.state_machine_parser.get_conditions(state)
                if validate_conditions(conditions):
                    self.add_transition_actions(next_state_name, assignable=True, state=state)
                    break