from nopasaran.interpreters.transition_interpreter import TransitionInterpreter
from nopasaran.definitions.transitions import StateDuringTransition
from nopasaran.definitions.commands import Command


class ActionQueue:
    """
    Queue for managing actions during state transitions.
    
    This queue is responsible for storing and managing actions to be executed during state transitions.
    """

    def __init__(self):
        """
        Initialize the ActionQueue.
        """
        self.action_list = []

    def __enqueue_action(self, action):
        """
        Enqueue an action.
        
        Args:
            action: The action to enqueue.
        """
        self.action_list.append(action)

    def dequeue_next_action(self):
        """
        Dequeue the next action.
        
        Returns:
            The dequeued action, or None if the queue is empty.
        """
        if self.action_list:
            action = self.action_list.pop(0)
            return action
        return None

    def add_entry_actions(self, entry_actions):
        """
        Add entry actions to the queue.
        
        Args:
            entry_actions (list): The list of entry actions to add.
        """
        if entry_actions is not None:
            for action in entry_actions:
                self.__enqueue_action({Command.EXECUTE_ACTION.name: action})

    def add_exit_actions(self, exit_actions):
        """
        Add exit actions to the queue.
        
        Args:
            exit_actions (list): The list of exit actions to add.
        """
        if exit_actions is not None:
            for action in exit_actions:
                self.__enqueue_action({Command.EXECUTE_ACTION.name: action})

    def assign_transition_variables(self, old_state_variables, transition_actions):
        """
        Assign transition variables and evaluate transition actions.
        
        This method assigns the old and new state variables and evaluates the transition actions.
        
        Args:
            old_state_variables (dict): The variables from the old state.
            transition_actions (list): The list of transition actions to evaluate.
        """
        state_variables = {
            StateDuringTransition.OLD_STATE.name: old_state_variables,
            StateDuringTransition.NEW_STATE.name: {},
        }
        if transition_actions is not None:
            for transition_action in transition_actions:
                TransitionInterpreter.evaluate(transition_action, state_variables)
        self.__enqueue_action({Command.ASSIGN_VARIABLES.name: state_variables[StateDuringTransition.NEW_STATE.name]})

    def update_state(self, state_name):
        """
        Update the state.
        
        Args:
            state_name (str): The name of the new state.
        """
        self.__enqueue_action({Command.SET_STATE.name: state_name})
