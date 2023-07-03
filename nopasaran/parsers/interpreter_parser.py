from nopasaran.errors.command_error import InvalidCommandError

class Parser:
    @staticmethod
    def _check_validity(string):
        depth = 0
        for c in string:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            elif c != ' ' and depth == 0:
                raise InvalidCommandError(f"Value without parentheses in '{string}'.")
            if depth < 0:
                raise InvalidCommandError(f"Closing parentheses without corresponding opening parentheses in '{string}'.")
            elif depth > 1:
                raise InvalidCommandError(f"Nested parentheses are not allowed in '{string}'.")
        if depth > 0:
            raise InvalidCommandError(f"Number of opening and closing parentheses does not match in '{string}'.")

    @staticmethod
    def _extract_arguments(string):
        Parser._check_validity(string)
        stack = []
        for i, c in enumerate(string):
            if c == '(':
                stack.append(i)
            elif c == ')' and stack:
                start = stack.pop()
                yield string[start + 1: i]

    @staticmethod
    def parse(command, input_args, output_args, optional_inputs=False, optional_outputs=False):
        args = list(Parser._extract_arguments(command))

        num_argument_sets = sum([input_args != 0 or optional_inputs, output_args != 0 or optional_outputs])

        if len(args) > num_argument_sets:
            raise InvalidCommandError(f"Too many argument sets in '{command}'. Expected: {num_argument_sets}.")
        if len(args) < num_argument_sets:
            raise InvalidCommandError(f"Not enough argument sets in '{command}'. Expected: {num_argument_sets}.")

        inputs, outputs = [], []

        if num_argument_sets == 2:
            inputs = args[0].split()
            outputs = args[1].split()
        elif num_argument_sets == 1:
            if input_args == 0 and not optional_inputs:
                outputs = args[0].split()
            else:
                inputs = args[0].split()

        if not optional_inputs and input_args != len(inputs):
            raise InvalidCommandError(f"Incorrect number of inputs in '{command}'. Expected: {input_args}.")
        if not optional_outputs and output_args != len(outputs):
            raise InvalidCommandError(f"Incorrect number of outputs in '{command}'. Expected: {output_args}.")

        return inputs, outputs