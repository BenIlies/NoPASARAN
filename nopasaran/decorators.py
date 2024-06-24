import logging
from functools import wraps

from nopasaran.parsers.interpreter_parser import Parser
from nopasaran.errors.parsing_error import ParsingError

def parsing_decorator(input_args, output_args, optional_inputs=False, optional_outputs=False):
    """
    Decorator for parsing inputs and outputs of a function.
    
    This decorator parses the inputs and outputs of a function based on the specified constraints.
    
    Args:
        input_args (int): The expected number of input arguments.
        output_args (int): The expected number of output arguments.
        optional_inputs (bool, optional): Whether optional inputs are allowed. Defaults to False.
        optional_outputs (bool, optional): Whether optional outputs are allowed. Defaults to False.
    
    Returns:
        function: The decorated function.
    
    Raises:
        ParsingError: If an error occurs while parsing or executing the function.
    """
    def handle_parsing_error(func, message):
        error_msg = f"Error while {message} '{func.__name__}'"
        logging.error("[Parsing] " + error_msg)
        raise ParsingError(error_msg)

    def decorator(func):
        @wraps(func)
        def wrapper(line, variable_dict):
            """
            Wrapper function for the decorator.
            
            This function parses the inputs and outputs, logs the details, and calls the decorated function.
            
            Args:
                line (str): The command line to parse.
                variable_dict (dict): The dictionary of variables.
            
            Returns:
                The result of the decorated function.
            
            Raises:
                ParsingError: If an error occurs while parsing or executing the function.
            """
            logging.debug("[Parsing] [Primitive - {}] Expecting {} input(s) and {} output(s). Optional inputs: {}. Optional outputs: {}"
                         .format(func.__name__, input_args, output_args, optional_inputs, optional_outputs))
            
            try:
                inputs, outputs = Parser.parse(line, input_args, output_args, optional_inputs, optional_outputs)
                logging.debug("[Parsing] [Primitive - {}] Received inputs: {}. Received outputs: {}".format(func.__name__, inputs, outputs))
            except ParsingError as e:
                handle_parsing_error(func, "parsing the command line")
            except Exception as e:
                handle_parsing_error(func, f"parsing the command line '{e}'")
            
            try:
                return func(inputs, outputs, variable_dict)
            except ParsingError as e:
                handle_parsing_error(func, "executing the function")
            except Exception as e:
                logging.error("[Execution] " + str(e))
                handle_parsing_error(func, "executing the function")

        return wrapper

    return decorator
