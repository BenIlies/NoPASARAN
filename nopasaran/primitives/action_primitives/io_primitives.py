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
    def write_to_file(inputs, outputs, state_machine):
        """
        Write the provided data to a file.

        Number of input arguments: 2

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the data to be written.
                - The name of the variable containing the file path.

            outputs (List[str]): The list of output variable names.

            state_machine: The state machine object.

        Returns:
            None
        """
        data = state_machine.get_variable_value(inputs[0])
        file_path = state_machine.get_variable_value(inputs[1])

        with open(file_path, "wb") as file:
            file.write(data)