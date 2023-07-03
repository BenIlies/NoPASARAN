from nopasaran.decorators import parsing_decorator

class ConditionPrimitives:
    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def equal(inputs, outputs, state_variables):
        return state_variables[inputs[0]] == state_variables[inputs[1]]

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def gt(inputs, outputs, state_variables):
        return state_variables[inputs[0]] > state_variables[inputs[1]]

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def gte(inputs, outputs, state_variables):
        return state_variables[inputs[0]] >= state_variables[inputs[1]]

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def lt(inputs, outputs, state_variables):
        return state_variables[inputs[0]] < state_variables[inputs[1]]

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def lte(inputs, outputs, state_variables):
        return state_variables[inputs[0]] <= state_variables[inputs[1]]