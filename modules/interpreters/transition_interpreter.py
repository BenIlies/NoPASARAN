import cmd

from modules.parsers.interpreter_parser import InterpreterParser


class TransitionInterpreter(cmd.Cmd):
    def onecmd(self, line, old_state_variables, new_state_variables):
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
        raise Exception('Parsing error: argument "' + line + '" is unknown.')

    def do_assign(self, line, old_state_variables, new_state_variables):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        new_state_variables[outputs[0]] = old_state_variables[inputs[0]]
