import uuid

def patch_xstate(array_to_to_parse, field):
            actions = ArrayParser.get_safe_array(array_to_to_parse[field])
            types = [action['type'] for action in actions]
            return types


class ArrayParser:
    """
    Parser class for handling arrays.
    
    This class provides methods to handle arrays in a safe manner.
    """

    @staticmethod
    def get_safe_array(key):
        """
        Get a safe array from the key.
        
        Args:
            key: The key to convert into an array.
        
        Returns:
            list: The converted array.
        """
        if isinstance(key, str):
            return [key]
        elif isinstance(key, dict):
            return [key]
        else:
            return key


class StateMachineParser:
    """
    Parser class for state machines.
    
    This class provides methods to parse state machine definitions.
    """

    def __init__(self, state_json):
        """
        Initialize the StateMachineParser.
        
        Args:
            state_json (dict): The JSON representation of the state machine.
        """
        self.id = state_json['id'] + '-' + uuid.uuid4().hex[:6]
        self.initial_state = state_json['initial']
        self.states = state_json['states']

    def get_id(self):
        """
        Get the ID of the state machine.
        
        Returns:
            str: The ID of the state machine.
        """
        return self.id
    
    def get_initial_state(self):
        """
        Get the initial state of the state machine.
        
        Returns:
            str: The initial state of the state machine.
        """
        return self.initial_state
    
    def get_states(self):
        """
        Get the list of states in the state machine.
        
        Returns:
            list: The list of states in the state machine.
        """
        return list(self.states.keys())

    def get_entry_actions(self, state):
        """
        Get the entry actions for a state.
        
        Args:
            state (str): The state for which to get the entry actions.
        
        Returns:
            list or None: The list of entry actions, or None if no entry actions are defined.
        """
        if 'entry' in self.states[state]:
            # Patching the changement of xstate discovered on th 9th of July 2023
            #return ArrayParser.get_safe_array(self.states[state]['entry'])
            return patch_xstate(self.states[state], 'entry')
        return None

    def get_exit_actions(self, state):
        """
        Get the exit actions for a state.
        
        Args:
            state (str): The state for which to get the exit actions.
        
        Returns:
            list or None: The list of exit actions, or None if no exit actions are defined.
        """
        if 'exit' in self.states[state]:
            # Patching the changement of xstate discovered on th 9th of July 2023
            #return ArrayParser.get_safe_array(self.states[state]['exit'])
            return patch_xstate(self.states[state], 'exit')
        return None

    def get_next_states_on_event(self, state, event):
        """
        Get the next states on an event for a state.
        
        Args:
            state (str): The state for which to get the next states.
            event (str): The event for which to get the next states.
        
        Returns:
            list or None: The list of next states, or None if no next states are defined for the event.
        """
        if 'on' in self.states[state] and event in self.states[state]['on']:
            return ArrayParser.get_safe_array(self.states[state]['on'][event])
        return None
    
    def get_conditions(self, possible_state):
        """
        Get the conditions for a possible state transition.
        
        Args:
            possible_state (dict): The possible state transition.
        
        Returns:
            dict or None: The conditions for the possible state transition, or None if no conditions are defined.
        """
        if 'cond' in possible_state:
            return possible_state['cond']
        return None

    def get_next_state_name(self, possible_state):
        """
        Get the name of the next state for a possible state transition.
        
        Args:
            possible_state (dict): The possible state transition.
        
        Returns:
            str or None: The name of the next state, or None if no next state is defined.
        """
        if 'target' in possible_state:
            return possible_state['target']
        return None

    def get_transition_actions(self, next_state):
        """
        Get the transition actions for a next state.
        
        Args:
            next_state (dict): The next state.
        
        Returns:
            list or None: The list of transition actions, or None if no transition actions are defined.
        """
        if 'actions' in next_state:
            # Patching the changement of xstate discovered on th 9th of July 2023
            #return ArrayParser.get_safe_array(next_state['actions'])
            return patch_xstate(next_state, 'actions')
        return None
