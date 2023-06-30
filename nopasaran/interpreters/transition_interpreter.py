import cmd

from nopasaran.parsers.interpreter_parser import InterpreterParser


class TransitionInterpreter(cmd.Cmd):
    """
    Custom TransitionInterpreter class inheriting from cmd.Cmd.
    This class interprets transition commands in the context of a command-line interface.
    """

    def onecmd(self, line, old_state_variables, new_state_variables):
        """
        Method to execute one command.
        Args:
            line (str): The line to parse.
            old_state_variables (dict): The state variables before transition.
            new_state_variables (dict): The state variables after transition.
        Returns:
            The return value of the function mapped to the command or error in default case.
        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF' :
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg, old_state_variables, new_state_variables)

    def default(self, line, old_state_variables, new_state_variables):
        """
        The method called on an input line when the command prefix is not recognized.
        Args:
            line (str): The line to parse.
            old_state_variables (dict): The state variables before transition.
            new_state_variables (dict): The state variables after transition.
        Raises:
            Exception: If the argument is unknown.
        """
        raise Exception('Parsing error: argument "' + line + '" is unknown.')

    def do_assign(self, line, old_state_variables, new_state_variables):
        """
        Method to assign value from old_state_variables to new_state_variables based on input from the line.
        Args:
            line (str): The line to parse, expected to contain one input and one output variable.
            old_state_variables (dict): The state variables before transition.
            new_state_variables (dict): The state variables after transition.
        """
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        new_state_variables[outputs[0]] = old_state_variables[inputs[0]]
