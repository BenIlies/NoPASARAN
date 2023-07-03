import cmd

class Interpreter(cmd.Cmd):
    """
    A base Interpreter class that inherits from cmd.Cmd.
    This class can be used as a generic interpreter.
    """

    @classmethod
    def evaluate(cls, line, variable, *function_classes):
        instance = cls()
        instance.function_classes = function_classes
        return instance.onecmd(line, variable)

    def onecmd(self, line, variable):
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
            return self.default(line, variable)

    def default(self, line, variable):
        raise Exception('Parsing error: argument "' + line + '" is unknown.')
