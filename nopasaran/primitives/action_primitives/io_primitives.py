import json

from nopasaran.decorators import parsing_decorator

class IOPrimitives:
    """
    Class containing IO primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def get_from_file(inputs, outputs, state_machine):
        """
        Load variables from a file and store them in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the file path and the name of the variable to store the loaded variables.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable where the loaded variables will be stored.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        file_variables = json.load(open('.'.join((inputs[0], 'json'))))
        state_machine.set_variable_value(outputs[0], file_variables[inputs[1]])

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def print_to_file(inputs, outputs, state_machine):
        """
        Load variables from a file and store them in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the file path and the name of the variable whose contents are to be appended to the file.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """

        with open(inputs[0], 'a') as file:
            file.write(inputs[1] + "\n")
