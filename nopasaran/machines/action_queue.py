from nopasaran.interpreters.transition_interpreter import TransitionInterpreter
from nopasaran.definitions.transitions import StateDuringTransition
from nopasaran.definitions.commands import Command

class ActionQueue:
    def __init__(self):
        self.action_list = []

    def __enqueue_action(self, action):
        self.action_list.append(action)

    def dequeue_next_action(self):
        if self.action_list:
            action = self.action_list.pop(0)
            return action
        return None

    def add_entry_actions(self, entry_actions):
        if entry_actions is not None:
            for action in entry_actions:
                self.__enqueue_action({Command.EXECUTE_ACTION.name: action})

    def add_exit_actions(self, exit_actions):
        if exit_actions is not None:
            for action in exit_actions:
                self.__enqueue_action({Command.EXECUTE_ACTION.name: action})
                
    def assign_transition_variables(self, old_state_variables, transition_actions):
        state_variables = {
            StateDuringTransition.OLD_STATE.name: old_state_variables,
            StateDuringTransition.NEW_STATE.name: {},
        }
        if transition_actions is not None:
            for transition_action in transition_actions:
                TransitionInterpreter.evaluate(transition_action, state_variables)
        self.__enqueue_action({Command.ASSIGN_VARIABLES.name: state_variables[StateDuringTransition.NEW_STATE.name]})

    def update_state(self, state_name):
        self.__enqueue_action({Command.SET_STATE.name: state_name})
