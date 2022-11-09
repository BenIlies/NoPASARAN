class InterpreterParser():
    @staticmethod
    def parse(command, input_args=1, output_args=0, optional_inputs=False, optional_outputs=False):
        def checker(string):
            depth = 0
            for c in string:
                if  c == '(':
                    depth = depth + 1
                elif  c == ')':
                    depth = depth - 1
                elif c != ' ' and depth == 0:
                    raise Exception('Error value without parenthesis in ' + string + '.')
                if depth < 0:
                    raise Exception('Parenthesis closed without having one open in ' + string + '.')
                elif depth > 1:
                    raise Exception('Parenthesis can not be nested in ' + string + '.')
            if depth > 0:
                raise Exception('Number of closing and opening parenthesis are not matching in ' + string + '.')


        def parenthetic_contents(string):
            checker(string)
            stack = []
            for i, c in enumerate(string):
                if c == '(':
                    stack.append(i)
                elif c == ')' and stack:
                    start = stack.pop()
                    yield string[start + 1: i]

        
        set_of_arguments = 0
        if input_args != 0 or optional_inputs:
            set_of_arguments = set_of_arguments + 1
        if output_args != 0 or optional_outputs:
            set_of_arguments = set_of_arguments + 1
        args = list(parenthetic_contents(command))
        if len(args) > set_of_arguments:
            raise Exception('Mismatch in the input and output values in ' + command + ', got too many sets of arguments.')
        if len(args) < set_of_arguments:
            raise Exception('Mismatch in the input and output values in ' + command + ', got not enough sets of arguments.')

        if set_of_arguments == 2:
            inputs = args[0].split(' ')
            outputs = args[1].split(' ')
        elif set_of_arguments == 1:        
            if input_args == 0 and not(optional_inputs):
                inputs = []
                outputs = args[0].split(' ')
            else:
                inputs = args[0].split(' ')
                outputs = []
        else:
            inputs = []
            outputs = []

        if not(optional_inputs) and input_args != len(inputs):
            raise Exception('Number of inputs mismatch.')
        if not(optional_outputs) and output_args != len(outputs):  
            raise Exception('Number of outputs mismatch.')            
        return inputs, outputs