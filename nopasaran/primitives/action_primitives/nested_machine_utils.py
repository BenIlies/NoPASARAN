import json

from nopasaran.decorators import parsing_decorator

class NestedMachinePrimitives:
    """
    Class containing primitives for interacting with nested state machines.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0, optional_inputs=True, optional_outputs=True)
    def call(inputs, outputs, state_machine):
        """
        Load a nested machine identified by the given name and call its start method with the provided parameters.
        The mandatory input argument is the name of the nested state machine to call.
        The optional input arguments are the parameters assigned to the nested state machine.
        The optional output arguments are the values returned by the nested state machine and will be stored in the
        specified optional output variables. The number of optional output arguments should match the number of optional
        input arguments specified in the 'return_values' primitive used within the nested state machine.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: Yes

        Optional output arguments: Yes

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the nested state machine to call, and optional input arguments representing the parameters assigned to the nested state machine.
            
            outputs (List[str]): The list of output variable names. It contains the names of the variables where the returned values will be stored (optional).
            
            state_machine: The state machine object.

        Returns:
            None
        """
        nested_state_json = json.load(open('.'.join((inputs[0], 'json'))))
        parameters = []
        for nested_variables in inputs[1:]:
            parameters.append(state_machine.get_variable_value(nested_variables))
        nested_machine = state_machine.get_nested_machine(nested_state_json, parameters)
        nested_machine.start()
        for index in range(len(nested_machine.returned)):
            state_machine.set_variable_value(outputs[index], nested_machine.get_variable_value(nested_machine.returned[index]))

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0, optional_outputs=True)
    def get_parameters(inputs, outputs, state_machine):
        """
        Retrieve the parameters of the current nested state machine that were passed from the parent state machine
        using the 'call' primitive. These parameters are optional input arguments specified in the 'call' action of
        the parent state machine. The retrieved parameter values will be stored in the specified optional output
        arguments for further use within the nested machine. The number of optional input arguments in the 'call'
        primitive and the number of output arguments in 'get_parameters' should match.

        Number of input arguments: 0

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: Yes

        Args:
            inputs (List[str]): The list of input variable names.
            
            outputs (List[str]): The list of output variable names. It contains the names of the variables where the parameter values will be stored (optional).
            
            state_machine: The state machine object.

        Returns:
            None
        """
        for index in range(len(state_machine.parameters)):
            state_machine.set_variable_value(outputs[index], state_machine.parameters[index])

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0, optional_inputs=True, optional_outputs=False)
    def return_values(inputs, outputs, state_machine):
        """
        This primitive is used within a nested state machine. It enables you to specify the values that will be returned
        by the nested state machine when it completes its execution. The returned values can be used by the calling state
        machine for further processing or decision-making.

        Number of input arguments: 0

        Number of output arguments: 0

        Optional input arguments: Yes

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.returned = inputs