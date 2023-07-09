import time

from scapy.all import send as sendpacket

from nopasaran.definitions.events import EventNames
from nopasaran.decorators import parsing_decorator


class DataChannelPrimitives:
    """
    Class containing data channel action primitives for the state machine.
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
        state_machine.update_sniffer_queue(state_machine.get_variable_value(outputs[0]))

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
        state_machine.update_sniffer_filter(state_machine.get_variable_value(inputs[0]))

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