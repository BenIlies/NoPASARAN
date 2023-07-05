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
        state_machine.set_variable_value(outputs[0], inputs[0])

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def send(inputs, outputs, state_machine):
        sendpacket(state_machine.get_variable_value(inputs[0]))
        state_machine.trigger_event(EventNames.PACKET_SENT.name)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0)
    def done(inputs, outputs, state_machine):
        state_machine.trigger_event(EventNames.DONE.name)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_TCP_packet(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], utils.create_TCP_packet())

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_UDP_packet(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], utils.create_UDP_packet())

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_random_int(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], utils.set_random_int(inputs[0], inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_random_float(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], utils.set_random_float(inputs[0], inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_src(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_IP_src(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_IP_dst(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_IP_dst(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_sport(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_sport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_dport(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_dport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_sport(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_UDP_sport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))
    
    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_UDP_dport(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_UDP_dport(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_seq(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_seq(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_TCP_flags(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], utils.get_TCP_flags(state_machine.get_variable_value(inputs[0])[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_flags(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_flags(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_ack(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_ack(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_payload(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_payload(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def remove_TCP_payload(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.remove_TCP_payload(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set_TCP_automatic_packet_seq(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_automatic_packet_seq(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_TCP_automatic_packet_ack(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], state_machine.get_variable_value(inputs[0]))
        utils.set_TCP_automatic_packet_ack(state_machine.get_variable_value(outputs[0]), state_machine.get_variable_value(inputs[1])[0])

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_packet_IP(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], utils.get_IP_src(state_machine.get_variable_value(inputs[0])[0]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_packet_port(inputs, outputs, state_machine):
        state_machine.set_variable_value(outputs[0], utils.get_TCP_sport(state_machine.get_variable_value(inputs[0])[0]))

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def print_TCP_payload(inputs, outputs, state_machine):
        print(state_machine.get_variable_value(inputs[0])[0]['TCP'].payload)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0, optional_inputs=True, optional_outputs=False)
    def return_values(inputs, outputs, state_machine):
        state_machine.returned = inputs

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def pop(inputs, outputs, state_machine):
        state_machine.get_variable_value(inputs[0]).pop(0)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def listen(inputs, outputs, state_machine):
        state_machine.start_sniffer()
        state_machine.set_variable_value(outputs[0], [])
        state_machine.set_sniffer_queue(state_machine.get_variable_value(outputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def wait_packet_signal(inputs, _, state_machine):
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
    def trigger_event(inputs, _, state_machine):
        state_machine.trigger_event(state_machine.get_variable_value(inputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def wait_ready_signal(inputs, _, state_machine):
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
        controller_protocol = state_machine.get_variable_value(inputs[0])
        if controller_protocol:
            controller_protocol.send_sync(inputs[1:])
            state_machine.trigger_event(EventNames.SYNC_SENT.name)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0, optional_outputs=True)
    def wait_sync_signal(inputs, outputs, state_machine):
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
        state_machine.set_sniffer_filter(state_machine.get_variable_value(inputs[0]))

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def get_from_file(inputs, outputs, state_machine):
        file_variables = json.load(open('.'.join((inputs[0], 'json'))))
        state_machine.set_variable_value(outputs[0], file_variables[inputs[1]])

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def redirect(inputs, _, state_machine):
        state_machine.add_redirection(inputs[0], inputs[1])

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0, optional_outputs=True)
    def get_parameters(_, outputs, state_machine):
        for index in range(len(state_machine.parameters)):
            state_machine.set_variable_value(outputs[index], state_machine.parameters[index])

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def load_control_channel_configuration(inputs, outputs, state_machine):
        controller_configuration = json.load(open('.'.join((inputs[0], 'json'))))
        state_machine.set_variable_value(outputs[0], controller_configuration)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=2)
    def configure_client_control_channel(inputs, outputs, state_machine):
        controller_configuration = state_machine.get_variable_value(inputs[0])
        state_machine.set_variable_value(outputs[1], None)
        controller = ClientController(state_machine, outputs[1], controller_configuration[Configuration.ROOT_CERTIFICATE.name], controller_configuration[Configuration.PRIVATE_CERTIFICATE.name])
        controller.configure(controller_configuration[Configuration.DESTINATION_IP.name], int(controller_configuration[Configuration.SERVER_PORT.name]))
        state_machine.set_variable_value(outputs[0], controller)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=2)
    def configure_server_control_channel(inputs, outputs, state_machine):
        controller_configuration = state_machine.get_variable_value(inputs[0])
        state_machine.set_variable_value(outputs[1], None)
        controller = ServerController(state_machine, outputs[1], controller_configuration[Configuration.ROOT_CERTIFICATE.name], controller_configuration[Configuration.PRIVATE_CERTIFICATE.name])
        controller.configure(int(controller_configuration[Configuration.SERVER_PORT.name]))
        state_machine.set_variable_value(outputs[0], controller)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def start_control_channel(inputs, _, state_machine):
        deferToThread(state_machine.get_variable_value(inputs[0]).start)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def print_packet(inputs, _, state_machine):
        print(state_machine.get_variable_value(inputs[0]).show())

