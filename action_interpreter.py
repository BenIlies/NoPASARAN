import cmd
import time

from scapy.all import send

from interpreter_parser import InterpreterParser
from utils import *


class ActionInterpreter(cmd.Cmd):
    def __init__(self, machine):
        self.machine = machine

    def default(self, args):
        raise Exception('Parsing error: argument "' + args + '" is unknown.')

    def do_listen(self, args):
        parsed = InterpreterParser.parse(args, 1)
        self.machine.start_sniffer()
        self.machine.set_stack(parsed[0])

    def do_send(self, args):
        parsed = InterpreterParser.parse(args, 1)
        send(self.machine.get_variable(parsed[0]))
        self.machine.trigger('PACKET_SENT')

    def do_handle_packets(self, args):
        parsed = InterpreterParser.parse(args, 1)
        timeout = False
        start_time = time.time()
        while (True):
            if len(self.machine.get_stack()) >= 1:
                if self.machine.get_stack_top()['TCP'].flags in ['S', 'SA', 'P', 'PA', 'F', 'FA', 'A']:
                    if self.machine.get_stack_top()['TCP'].flags == 'S':
                        self.machine.trigger('SYN_RECEIVED')
                    elif self.machine.get_stack_top()['TCP'].flags == 'SA':
                        self.machine.trigger('SYN_ACK_RECEIVED')
                    elif self.machine.get_stack_top()['TCP'].flags == 'P':
                        self.machine.trigger('PSH_RECEIVED')
                    elif self.machine.get_stack_top()['TCP'].flags == 'PA':
                        self.machine.trigger('PSH_ACK_RECEIVED')
                    elif self.machine.get_stack_top()['TCP'].flags == 'F':
                        self.machine.trigger('FIN_RECEIVED')
                    elif self.machine.get_stack_top()['TCP'].flags == 'FA':
                        self.machine.trigger('FIN_ACK_RECEIVED')
                    elif self.machine.get_stack_top()['TCP'].flags == 'A':
                        self.machine.trigger('ACK_RECEIVED')
                    break
                else:
                    self.machine.discard_stack_packet(self.machine.get_stack())
            if (time.time() - start_time > float(self.machine.get_variable(parsed[0]))):
                timeout = True
                break
        if (timeout):
            self.machine.trigger('TIMEOUT')

    def do_pop(self, args):
        parsed = InterpreterParser.parse(args, 1)
        self.machine.discard_stack_packet(self.machine.get_variable(parsed[0]))

    def do_create_TCP_packet(self, args):
        parsed = InterpreterParser.parse(args, 1)
        self.machine.set_variable(parsed[0], create_TCP_packet())

    def do_set_IP_dst(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_IP_dst(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1]))

    def do_set_IP_src(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_IP_src(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1]))
        

    def do_set_TCP_sport(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_TCP_sport(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1]))

    def do_set_TCP_dport(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_TCP_dport(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1]))

    def do_set_TCP_seq(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_TCP_seq(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1]))

    def do_set_TCP_flags(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_TCP_flags(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1]))

    def do_set_TCP_ack(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_TCP_ack(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1]))

    def do_set_TCP_payload(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_TCP_payload(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1]))

    def do_remove_TCP_payload(self, args):
        parsed = InterpreterParser.parse(args, 1)
        remove_TCP_payload(self.machine.get_variable(parsed[0]))

    def do_set_TCP_automatic_packet_seq(self, args):
        parsed = InterpreterParser.parse(args, 1)
        set_TCP_automatic_packet_seq(self.machine.get_variable(parsed[0]))

    def do_set_TCP_automatic_packet_ack(self, args):
        parsed = InterpreterParser.parse(args, 2)
        set_TCP_automatic_packet_ack(self.machine.get_variable(parsed[0]), self.machine.get_variable(parsed[1])[0])

    def do_print_TCP_payload(self, args):
        parsed = InterpreterParser.parse(args, 1)
        print(self.machine.get_variable(parsed[0])[0]['TCP'].payload)

    def do_set_random_int(self, args):
        parsed = InterpreterParser.parse(args, 3)
        self.machine.set_variable(parsed[0], set_random_int(parsed[1], parsed[2]))
    
    def do_set_random_float(self, args):
        parsed = InterpreterParser.parse(args, 3)
        self.machine.set_variable(parsed[0], set_random_float(parsed[1], parsed[2]))

    def do_return(self, args):
        parsed = InterpreterParser.parse(args, 0)
        self.machine.return_to_previous_state()