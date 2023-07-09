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
        """
        Initialize the StateMachine.

        Args:
            state_json (dict): The JSON representation of the state machine.
            parameters (list, optional): The parameters for the state machine. Defaults to [].
            root_state_machine (StateMachine, optional): The root state machine. Defaults to None.
        """
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
        logging.info('[State Machine - {}] Parameters received: {}'.format(self.machine_id, parameters))
        logging.debug('[State Machine - {}] Initialized.'.format(self.machine_id))

    def start(self):
        """
        Start the state machine and execute actions.
        """
        logging.debug('[State Machine - {}] Starting machine.'.format(self.machine_id))
        self.trigger_event(EventNames.STARTED.name)
        while True:
            next_action = self.actions.dequeue_next_action()
            if next_action is None:
                logging.warning('[State Machine - {}] Dequeue returned None. Stopping.'.format(self.machine_id))
                break
            self.execute_action(next_action)

    def execute_action(self, action):
        """
        Execute an action.

        Args:
            action (dict): The action to execute.
        """
        logging.debug('[State Machine - {}] Executing action: {}'.format(self.machine_id, action))
        if Command.EXECUTE_ACTION.name in action:
            ActionInterpreter.evaluate(action[Command.EXECUTE_ACTION.name], self)
        elif Command.ASSIGN_VARIABLES.name in action:
            self.assign_variables(action[Command.ASSIGN_VARIABLES.name])
            logging.info('[State Machine - {}] Variables assigned: {}'.format(self.machine_id, self.variables))
        elif Command.SET_STATE.name in action:
            self.update_state(action[Command.SET_STATE.name])

    def get_nested_machine(self, nested_state_json, parameters):
        """
        Get a nested state machine.

        Args:
            nested_state_json (dict): The JSON representation of the nested state machine.
            parameters (list): The parameters for the nested state machine.

        Returns:
            StateMachine: The nested state machine.
        """
        logging.debug('[State Machine - {}] Getting nested finite state machine.'.format(self.machine_id))
        nested_machine = StateMachine(state_json=nested_state_json, parameters=parameters, root_state_machine=self.root_state_machine)
        return nested_machine

    def update_state(self, state):
        """
        Update the current state of the state machine.

        Args:
            state (str): The new state.
        """
        logging.debug('[State Machine - {}] Setting state to: {}'.format(self.machine_id, state))
        self.current_state = state

    def start_sniffer(self):
        """
        Start the sniffer for the state machine.
        """
        logging.debug('Starting sniffer for machine with ID: {}'.format(self.machine_id))
        self.sniffer.start()

    def stop_sniffer(self):
        """
        Stop the sniffer for the state machine.
        """
        logging.debug('Stopping sniffer for machine with ID: {}'.format(self.machine_id))
        self.sniffer.stop()

    def assign_variables(self, variables):
        """
        Assign variables to the state machine.

        Args:
            variables (dict): The variables to assign.
        """
        logging.debug('[State Machine - {}] Setting variables: {}'.format(self.machine_id, variables))
        self.variables = variables

    def set_variable_value(self, name, new_value):
        """
        Set the value of a variable.

        Args:
            name (str): The name of the variable.
            new_value: The new value for the variable.
        """
        logging.info('[State Machine - {}] Setting variable {} to: {}'.format(self.machine_id, name, new_value))
        self.variables[name] = new_value

    def get_variable_value(self, variable_name):
        """
        Get the value of a variable.

        Args:
            variable_name (str): The name of the variable.

        Returns:
            The value of the variable.
        """
        if variable_name not in self.variables:
            logging.error('[State Machine - {}] Variable {} does not exist.'.format(self.machine_id, variable_name))
        return self.variables[variable_name]

    def update_variable_value(self, variable_name, new_value):
        """
        Update the value of a variable.

        Args:
            variable_name (str): The name of the variable.
            new_value: The new value for the variable.
        """
        logging.info('[State Machine - {}] Updating variable {} to: {}'.format(self.machine_id, variable_name, new_value))
        self.variables[variable_name] = new_value

    def update_sniffer_filter(self, filter):
        """
        Update the filter for the sniffer.

        Args:
            filter (str): The new filter.
        """
        self.sniffer.set_filter(filter)

    def update_sniffer_queue(self, queue):
        """
        Update the queue for the sniffer.

        Args:
            queue: The new queue.
        """
        self.sniffer.queue = queue

    def add_redirection(self, event, state):
        """
        Add a redirection from an event to a state.

        Args:
            event (str): The event to redirect.
            state (str): The state to redirect to.
        """
        logging.debug('[State Machine - {}] Adding redirection from event {} to state {}.'.format(self.machine_id, event, state))
        self.redirections[event] = state

    def trigger_event(self, event):
        """
        Trigger an event.

        Args:
            event (str): The event to trigger.
        """
        logging.debug('[State Machine - {}] Event {} triggered'.format(self.machine_id, event))
        next_states = self.state_machine_parser.get_next_states_on_event(self.current_state, event)
        if next_states is not None:
            self.make_transition(next_states)
        elif event in self.redirections:
            self.add_transition_actions(self.redirections[event])
        else:
            logging.warning('[State Machine - {}] No matching event for {}. Skipping.'.format(self.machine_id, event))

    def add_transition_actions(self, next_state_name, assignable=False, state=None):
        """
        Add transition actions for the next state.

        Args:
            next_state_name (str): The name of the next state.
            assignable (bool, optional): Whether the transition is assignable. Defaults to False.
            state (dict, optional): The state transition. Defaults to None.
        """
        self.actions.add_exit_actions(self.state_machine_parser.get_exit_actions(self.current_state))
        if assignable and state is not None:
            self.actions.assign_transition_variables(self.variables, self.state_machine_parser.get_transition_actions(state))
        self.actions.update_state(next_state_name)
        self.actions.add_entry_actions(self.state_machine_parser.get_entry_actions(next_state_name))

    def make_transition(self, possible_states):
        """
        Make a state transition.

        Args:
            possible_states (list): The possible states for the transition.
        """
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