import json
import time

from twisted.internet.threads import deferToThread
from scapy.all import send as sendpacket

import nopasaran.utils as utils
from nopasaran.controllers.controller import ClientController, ServerController
from nopasaran.definitions.control_channel import JSONMessage, Status, Configuration
from nopasaran.definitions.events import EventNames
from nopasaran.decorators import parsing_decorator


class ActionPrimitives:
    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set(inputs, outputs, state_machine):
        """
        Set the value of an output variable in the machine's state.
        
        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the new value.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modification.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], inputs[0])

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def send(inputs, outputs, state_machine):
        """
        Send the packet stored in the variable with the given name from the machine's state using the machine's
        network interface. Triggers the event PACKET_SENT.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of the variable storing the packet to be sent.
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

        Args:
            inputs (List[str]): The list of input variable names.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.trigger_event(EventNames.DONE.name)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_TCP_packet(inputs, outputs, state_machine):
        """
        Create a TCP packet and store it in an output variable in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable to store the created TCP packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.create_TCP_packet())

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_UDP_packet(inputs, outputs, state_machine):
        """
        Create a UDP packet and store it in an output variable in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable to store the created UDP packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.create_UDP_packet())

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_random_int(inputs, outputs, state_machine):
        """
        Generate a random integer between two input values and store it in an output variable in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the lower bound and the upper bound.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable to store the generated random integer.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.set_random_int(inputs[0], inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_random_float(inputs, outputs, state_machine):
        """
        Generate a random float between two input values and store it in an output variable in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the lower bound and the upper bound.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable to store the generated random float.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.set_random_float(inputs[0], inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_src(inputs, outputs, state_machine):
        """
        Set the source IP address of a packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new IP address and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_IP_src(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_dst(inputs, outputs, state_machine):
        """
        Set the destination IP address of a packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new IP address and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_IP_dst(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_sport(inputs, outputs, state_machine):
        """
        Set the source port of a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new source port value and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_sport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_dport(inputs, outputs, state_machine):
        """
        Set the destination port of a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new destination port value and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_dport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_sport(inputs, outputs, state_machine):
        """
        Set the source port of a UDP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new source port value and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_UDP_sport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_dport(inputs, outputs, state_machine):
        """
        Set the destination port of a UDP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new destination port value and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_UDP_dport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_seq(inputs, outputs, state_machine):
        """
        Set the sequence number of a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new sequence number value and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified packet.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_seq(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_TCP_flags(inputs, outputs, state_machine):
        """
        Get the TCP flags from a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable to store the TCP flags.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.get_TCP_flags(state_machine.get_variable_value(inputs[0])[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_flags(inputs, outputs, state_machine):
        """
        Set the TCP flags of a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new TCP flags value and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified TCP flags.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_flags(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_ack(inputs, outputs, state_machine):
        """
        Set the acknowledgment number of a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new acknowledgment number value and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified acknowledgment number.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_ack(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_payload(inputs, outputs, state_machine):
        """
        Set the payload of a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new payload value and the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the modified payload.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_payload(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def remove_TCP_payload(inputs, outputs, state_machine):
        """
        Remove the payload from a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the payload removed.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.remove_TCP_payload(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set_TCP_automatic_packet_seq(inputs, outputs, state_machine):
        """
        Set the sequence number of a TCP packet in the machine's state to an automatically generated value.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the automatically generated sequence number.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_automatic_packet_seq(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_automatic_packet_ack(inputs, outputs, state_machine):
        """
        Set the acknowledgment number of a TCP packet in the machine's state to an automatically generated value.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the new acknowledgment number value, the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable with the automatically generated acknowledgment number.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_automatic_packet_ack(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1])[0])

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_packet_IP(inputs, outputs, state_machine):
        """
        Get the source IP address from a packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable to store the source IP address.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.get_IP_src(state_machine.get_variable_value(inputs[0])[0]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_packet_port(inputs, outputs, state_machine):
        """
        Get the source port from a packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable to store the source port.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.set_variable_value(outputs[0], utils.get_TCP_sport(state_machine.get_variable_value(inputs[0])[0]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def print_TCP_payload(inputs, outputs, state_machine):
        """
        Print the payload of a TCP packet in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of a variable representing the packet.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        print(state_machine.get_variable_value(inputs[0])[0]['TCP'].payload)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0, optional_inputs=True, optional_outputs=False)
    def return_values(inputs, outputs, state_machine):
        """
        This primitive is used within a nested state machine. It enables you to specify the values that will be returned
        by the nested state machine when it completes its execution. The returned values can be used by the calling state
        machine for further processing or decision-making.

        Args:
            inputs (List[str]): The list of input variable names.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.returned = inputs

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def pop(inputs, outputs, state_machine):
        """
        Remove the first element from a list stored in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of a variable representing the list.
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

        Args:
            inputs (List[str]): The list of input variable names.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable to store the captured packets.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.start_sniffer()
        state_machine.set_variable_value(outputs[0], [])
        state_machine.set_sniffer_queue(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def wait_packet_signal(inputs, _, state_machine):
        """
        Wait for a packet to be available in the sniffer's packet stack stored in the machine's state.
        The sniffer's packet stack is created and populated in the 'listen' primitive.
        If a packet becomes available within the specified timeout (second mandatory input argument),
        triggers the event PACKET_AVAILABLE. Otherwise, triggers the event TIMEOUT.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the name of the packet stack variable and the timeout value.
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
    @parsing_decorator(input_args=1, output_args=0, optional_inputs=True, optional_outputs=True)
    def call(inputs, outputs, state_machine):
        """
        Load a nested machine identified by the given name and call its start method with the provided parameters.
        The mandatory input argument is the name of the nested state machine to call.
        The optional input arguments are the parameters assigned to the nested state machine.
        The optional output arguments are the values returned by the nested state machine and will be stored in the
        specified optional output variables. The number of optional output arguments should match the number of optional
        input arguments specified in the 'return_values' primitive used within the nested state machine.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of the nested state machine to call, and optional input arguments
                                representing the parameters assigned to the nested state machine.
            outputs (List[str]): The list of output variable names. It contains the names of the variables where
                                 the returned values will be stored (optional).
            state_machine: The state machine object.

        Returns:
            None
        """
        nested_state_json = json.load(open('.'.join((inputs[0], 'json'))))
        parameters = []
        for nested_variables in inputs[1:]:
            parameters.append(state_machine.get_variable_value(nested_variables))
        nested_machine = state_machine.get_nested_machine(nested_state_json, parameters)
        nested_machine.start()
        for index in range(len(nested_machine.returned)):
            state_machine.set_variable_value(outputs[index], nested_machine.get_variable_value(nested_machine.returned[index]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def trigger(inputs, _, state_machine):
        """
        Generate an event with a given name based on a local state variable.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of the event to trigger.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.trigger_event(state_machine.get_variable_value(inputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def wait_ready_signal(inputs, _, state_machine):
        """
        Wait for the local and remote status of the controller protocol to be READY.
        If the status becomes READY within the specified timeout (input argument),
        triggers the event READY. Otherwise, triggers the event TIMEOUT.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the names of the local and remote status variables, and the timeout value.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = False
        start_time = time.time()
        while True:
            controller_protocol = state_machine.get_variable_value(inputs[0])
            if controller_protocol:
                if controller_protocol.local_status == Status.READY.name and controller_protocol.remote_status == Status.READY.name:
                    break
            if time.time() - start_time > float(state_machine.get_variable_value(inputs[1])):
                timeout = True
                break
        if timeout:
            state_machine.trigger_event(EventNames.TIMEOUT.name)
        else:
            state_machine.trigger_event(EventNames.READY.name)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0, optional_inputs=True)
    def sync(inputs, _, state_machine):
        """
        Send a synchronization message containing the provided inputs to the controller protocol.
        Triggers the event SYNC_SENT.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of the variable storing the inputs to be synchronized,
                                and optional input arguments representing additional synchronization inputs.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        controller_protocol = state_machine.get_variable_value(inputs[0])
        if controller_protocol:
            controller_protocol.send_sync(inputs[1:])
            state_machine.trigger_event(EventNames.SYNC_SENT.name)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0, optional_outputs=True)
    def wait_sync_signal(inputs, outputs, state_machine):
        """
        Wait for a synchronization message to be available in the controller protocol's queue.
        If a message becomes available within the specified timeout (input argument),
        store its contents in the output variables and trigger the event SYNC_AVAILABLE.
        Otherwise, triggers the event TIMEOUT.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the name of the variable storing the received synchronization message,
                                and the timeout value.
            outputs (List[str]): The list of output variable names. It contains the names of the variables where
                                 the synchronization message will be stored (optional).
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = False
        start_time = time.time()
        sync_message = None
        while True:
            controller_protocol = state_machine.get_variable_value(inputs[0])
            if controller_protocol:
                if len(controller_protocol.queue) > 0:
                    sync_message = controller_protocol.queue[0]
                    controller_protocol.queue.pop(0)
                    break
            if time.time() - start_time > float(state_machine.get_variable_value(inputs[1])):
                timeout = True
                break
        if timeout:
            state_machine.trigger_event(EventNames.TIMEOUT.name)
        else:
            for index in range(len(outputs)):
                state_machine.set_variable_value(outputs[index], sync_message[JSONMessage.SYNC.name][index])
            state_machine.trigger_event(EventNames.SYNC_AVAILABLE.name)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def packet_filter(inputs, _, state_machine):
        """
        Set the packet filter for the packet sniffer.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the new packet filter value.
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

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the file path and the name of the variable to store the loaded variables.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable where the loaded variables will be stored.
            state_machine: The state machine object.

        Returns:
            None
        """
        file_variables = json.load(open('.'.join((inputs[0], 'json'))))
        state_machine.set_variable_value(outputs[0], file_variables[inputs[1]])

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def redirect(inputs, _, state_machine):
        """
        Redirect an event to a specific target state when triggered within the state machine.
        This primitive allows you to define a redirection rule for events, specifying the name of the event
        as the first mandatory input argument and the target state as the second mandatory input argument.

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments,
                                which are the name of the event to redirect and the name of the target state.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        state_machine.add_redirection(inputs[0], inputs[1])

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0, optional_outputs=True)
    def get_parameters(_, outputs, state_machine):
        """
        Retrieve the parameters of the current nested state machine that were passed from the parent state machine
        using the 'call' primitive. These parameters are optional input arguments specified in the 'call' action of
        the parent state machine. The retrieved parameter values will be stored in the specified optional output
        arguments for further use within the nested machine. The number of optional input arguments in the 'call'
        primitive and the number of output arguments in 'get_parameters' should match.

        Args:
            inputs (List[str]): The list of input variable names.
            outputs (List[str]): The list of output variable names. It contains the names of the variables where
                                 the parameter values will be stored (optional).
            state_machine: The state machine object.

        Returns:
            None
        """
        for index in range(len(state_machine.parameters)):
            state_machine.set_variable_value(outputs[index], state_machine.parameters[index])

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def load_control_channel_configuration(inputs, outputs, state_machine):
        """
        Load the control channel configuration from a file and store it in the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the file path, and one mandatory output argument,
                                which is the name of the variable to store the loaded configuration.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument,
                                 which is the name of the variable where the loaded configuration will be stored.
            state_machine: The state machine object.

        Returns:
            None
        """
        controller_configuration = json.load(open('.'.join((inputs[0], 'json'))))
        state_machine.set_variable_value(outputs[0], controller_configuration)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=2)
    def configure_client_control_channel(inputs, outputs, state_machine):
        """
        Configure the client control channel using the controller configuration from the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of the variable storing the configuration,
                                and two mandatory output arguments, which are the names of the variables where
                                the configured controller and controller protocols will be stored.
            outputs (List[str]): The list of output variable names. It contains two mandatory output arguments,
                                 which are the names of the variables where the configured controller and controller
                                 protocols will be stored.
            state_machine: The state machine object.

        Returns:
            None
        """
        controller_configuration = state_machine.get_variable_value(inputs[0])
        state_machine.set_variable_value(outputs[1], None)
        controller = ClientController(state_machine, outputs[1], controller_configuration[Configuration.ROOT_CERTIFICATE.name], controller_configuration[Configuration.PRIVATE_CERTIFICATE.name])
        controller.configure(controller_configuration[Configuration.DESTINATION_IP.name], int(controller_configuration[Configuration.SERVER_PORT.name]))
        state_machine.set_variable_value(outputs[0], controller)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=2)
    def configure_server_control_channel(inputs, outputs, state_machine):
        """
        Configure the server control channel using the controller configuration from the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of the variable storing the configuration,
                                and two mandatory output arguments, which are the names of the variables where
                                the configured controller and controller protocols will be stored.
            outputs (List[str]): The list of output variable names. It contains two mandatory output arguments,
                                 which are the names of the variables where the configured controller and controller
                                 protocols will be stored.
            state_machine: The state machine object.

        Returns:
            None
        """
        controller_configuration = state_machine.get_variable_value(inputs[0])
        state_machine.set_variable_value(outputs[1], None)
        controller = ServerController(state_machine, outputs[1], controller_configuration[Configuration.ROOT_CERTIFICATE.name], controller_configuration[Configuration.PRIVATE_CERTIFICATE.name])
        controller.configure(int(controller_configuration[Configuration.SERVER_PORT.name]))
        state_machine.set_variable_value(outputs[0], controller)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def start_control_channel(inputs, outputs, state_machine):
        """
        Start the control channel using the specified variable's value from the machine's state.

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument,
                                which is the name of the variable storing the control channel object.
            outputs (List[str]): The list of output variable names.
            state_machine: The state machine object.

        Returns:
            None
        """
        deferToThread(state_machine.get_variable_value(inputs[0]).start)

