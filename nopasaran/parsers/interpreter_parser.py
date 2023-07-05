class Parser:
    """
    A class for parsing commands and validating arguments.
    """

    @staticmethod
    def _check_validity(string):
        """
        Check the validity of the string.
        
        This method checks whether the string has valid parentheses.
        
        Args:
            string (str): The string to check.
        
        Raises:
            RuntimeError: If the string contains a value without parentheses,
                closing parentheses without corresponding opening parentheses,
                or nested parentheses are not allowed.
        """
        depth = 0
        for c in string:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            elif c != ' ' and depth == 0:
                raise RuntimeError(f"Value without parentheses in '{string}'.")
            if depth < 0:
                raise RuntimeError(f"Closing parentheses without corresponding opening parentheses in '{string}'.")
            elif depth > 1:
                raise RuntimeError(f"Nested parentheses are not allowed in '{string}'.")
        if depth > 0:
            raise RuntimeError(f"Number of opening and closing parentheses does not match in '{string}'.")

    @staticmethod
    def _extract_arguments(string):
        """
        Extract arguments from the string.
        
        This method extracts the arguments enclosed in parentheses from the string.
        
        Args:
            string (str): The string to extract arguments from.
        
        Yields:
            str: Each extracted argument from the string.
        
        Raises:
            RuntimeError: If the string does not have valid parentheses.
        """
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
        """
        Parse the command and validate the arguments.
        
        This method parses the command and validates the number of input and output arguments
        based on the specified constraints.
        
        Args:
            command (str): The command to parse.
            input_args (int): The expected number of input arguments.
            output_args (int): The expected number of output arguments.
            optional_inputs (bool, optional): Whether optional inputs are allowed. Defaults to False.
            optional_outputs (bool, optional): Whether optional outputs are allowed. Defaults to False.
        
        Returns:
            tuple: A tuple containing two lists: the input arguments and the output arguments.
        
        Raises:
            RuntimeError: If the command has too many or too few argument sets,
                incorrect number of inputs or outputs, or if the arguments do not match the expected constraints.
        """
        args = list(Parser._extract_arguments(command))

        num_argument_sets = sum([input_args != 0 or optional_inputs, output_args != 0 or optional_outputs])

        if len(args) > num_argument_sets:
            raise RuntimeError(f"Too many argument sets in '{command}'. Expected: {num_argument_sets}.")
        if len(args) < num_argument_sets:
            raise RuntimeError(f"Not enough argument sets in '{command}'. Expected: {num_argument_sets}.")

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
            raise RuntimeError(f"Incorrect number of inputs in '{command}'. Expected: {input_args}.")
        if not optional_outputs and output_args != len(outputs):
            raise RuntimeError(f"Incorrect number of outputs in '{command}'. Expected: {output_args}.")

        return inputs, outputs
