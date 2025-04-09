# checks.py
# This file contains the functions that are used to verify the frames
# Each function takes an event and a set of parameters and returns a boolean
# If the test does not apply to the event, the function should return None
# If the test passes, the function should return True
# If the test fails, the function should return False

def check_header_field(event, name, value=None):
    """
    Check if a header field exists and optionally check its value.
    
    Args:
        event: The event containing headers
        name: The header name to check for
        value: Optional value to match against. If None, only checks header presence
    
    Returns:
        - True if:
            * value is None and header is found
            * value is provided and matches the header value
        - False if:
            * header is not found
            * value is provided but doesn't match
        - None if the event doesn't have headers
    """
    if hasattr(event, 'headers'):
        for header_name, header_value in event.headers:
            if header_name == name:
                if value is None:
                    return True
                return header_value == value
        return False
    return None

function_map = {
    'check_header_field': check_header_field
}