from nopasaran.primitives.primitives import Primitives
from nopasaran.primitives.condition_primitives.variable_comparisons import VariableComparisons

class ConditionPrimitives(Primitives):
    """
    Class containing condition primitives for the state machine.
    """
    classes = [VariableComparisons]
