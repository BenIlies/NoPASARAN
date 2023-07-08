import json
import time

from scapy.all import send as sendpacket

import nopasaran.utils as utils
from nopasaran.definitions.events import EventNames
from nopasaran.decorators import parsing_decorator


class TmpPrimitives:
    """
    Class containing action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def send(inputs, outputs, state_machine):
        """
        Send the packet stored in the variable with the given name from the machine's state using the machine's
        network interface. Triggers the event PACKET_SENT.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable storing the packet to be sent.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        sendpacket(state_machine.get_variable_value(inputs[0]))
        state_machine.trigger_event(EventNames.PACKET_SENT.name)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0)
    def done(inputs, outputs, state_machine):
        """
        Triggers the event DONE when executed.

        Number of input arguments: 0

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names.

            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.trigger_event(EventNames.DONE.name)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_packet_port(inputs, outputs, state_machine):
        """
        Get the source port from a packet in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of a variable representing the packet.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the source port.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.get_TCP_sport(state_machine.get_variable_value(inputs[0])[0]))



    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def pop(inputs, outputs, state_machine):
        """
        Remove the first element from a list stored in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of a variable representing the list.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.get_variable_value(inputs[0]).pop(0)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def listen(inputs, outputs, state_machine):
        """
        Start the packet sniffer and store the captured packets in a list stored in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the captured packets.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.start_sniffer()
        state_machine.set_variable_value(outputs[0], [])
        state_machine.set_sniffer_queue(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def wait_packet_signal(inputs, outputs, state_machine):
        """
        Wait for a packet to be available in the sniffer's packet stack stored in the machine's state.
        The sniffer's packet stack is created and populated in the 'listen' primitive.
        If a packet becomes available within the specified timeout (second mandatory input argument),
        triggers the event PACKET_AVAILABLE. Otherwise, triggers the event TIMEOUT.

        Number of input arguments: 2

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the name of the packet stack variable and the timeout value.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = False
        start_time = time.time()
        while True:
            stack = state_machine.get_variable_value(inputs[0])
            if len(stack) > 0:
                state_machine.trigger_event(EventNames.PACKET_AVAILABLE.name)
                break
            if time.time() - start_time > float(state_machine.get_variable_value(inputs[1])):
                timeout = True
                break
        if timeout:
            state_machine.trigger_event(EventNames.TIMEOUT.name)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def trigger(inputs, outputs, state_machine):
        """
        Generate an event with a given name based on a local state variable.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the event to trigger.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.trigger_event(state_machine.get_variable_value(inputs[0]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def packet_filter(inputs, outputs, state_machine):
        """
        Set the packet filter for the packet sniffer.

        Number of input arguments: 1

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the new packet filter value.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_sniffer_filter(state_machine.get_variable_value(inputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def get_from_file(inputs, outputs, state_machine):
        """
        Load variables from a file and store them in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the file path and the name of the variable to store the loaded variables.
            
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable where the loaded variables will be stored.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        file_variables = json.load(open('.'.join((inputs[0], 'json'))))
        state_machine.set_variable_value(outputs[0], file_variables[inputs[1]])

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def redirect(inputs, outputs, state_machine):
        """
        Redirect an event to a specific target state when triggered within the state machine.
        This primitive allows you to define a redirection rule for events, specifying the name of the event
        as the first mandatory input argument and the target state as the second mandatory input argument.

        Number of input arguments: 2

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments, which are the name of the event to redirect and the name of the target state.
            
            outputs (List[str]): The list of output variable names.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.add_redirection(inputs[0], inputs[1])