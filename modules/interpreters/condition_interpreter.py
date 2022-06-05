import cmd

from modules.parsers.interpreter_parser import InterpreterParser


class ConditionInterpreter(cmd.Cmd):
    def onecmd(self, line, variables):
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
            return func(arg, variables)

    def default(self, line, variables):
        raise Exception('Parsing error: argument "' + line + '" is unknown.')

    def do_equal(self, line, variables):
        parsed = InterpreterParser.parse(line, 2)
        if variables[parsed[0]] == parsed[1]:
            return True
        else:
            return False

    def do_gt(self, line, variables):
        parsed = InterpreterParser.parse(line, 2)
        if variables[parsed[0]] > parsed[1]:
            return True
        else:
            return False

    def do_gte(self, line, variables):
        parsed = InterpreterParser.parse(line, 2)
        if variables[parsed[0]] >= parsed[1]:
            return True
        else:
            return False

    def do_it(self, line, variables):
        parsed = InterpreterParser.parse(line, 2)
        if variables[parsed[0]] < parsed[1]:
            return True
        else:
            return False

    def do_ite(self, line, variables):
        parsed = InterpreterParser.parse(line, 2)
        if variables[parsed[0]] <= parsed[1]:
            return True
        else:
            return False

    def do_equal(self, line, variables):
        parsed = InterpreterParser.parse(line, 2)
        if variables[parsed[0]] == parsed[1]:
            return True
        else:
            return False
