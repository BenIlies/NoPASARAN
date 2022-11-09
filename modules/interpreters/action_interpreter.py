import cmd
import codecs
import logging
import pickle
import time
import json

from scapy.all import send

from modules.controllers.messages import JSONLOGMessage, JSONMessage, Status
from modules.parsers.interpreter_parser import InterpreterParser
from modules.utils import *


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
        serializable_packet = codecs.encode(pickle.dumps(machine.get_variable(inputs[0])), "base64").decode()
        if machine.root_machine.controller_protocol:
            machine.root_machine.controller_protocol.transport.write(json.dumps({JSONMessage.LOG.name: JSONLOGMessage.SENT.name, JSONMessage.PARAMETERS.name: serializable_packet}).encode())
        logging.info('LOCAL SENT ' + repr(machine.get_variable(inputs[0])))
        machine.trigger('PACKET_SENT')

    def do_done(self, line, machine):
        InterpreterParser.parse(line, 0, 0)
        machine.trigger('DONE')

    def do_create_TCP_packet(self, line, machine):
        _, outputs = InterpreterParser.parse(line, 0, 1)
        machine.set_variable(outputs[0], create_TCP_packet())

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

    def do_set_TCP_seq(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 2, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        set_TCP_seq(machine.get_variable(outputs[0]), machine.get_variable(inputs[1]))

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

    def do_rollback(self, line, machine):
        InterpreterParser.parse(line, 0, 0)
        machine.return_to_previous_state()

    def do_return(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        machine.returned = inputs

    def do_pop(self, line, machine):     
        inputs, outputs = InterpreterParser.parse(line, 1, 1)
        machine.set_variable(outputs[0], machine.get_variable(inputs[0]))
        machine.discard_stack_packet(machine.get_variable(outputs[0]))

    def do_listen(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        machine.start_sniffer()
        machine.set_stack(inputs[0])

    ##HAVE TO ADD THE QUEUE HERE
    def do_wait_packet_signal(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 2, 0)
        timeout = False
        start_time = time.time()
        while (True):
            if len(machine.get_stack()) >= 1:
                if machine.get_stack_top()['TCP'].flags in ['S', 'SA', 'P', 'PA', 'F', 'FA', 'A']:
                    if machine.get_stack_top()['TCP'].flags == 'S':
                        machine.trigger('SYN_RECEIVED')
                    elif machine.get_stack_top()['TCP'].flags == 'SA':
                        machine.trigger('SYN_ACK_RECEIVED')
                    elif machine.get_stack_top()['TCP'].flags == 'P':
                        machine.trigger('PSH_RECEIVED')
                    elif machine.get_stack_top()['TCP'].flags == 'PA':
                        machine.trigger('PSH_ACK_RECEIVED')
                    elif machine.get_stack_top()['TCP'].flags == 'F':
                        machine.trigger('FIN_RECEIVED')
                    elif machine.get_stack_top()['TCP'].flags == 'FA':
                        machine.trigger('FIN_ACK_RECEIVED')
                    elif machine.get_stack_top()['TCP'].flags == 'A':
                        machine.trigger('ACK_RECEIVED')
                    break
                else:
                    machine.discard_stack_packet(machine.get_stack())
            if (time.time() - start_time > float(machine.get_variable(inputs[1]))):
                timeout = True
                break
        if (timeout):
            machine.trigger('TIMEOUT')

    def do_call(self, line, machine):
        inputs, outputs = InterpreterParser.parse(line, 1, 0, True, True)
        nested_xstate_json = json.load(open('.'.join((inputs[0], 'json'))))
        nested_machine = machine.get_child_machine(nested_xstate_json)
        nested_machine.start()
        for index in range (0, len(nested_machine.returned)):
            machine.set_variable(outputs[index], nested_machine.get_variable(nested_machine.returned[index])) 
        print("RETURNED VALUES", machine.get_variables())

    def do_wait_for_ready_control_link(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        timeout = False
        start_time = time.time()
        while (True):
            if machine.root_machine.controller_protocol:
                if machine.root_machine.controller_protocol.local_status == Status.READY.name and machine.root_machine.controller_protocol.remote_status == Status.READY.name:
                    break
            if (time.time() - start_time > float(machine.get_variable(inputs[0]))):
                timeout = True
                break
        if (timeout):
            machine.trigger('TIMEOUT')
        else:
            machine.trigger('CONTROL_LINK_READY')
            
            
    def do_wait_for_disconnecting_control_link(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        timeout = False
        machine.root_machine.controller_protocol.disconnecting()
        start_time = time.time()
        while (True):
            if machine.root_machine.controller_protocol:
                if not machine.root_machine.controller_protocol.is_active:
                    break
            if (time.time() - start_time > float(machine.get_variable(inputs[0]))):
                timeout = True
                break
        if (timeout):
            machine.trigger('TIMEOUT')
        else:
            machine.trigger('CONTROL_LINK_DISCONNECTING')

    def do_packet_filter(self, line, machine):
        inputs, _ = InterpreterParser.parse(line, 1, 0)
        machine.set_sniffer_filter(machine.get_variable(inputs[0]))