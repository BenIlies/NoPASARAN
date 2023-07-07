import logging

from functools import wraps

from nopasaran.parsers.interpreter_parser import Parser


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
        RuntimeError: If an error occurs while parsing or executing the function.
    """
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
                RuntimeError: If an error occurs while parsing or executing the function.
            """
            logging.debug("[Parsing] Primitive name: {}. Expecting {} input(s) and {} output(s). Optional inputs: {}. Optional outputs: {}"
                         .format(func.__name__, input_args, output_args, optional_inputs, optional_outputs))
            
            try:
                inputs, outputs = Parser.parse(line, input_args, output_args, optional_inputs, optional_outputs)
                logging.debug("[Parsing] Received inputs: {}. Received outputs: {}".format(inputs, outputs))
            except Exception as e:
                error_msg = "Error while parsing primitive '{}': {}".format(func.__name__, e)
                logging.error("[Parsing] " + error_msg)
                raise RuntimeError(error_msg)
            try:
                return func(inputs, outputs, variable_dict)
            except Exception as e:
                error_msg = "Error while executing primitive {}".format(func.__name__)
                logging.error("[Parsing] " + error_msg)
                raise RuntimeError(error_msg)
            
        return wrapper
    
    return decorator
