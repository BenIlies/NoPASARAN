class InterpreterParser():
    @staticmethod
    def parse(parameters, correct_number):
        parsed_parameters = parameters.split()
        if len(parsed_parameters) == correct_number:
            return parsed_parameters
        else:
            raise Exception('Parsing error: number of argument is incorrect expected ' + str(correct_number) + ' received ' + str(len(parsed_parameters)) + '.')