import cmd
from modules.parsers.interpreter_parser import InterpreterParser

class ConditionInterpreter(cmd.Cmd):
    """
    Custom ConditionInterpreter class inheriting from cmd.Cmd.
    This class interprets conditions in the context of a command-line interface.
    """
    def onecmd(self, line, variables):
        """
        Method to execute one command.
        Args:
            line (str): The line to parse.
            variables (dict): The variables to use.
        Returns:
            The return value of the function mapped to the command or error in default case.
        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'if_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg, variables)

    def default(self, line, variables):
        """
        The method called on an input line when the command prefix is not recognized.
        Args:
            line (str): The line to parse.
            variables (dict): The variables to use.
        Raises:
            Exception: If the argument is unknown.
        """
        raise Exception('Parsing error: argument "' + line + '" is unknown.')

    def if_equal(self, line, variables):
        """
        Method to evaluate equality condition.
        Args:
            line (str): The line to parse, expected to contain two variables for the condition.
            variables (dict): The dictionary containing variable names and their corresponding values.
        Returns:
            bool: True if the two variables are equal, False otherwise.
        """
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        if variables[inputs[0]] == variables[inputs[1]]:
            return True
        else:
            return False

    def if_gt(self, line, variables):
        """
        Method to evaluate greater than condition.
        Args:
            line (str): The line to parse, expected to contain two variables for the condition.
            variables (dict): The dictionary containing variable names and their corresponding values.
        Returns:
            bool: True if the first variable is greater than the second, False otherwise.
        """
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        if variables[inputs[0]] > variables[inputs[1]]:
            return True
        else:
            return False

    def if_gte(self, line, variables):
        """
        Method to evaluate greater than or equal to condition.
        Args:
            line (str): The line to parse, expected to contain two variables for the condition.
            variables (dict): The dictionary containing variable names and their corresponding values.
        Returns:
            bool: True if the first variable is greater than or equal to the second, False otherwise.
        """
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        if variables[inputs[0]] >= variables[inputs[1]]:
            return True
        else:
            return False

    def if_lt(self, line, variables):
        """
        Method to evaluate less than condition.
        Args:
            line (str): The line to parse, expected to contain two variables for the condition.
            variables (dict): The dictionary containing variable names and their corresponding values.
        Returns:
            bool: True if the first variable is less than the second, False otherwise.
        """
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        if variables[inputs[0]] < variables[inputs[1]]:
            return True
        else:
            return False

    def if_lte(self, line, variables):
        """
        Method to evaluate less than or equal to condition.
        Args:
            line (str): The line to parse, expected to contain two variables for the condition.
            variables (dict): The dictionary containing variable names and their corresponding values.
        Returns:
            bool: True if the first variable is less than or equal to the second, False otherwise.
        """
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        if variables[inputs[0]] <= variables[inputs[1]]:
            return True
        else:
            return False
