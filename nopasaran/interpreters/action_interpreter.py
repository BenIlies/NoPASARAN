import cmd
import time
import json

from scapy.all import send
from twisted.internet.threads import deferToThread

from nopasaran.controllers.messages import JSONMessage, Status
from nopasaran.parsers.interpreter_parser import InterpreterParser
from nopasaran.controllers.controller import ClientController, ServerController
from nopasaran.utils import *


class ActionInterpreter(cmd.Cmd):
    def onecmd(self, line, machine):
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
            return func(arg, machine)

    def default(self, line, machine):
        raise Exception('Parsing error: argument "' + line + '" is unknown.')

    def do_set(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], inputs[0])
        

    def do_send(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        send(machine.get_variable(inputs[0]))
        machine.trigger('PACKET_SENT')

    def do_done(self, line, machine):
        InterpreterParser.parse(line, 0, 0)
        machine.trigger('DONE')

    def do_create_TCP_packet(self, line, machine):
        _, outputs = InterpreterParser.parse(line, 0, 1)
        machine.set_variable(outputs[0], create_TCP_packet())

    def do_create_UDP_packet(self, line, machine):
        _, outputs = InterpreterParser.parse(line, 0, 1)
        machine.set_variable(outputs[0], create_UDP_packet())

    def do_set_random_int(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], set_random_int(inputs[0], inputs[1]))
    
    def do_set_random_float(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], set_random_float(inputs[0], inputs[1]))

    def do_set_IP_src(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_IP_src(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_set_IP_dst(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_IP_dst(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_set_TCP_sport(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_sport(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_set_TCP_dport(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_dport(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_set_UDP_sport(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_UDP_sport(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_set_UDP_dport(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_UDP_dport(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_set_TCP_seq(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_seq(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_get_TCP_flags(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], get_TCP_flags(machine.get_variable(inputs[0])[0]))

    def do_set_TCP_flags(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_flags(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_set_TCP_ack(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_ack(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_set_TCP_payload(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_payload(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

    def do_remove_TCP_payload(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        remove_TCP_payload(machine.get_variable(outputs[0]))

    def do_set_TCP_automatic_packet_seq(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_automatic_packet_seq(machine.get_variable(outputs[0]))

    def do_set_TCP_automatic_packet_ack(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_automatic_packet_ack(machine.get_variable(outputs[0]), machine.get_variable(inputs[1])[0])

    def do_get_packet_IP(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], get_IP_src(machine.get_variable(inputs[0])[0]))

    def do_get_packet_port(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], get_TCP_sport(machine.get_variable(inputs[0])[0]))

    def do_print_TCP_payload(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        print(machine.get_variable(inputs[0])[0]['TCP'].payload)

    def do_return(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 0, 0, True, False)
        machine.returned = inputs

    def do_pop(self, line, machine):     
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        machine.get_variable(inputs[0]).pop(0)

    def do_listen(self, line, machine):
        _, outputs = InterpreterParser.parse(line, 0, 1)
        machine.start_sniffer()
        machine.set_variable(outputs[0], [])
        machine.set_sniffer_queue(machine.get_variable(outputs[0]))

    def do_wait_packet_signal(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        timeout = False
        start_time = time.time()
        while (True):
            stack = machine.get_variable(inputs[0])
            if len(stack) > 0:
                machine.trigger('PACKET_AVAILABLE')
                break
            if (time.time() - start_time > float(machine.get_variable(inputs[1]))):
                timeout = True
                break
        if (timeout):
            machine.trigger('TIMEOUT')

    def do_call(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 0, True, True)
        nested_xstate_json = json.load(open('.'.join((inputs[0], 'json'))))
        parameters = []
        for index in range (1, len(inputs)):
            parameters.append(machine.get_variable(inputs[index]))
        nested_machine = machine.get_child_machine(nested_xstate_json, parameters)
        nested_machine.start()
        for index in range (0, len(nested_machine.returned)):
            machine.set_variable(outputs[index], nested_machine.get_variable(nested_machine.returned[index])) 

    def do_trigger(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        machine.trigger(machine.get_variable(inputs[0]))

    def do_wait_ready_signal(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        timeout = False
        start_time = time.time()
        while (True):
            controller_protocol = machine.get_variable(inputs[0])
            if controller_protocol:
                if controller_protocol.local_status == Status.READY.name and controller_protocol.remote_status == Status.READY.name:
                    break
            if (time.time() - start_time > float(machine.get_variable(inputs[1]))):
                timeout = True
                break
        if (timeout):
            machine.trigger('TIMEOUT')
        else:
            machine.trigger('READY')


    def do_sync(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0, True, False)
        controller_protocol = machine.get_variable(inputs[0])
        if controller_protocol:
            controller_protocol.send_sync(inputs[1:])
            machine.trigger('SYNC_SENT')     

    def do_wait_sync_signal(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 0, False, True)
        timeout = False
        start_time = time.time()
        sync_message = None
        while (True):
            controller_protocol = machine.get_variable(inputs[0])
            if controller_protocol:
                if len(controller_protocol.queue) > 0:
                    sync_message = controller_protocol.queue[0]
                    controller_protocol.queue.pop(0)
                    break
            if (time.time() - start_time > float(machine.get_variable(inputs[1]))):
                timeout = True
                break
        if (timeout):
            machine.trigger('TIMEOUT')
        else:
            for index in range (0, len(outputs)):
                machine.set_variable(outputs[index], sync_message[JSONMessage.SYNC.name][index])
            machine.trigger('SYNC_AVAILABLE')
            
    def do_packet_filter(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        machine.set_sniffer_filter(machine.get_variable(inputs[0]))

    def do_get_from_file(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        file_variables = json.load(open('.'.join((inputs[0], 'json'))))
        machine.set_variable(outputs[0], file_variables[inputs[1]])

    def do_redirect(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        machine.add_redirection(inputs[0], inputs[1])

    def do_get_parameters(self, line, machine):
        _, outputs = InterpreterParser.parse(line, 0, 0, False, True)
        for index in range (0, len(machine.parameters)):
            machine.set_variable(outputs[index], machine.parameters[index])

    def do_load_control_channel_configuration(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        controller_configuration = json.load(open('.'.join((inputs[0], 'json'))))
        machine.set_variable(outputs[0], controller_configuration)

    def do_configure_client_control_channel(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 2)
        controller_configuration = machine.get_variable(inputs[0])
        machine.set_variable(outputs[1], None)
        controller = ClientController(machine, outputs[1], controller_configuration['root_certificate'], controller_configuration['private_certificate'])
        controller.configure(controller_configuration['destination_ip'], int(controller_configuration['server_port']))
        machine.set_variable(outputs[0], controller)

    def do_configure_server_control_channel(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 2)
        controller_configuration = machine.get_variable(inputs[0])
        machine.set_variable(outputs[1], None)
        controller = ServerController(machine, outputs[1], controller_configuration['root_certificate'], controller_configuration['private_certificate'])
        controller.configure(int(controller_configuration['server_port']))
        machine.set_variable(outputs[0], controller)

    def do_start_control_channel(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        deferToThread(machine.get_variable(inputs[0]).start)

    def do_print_packet(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        print(machine.get_variable(inputs[0]).show())

    def do_add_tls_payload(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        packet = add_TLS_payload(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))
        machine.set_variable(outputs[0], packet)

    def do_set_as_tls_handshake(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        packet = add_TLS_handshake(machine.get_variable(outputs[0]))
        machine.set_variable(outputs[0], packet)

    def do_add_tls_client_hello(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        packet = add_TLS_client_hello(machine.get_variable(outputs[0]))
        machine.set_variable(outputs[0], packet)

    def do_add_tls_server_hello(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        packet = add_TLS_server_hello(machine.get_variable(outputs[0]))
        machine.set_variable(outputs[0], packet)

    def do_set_as_tls_application_data(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        packet = add_TLS_application_data(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))
        machine.set_variable(outputs[0], packet)

    def do_get_TCP_payload_length(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        length = get_TCP_payload_length(machine.get_variable(inputs[0]))
        machine.set_variable(outputs[0], length)
