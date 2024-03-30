import nopasaran.utils as utils
from nopasaran.decorators import parsing_decorator

class DataManipulationPrimitives:
    """
    Class containing data manipulation primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set(inputs, outputs, state_machine):
        """
        Set the value of an output variable in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No
        
        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the new value.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modification.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], inputs[0])

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set_integer(inputs, outputs, state_machine):
        """
        Set the integer value of an output variable in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No
        
        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the new integer.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable with the modification.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], int(inputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_random_int(inputs, outputs, state_machine):
        """
        Generate a random integer between two input values and store it in an output variable in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the lower bound and the upper bound.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the generated random integer.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.set_random_int(inputs[0], inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_random_float(inputs, outputs, state_machine):
        """
        Generate a random float between two input values and store it in an output variable in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the lower bound and the upper bound.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the generated random float.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.set_random_float(inputs[0], inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def pop(inputs, outputs, state_machine):
        """
        Remove the first element from a list stored in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of a variable representing the list.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.get_variable_value(inputs[0]).pop(0)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_first_element(inputs, outputs, state_machine):
        """
        Get the first element from a list stored in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                which is the name of a variable representing the list.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the first element.

            state_machine: The state machine object.

        Returns:
            None
        """
        input_list = state_machine.get_variable_value(inputs[0])
        first_element = input_list[0]
        state_machine.set_variable_value(outputs[0], first_element)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def increment(inputs, outputs, state_machine):
        """
        Increment the value of a variable stored in the machine's state by a specified amount.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of a variable representing the value to be incremented.
                - The amount by which the value should be incremented.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                The name of the variable to store the result of the increment operation.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        old_value = int(state_machine.get_variable_value(inputs[0]))
        increment_amount = int(inputs[1])
        incremented_value = old_value + increment_amount
        state_machine.set_variable_value(outputs[0], incremented_value)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def decrement(inputs, outputs, state_machine):
        """
        Decrement the value of a variable stored in the machine's state by a specified amount.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of a variable representing the value to be decremented.
                - The amount by which the value should be decremented.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                The name of the variable to store the result of the decrement operation.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        old_value = int(state_machine.get_variable_value(inputs[0]))
        decrement_amount = int(inputs[1])
        decremented_value = old_value - decrement_amount
        state_machine.set_variable_value(outputs[0], decremented_value)
