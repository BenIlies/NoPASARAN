import logging

from nopasaran.parsers.interpreter_parser import Parser

def parsing_decorator(input_args, output_args, optional_inputs=False, optional_outputs=False):
    def decorator(func):
        def wrapper(line, variable_dict):
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
