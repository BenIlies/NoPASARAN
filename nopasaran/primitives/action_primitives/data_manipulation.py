import nopasaran.utils as utils
from nopasaran.decorators import parsing_decorator
import json

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
        increment_amount = int(state_machine.get_variable_value(inputs[1]))
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
        decrement_amount = int(state_machine.get_variable_value(inputs[1]))
        decremented_value = old_value - decrement_amount
        state_machine.set_variable_value(outputs[0], decremented_value)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def divide(inputs, outputs, state_machine):
        """
        Divide the value of a variable stored in the machine's state by a specified divisor.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of a variable representing the numerator.
                - The divisor by which the numerator should be divided.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                The name of the variable to store the result of the division operation.
            
            state_machine: The state machine object.

        Returns:
            None

        Raises:
            ValueError: If the divisor is zero.
        """
        numerator = int(state_machine.get_variable_value(inputs[0]))
        divisor = int(state_machine.get_variable_value(inputs[1]))
        if divisor == 0:
            raise ValueError("Division by zero is not allowed.")
        divided_value = numerator // divisor
        state_machine.set_variable_value(outputs[0], divided_value)



    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_dict(inputs, outputs, state_machine):
        """
        Create an empty dictionary and store it in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): No input arguments.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the empty dictionary.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], {})


    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_element_to_dict(inputs, outputs, state_machine):
        """
        Add an element to a dictionary stored in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the dictionary variable.
                - The name of the variable whose value will be added as the value in the dictionary.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the dictionary variable to store the updated dictionary.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        dictionary = state_machine.get_variable_value(inputs[0])
        key = inputs[1]
        value = state_machine.get_variable_value(key)
        dictionary[key] = value
        state_machine.set_variable_value(outputs[0], dictionary)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def remove_element_from_dict(inputs, outputs, state_machine):
        """
        Remove an element from a dictionary stored in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the dictionary variable.
                - The name of the variable whose value will be removed from the dictionary.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the dictionary variable to store the updated dictionary.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        dictionary = state_machine.get_variable_value(inputs[0])
        key = inputs[1]
        
        if key in dictionary:
            del dictionary[key]
        
        state_machine.set_variable_value(outputs[0], dictionary)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def string_to_integer(inputs, outputs, state_machine):
        """
        Convert a string value to an integer and store it in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                which is the name of a variable containing the string to be converted.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the converted integer.

            state_machine: The state machine object.

        Returns:
            None

        Raises:
            ValueError: If the input string cannot be converted to an integer.
        """
        try:
            integer_value = int(state_machine.get_variable_value(inputs[0]))
            state_machine.set_variable_value(outputs[0], integer_value)
        except ValueError:
            raise ValueError(f"Cannot convert value {state_machine.get_variable_value(inputs[0])} to an integer.")
        
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def fetch_element_from_dict(inputs, outputs, state_machine):
        """
        Fetch an element from a dictionary stored in the machine's state.

        Number of input arguments: 2
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the dictionary variable.
                - The name of the key whose value needs to be retrieved.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, 
                which is the name of the variable to store the retrieved value.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        dictionary = state_machine.get_variable_value(inputs[0])
        key = inputs[1]
        
        # Fetch the value from the dictionary
        value = dictionary.get(key, None)  # Returns None if key does not exist
        
        # Store the retrieved value in the state machine
        state_machine.set_variable_value(outputs[0], value)



    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def fetch_value_from_json_list(inputs, outputs, state_machine):
        """
        Fetch a specific key's value from a JSON list stored in a separate file at a given index.

        Number of input arguments: 3
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The file path of the JSON list.
                - The name of the variable storing the index.
                - The name of the variable storing the key to be retrieved.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the retrieved value.

            state_machine: The state machine object.

        Returns:
            None
        """
        file_path = inputs[0]  # Path to JSON file
        index_variable = state_machine.get_variable_value(inputs[1])  # Get index from state
        key_variable = state_machine.get_variable_value(inputs[2])  # Get key from state

        # Load JSON list from file
        try:
            with open(file_path, "r") as file:
                json_list = json.load(file)
        except Exception as e:
            raise ValueError(f"Error reading JSON file: {e}")

        # Validate JSON list type
        if not isinstance(json_list, list):
            raise ValueError(f"Expected a list in JSON file, but got {type(json_list).__name__}")

        try:
            index = int(index_variable)  # Convert index to an integer inside the function
        except ValueError:
            raise ValueError(f"Index must be an integer, but got: {index_variable}")

        # Ensure key is a string
        if not isinstance(key_variable, str):
            raise ValueError(f"Expected key to be a string, but got {type(key_variable).__name__}")

        # Validate index range
        if index < 0 or index >= len(json_list):
            raise IndexError(f"Index {index} is out of range for the JSON list.")

        # Retrieve the value for the given key
        value = json_list[index].get(key_variable, None)

        # Store the retrieved value in the state machine
        state_machine.set_variable_value(outputs[0], value)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_json_list_length(inputs, outputs, state_machine):
        """
        Get the length of a JSON list stored in a separate file.

        Number of input arguments: 1
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The file path of the JSON list.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                which is the name of the variable to store the length of the list.

            state_machine: The state machine object.

        Returns:
            None
        """
        file_path = inputs[0]  # Path to JSON file

        # Load JSON list from file
        try:
            with open(file_path, "r") as file:
                json_list = json.load(file)
        except Exception as e:
            raise ValueError(f"Error reading JSON file: {e}")

        # Validate JSON list type
        if not isinstance(json_list, list):
            raise ValueError(f"Expected a list in JSON file, but got {type(json_list).__name__}")

        # Get the length of the list
        list_length = len(json_list)

        # Store the length in the state machine
        state_machine.set_variable_value(outputs[0], list_length)
