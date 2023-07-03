import logging
import sys

from nopasaran.parsers.interpreter_parser import Parser

def parsing_decorator(input_args, output_args, optional_inputs=False, optional_outputs=False):
    def decorator(func):
        def wrapper(line, variable_dict_dict):
            logging.info("Primitive: {}. Expecting {} input(s) and {} output(s). Optional inputs: {}. Optional outputs: {}"
                         .format(func.__name__, input_args, output_args, optional_inputs, optional_outputs))
            
            try:
                inputs, outputs = Parser.parse(line, input_args, output_args, optional_inputs, optional_outputs)
                logging.debug("Received inputs: {}. Received outputs: {}".format(inputs, outputs))
            except Exception as e:
                logging.error("Error while parsing primitive '{}': {}".format(func.__name__, e))
                sys.exit("Error while parsing primitive '{}': {}".format(func.__name__, e))
            
            try:
                return func(inputs, outputs, variable_dict_dict)
            except Exception as e:
                logging.error("Error while executing primitive {}: {}".format(func.__name__, e))
                sys.exit("Error while executing primitive {}: {}".format(func.__name__, e))
            
        return wrapper
    return decorator
