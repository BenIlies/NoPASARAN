# checks.py
# This file contains the functions that are used to verify the frames
# Each function takes an event and a set of parameters and returns a boolean
# If the test does not apply to the event, the function should return None
# If the test passes, the function should return True
# If the test fails, the function should return False

def check_header_field(event, name, value = None):
    if hasattr(event, 'headers'):
        for header in event.headers:
            if header.name == name:
                if value is None:
                    return True
                elif header.value == value:
                    return True
                else:
                    return False
    return None

function_map = {
    'check_header_field': check_header_field
}