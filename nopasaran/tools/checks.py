# checks.py
# This file contains the functions that are used to verify the frames
# Each function takes an event and a set of parameters and returns a boolean
# True means the check passed, False means it failed
# A check is considered passed if the params passed are all true

def verifyregex(frame, attribute, regex):
    """
    Verify if a frame attribute matches a regex pattern.
    
    Args:
        frame: The H2 frame to check
        attribute: The attribute name to check
        regex: The regex pattern to match against
    """
    if not hasattr(frame, attribute):
        return False
    
    try:
        value = getattr(frame, attribute)
        matches = value.matches(regex)
        if matches:
            return True
        else:
            return False
    except AttributeError:
        return False

def length_equal_to(event, length):
    """
    Verify the length of frame data or payload.
    Handles different frame types appropriately.
    """
    try:
        expected_length = int(length)
            
        # For events with data attribute
        if hasattr(event, 'data'):
            actual_length = len(event.data)
            return actual_length == expected_length
            
        return False
        
    except Exception as e:
        return False
    
def length_greater_than(event, length):
    """
    Verify if the length of frame data or payload is greater than a given value.
    Handles different frame types appropriately.
    """
    try:
        expected_length = int(length)
        
        # For events with data attribute
        if hasattr(event, 'data'):
            actual_length = len(event.data)
            return actual_length > expected_length

        return False
    
    except Exception as e:
        return False

def verifystreamid(event, stream_id):
    """
    Verify the stream ID of a frame.
    
    Args:
        event: The H2 frame to check
        stream_id: Expected stream ID as string or int
    """
    try:
        expected_stream_id = int(stream_id)
        if not hasattr(event, 'stream_id'):
            return False
        
        actual_stream_id = event.stream_id
        if actual_stream_id == expected_stream_id:
            return True
        else:
            return False
    except ValueError:
        return False

def verifyack(event, ack):
    """
    Verify if ACK flag is set in the frame.
    
    Args:
        event: The H2 frame to check
        ack: Expected ACK value ('true' or 'false', case insensitive)
    """
    try:
        expected_ack = str(ack).lower() == 'true'
        
        # Handle SettingsFrame which has a dedicated is_ack property
        if hasattr(event, 'is_ack'):
            result = event.is_ack == expected_ack
        # Handle other frame types that use flags
        elif hasattr(event, 'flags'):
            result = event.flags.get('ACK', False) == expected_ack
        else:
            return False
        
        if result:
            return True
        else:
            return False
    except Exception as e:
        return False

def verifysettings(event, setting, value):
    """
    Verify settings values in a SETTINGS frame.
    
    Args:
        event: The H2 frame to check
        setting: The setting name to verify
        value: Expected setting value as string or int
    """
    try:
        expected_value = int(value)
        if not hasattr(event, 'changed_settings'):
            return False
        
        # Convert items() to dict if it's not already
        settings = dict(event.changed_settings) if hasattr(event.changed_settings, 'items') else event.changed_settings
        
        if setting not in settings:
            return False
        
        actual_value = settings[setting]
        if actual_value == expected_value:
            return True
        else:
            return False
    except ValueError:
        return False
    except Exception as e:
        return False


def verifytype(event, type):
    if event.__class__.__name__ == type:
        return True
    else:
        return False

function_map = {
    'verifyregex': verifyregex,
    'length_equal_to': length_equal_to,
    'length_greater_than': length_greater_than,
    'verifystreamid': verifystreamid,
    'verifyack': verifyack,
    'verifysettings': verifysettings,
    'verifytype': verifytype
}