import uuid

class ArrayParser:
    @staticmethod
    def get_safe_array(key):
        if isinstance(key, str):
            return [key]
        elif isinstance(key, dict):
            return [key]
        else:
            return key

class StateMachineParser:
    def __init__(self, state_json):
        self.id = state_json['id'] + '-' + uuid.uuid4().hex[:6]
        self.initial_state = state_json['initial']
        self.states = state_json['states']

    def get_id(self):
        return self.id
    
    def get_initial_state(self):
        return self.initial_state
    
    def get_states(self):
        return list(self.states.keys())

    def get_entry_actions(self, state):
        if 'entry' in self.states[state]:
            return ArrayParser.get_safe_array(self.states[state]['entry'])
        return None

    def get_exit_actions(self, state):
        if 'exit' in self.states[state]:
            return ArrayParser.get_safe_array(self.states[state]['exit'])
        return None

    def get_next_states_on_event(self, state, event):
        if 'on' in self.states[state] and event in self.states[state]['on']:
            return ArrayParser.get_safe_array(self.states[state]['on'][event])
        return None
    
    def get_conditions(self, possible_state):
        if 'cond' in possible_state:
            return possible_state['cond']
        return None

    def get_next_state_name(self, possible_state):
        if 'target' in possible_state:
            return possible_state['target']
        return None

    def get_transition_actions(self, next_state):
        if 'actions' in next_state:
            return ArrayParser.get_safe_array(next_state['actions'])
        return None