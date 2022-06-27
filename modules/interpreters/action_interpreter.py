import cmd
import codecs
import logging
import pickle
import time
import json

from scapy.all import send

from modules.controllers.messages import JSONLOGMessage, JSONMessage
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

    def do_listen(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        machine.start_sniffer()
        machine.set_stack(parsed[0])

    def do_send(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        send(machine.get_variable(parsed[0]))
        serializable_packet = codecs.encode(pickle.dumps(machine.get_variable(parsed[0])), "base64").decode()
        machine.controller_protocol.transport.write(json.dumps({JSONMessage.LOG.name: JSONLOGMessage.SENT.name, JSONMessage.PARAMETERS.name: serializable_packet}).encode())
        #pickle.loads(codecs.decode('encoded_string'.encode(), "base64"))
        logging.info('SENT ' + get_packet_info(machine.get_variable(parsed[0])))
        machine.trigger('PACKET_SENT')

    def do_done(self, line, machine):
        parsed = InterpreterParser.parse(line, 0)
        machine.trigger('DONE')

    def do_handle_packets(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
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
            if (time.time() - start_time > float(machine.get_variable(parsed[0]))):
                timeout = True
                break
        if (timeout):
            machine.trigger('TIMEOUT')

    def do_pop(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        machine.discard_stack_packet(machine.get_variable(parsed[0]))

    def do_create_TCP_packet(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        machine.set_variable(parsed[0], create_TCP_packet())

    def do_set_IP_dst(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_IP_dst(machine.get_variable(parsed[0]), machine.get_variable(parsed[1]))

    def do_set_IP_src(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_IP_src(machine.get_variable(parsed[0]), machine.get_variable(parsed[1]))
        
    def do_set_TCP_sport(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_TCP_sport(machine.get_variable(parsed[0]), machine.get_variable(parsed[1]))

    def do_set_TCP_dport(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_TCP_dport(machine.get_variable(parsed[0]), machine.get_variable(parsed[1]))

    def do_set_TCP_seq(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_TCP_seq(machine.get_variable(parsed[0]), machine.get_variable(parsed[1]))

    def do_set_TCP_flags(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_TCP_flags(machine.get_variable(parsed[0]), machine.get_variable(parsed[1]))

    def do_set_TCP_ack(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_TCP_ack(machine.get_variable(parsed[0]), machine.get_variable(parsed[1]))

    def do_set_TCP_payload(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_TCP_payload(machine.get_variable(parsed[0]), machine.get_variable(parsed[1]))

    def do_remove_TCP_payload(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        remove_TCP_payload(machine.get_variable(parsed[0]))

    def do_set_TCP_automatic_packet_seq(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        set_TCP_automatic_packet_seq(machine.get_variable(parsed[0]))

    def do_set_TCP_automatic_packet_ack(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        set_TCP_automatic_packet_ack(machine.get_variable(parsed[0]), machine.get_variable(parsed[1])[0])

    def do_get_packet_IP(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        machine.set_variable(parsed[0], get_IP_src(machine.get_variable(parsed[1])[0]))

    def do_get_packet_port(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        machine.set_variable(parsed[0], get_TCP_sport(machine.get_variable(parsed[1])[0]))

    def do_print_TCP_payload(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        print(machine.get_variable(parsed[0])[0]['TCP'].payload)

    def do_set_random_int(self, line, machine):
        parsed = InterpreterParser.parse(line, 3)
        machine.set_variable(parsed[0], set_random_int(parsed[1], parsed[2]))
    
    def do_set_random_float(self, line, machine):
        parsed = InterpreterParser.parse(line, 3)
        machine.set_variable(parsed[0], set_random_float(parsed[1], parsed[2]))

    def do_set_variable(self, line, machine):
        parsed = InterpreterParser.parse(line, 2)
        machine.set_variable(parsed[0], parsed[1])

    def do_add_sport_filter(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        machine.filter_sport.append(int(machine.get_variable(parsed[0])))

    def do_add_dport_filter(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        machine.filter_dport.append(int(machine.get_variable(parsed[0])))

    def do_remove_sport_filter(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        machine.filter_sport.remove(int(machine.get_variable(parsed[0])))

    def do_remove_dport_filter(self, line, machine):
        parsed = InterpreterParser.parse(line, 1)
        machine.filter_dport.remove(int(machine.get_variable(parsed[0])))

    def do_return(self, line, machine):
        parsed = InterpreterParser.parse(line, 0)
        machine.return_to_previous_state()