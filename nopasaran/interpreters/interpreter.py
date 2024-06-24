import cmd
import logging


class Interpreter(cmd.Cmd):
    """
    A base Interpreter class that inherits from cmd.Cmd.
    This class can be used as a generic interpreter.
    """

    @classmethod
    def evaluate(cls, line, variable, *function_classes):
        """
        Evaluate the input line using the provided variable and function classes.

        Args:
            line (str): The input line to evaluate.
            variable: The variable to use during evaluation.
            function_classes: Variable-length argument list of function classes.

        Returns:
            The result of the evaluation.
        """
        instance = cls()
        instance.function_classes = function_classes
        return instance.onecmd(line, variable)

    def onecmd(self, line, variable):
        """
        Run a single command with the provided line and variable.

        Args:
            line (str): The command line to execute.
            variable: The variable to use during execution.

        Returns:
            The result of the command execution.
        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line, variable)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line, variable)
        else:
            for function_class in self.function_classes:
                try:
                    func = getattr(function_class, cmd)
                    return func(arg, variable)
                except AttributeError:
                    continue
            logging.error('[Interpreter] Primitive not recognized: "{}"'.format(cmd))
            exit()

    def default(self, line, variable):
        """
        Handle the default behavior when an unknown command is encountered.

        Args:
            line (str): The unknown command line.
            variable: The variable to use during handling.

        Raises:
            Exception: Parsing error with the unknown argument.
        """
        raise Exception('Parsing error: argument "' + line + '" is unknown.')
