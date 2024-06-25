import random

from scapy.all import IP, TCP, UDP, ICMP

def create_TCP_packet():
	return IP()/TCP()

def create_UDP_packet():
	return IP()/UDP()

def set_IP_dst(packet, dst):
	packet['IP'].dst = dst

def set_IP_src(packet, src):
	packet['IP'].src = src

def get_IP_dst(packet):
	return packet['IP'].dst

def get_IP_src(packet):
	return packet['IP'].src

def set_TCP_sport(packet, sport):
	packet['TCP'].sport = int(sport)

def set_TCP_dport(packet, dport):
	packet['TCP'].dport = int(dport)

def set_UDP_sport(packet, sport):
	packet['UDP'].sport = int(sport)

def set_UDP_dport(packet, dport):
	packet['UDP'].dport = int(dport)

def get_UDP_sport(packet):
	return packet['UDP'].sport

def get_UDP_dport(packet):
	return packet['UDP'].dport

def get_TCP_sport(packet):
	return packet['TCP'].sport

def get_TCP_dport(packet):
	return packet['TCP'].sport

def set_TCP_seq(packet, seq):
	packet['TCP'].seq = int(seq)

def set_TCP_flags(packet, flags):
	packet['TCP'].flags = flags

def get_TCP_flags(packet):
	return str(packet['TCP'].flags)

def set_TCP_ack(packet, ack):
    packet['TCP'].ack = int(ack)

def set_TCP_automatic_packet_seq(packet):
	increase = 0
	if packet['TCP'].flags in ['S','F','SA','FA']:
		increase =  1
	elif packet['TCP'].flags in ['P','PA']:
		increase = len(packet['TCP'].payload)
	else:
		if packet['TCP'].payload != None:
			if len(packet['TCP'].payload) > 0:
				increase = len(packet['TCP'].payload)
	packet['TCP'].seq = packet['TCP'].seq + increase

def set_TCP_automatic_packet_ack(ack_packet, original_packet):
	increase = 0
	if original_packet['TCP'].flags in ['S','F','SA','FA']:
		increase =  1
	elif original_packet['TCP'].flags in ['P','PA']:
		increase = len(original_packet['TCP'].payload)
	else:
		if original_packet['TCP'].payload != None:
			if len(original_packet['TCP'].payload) > 0:
				increase = len(original_packet['TCP'].payload)
	ack_packet['TCP'].ack = original_packet['TCP'].seq + increase

def set_TCP_payload(packet, payload):
	packet['TCP'].remove_payload()
	packet['TCP'].add_payload(payload)

def remove_TCP_payload(packet):
	packet['TCP'].remove_payload()

def set_random_int(min, max):
	return random.randint(int(min), int(max))

def set_random_float(min, max):
	return random.uniform(int(min), int(max))

def create_ICMP_packet():
	return IP()/ICMP()

def get_ICMP_payload(packet):
	return packet[ICMP].payload

def handle_client_connection(client_socket):
    try:
        client_socket.recv(1024)
    except Exception as e:
        raise(e)
