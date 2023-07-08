from nopasaran.primitives.primitives import Primitives
from nopasaran.primitives.condition_primitives.variables_condition_primitives import VariablesConditionPrimitives

class ConditionPrimitives(Primitives):
    """
    Class containing condition primitives for the state machine.
    """
    classes = [VariablesConditionPrimitives]
