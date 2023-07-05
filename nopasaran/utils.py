from scapy.all import IP, TCP, UDP
import random
from scapy.layers.tls.all import *

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

def not_(boolean):
	boolean = not(boolean)

def set_random_int(min, max):
	return random.randint(int(min), int(max))

def set_random_float(min, max):
	return random.uniform(int(min), int(max))

def add_TLS_payload(packet, tls_version):
	version = 0x00
	if tls_version == "0":
		version = 0x300
	elif tls_version == "1":
		version = 0x301
	elif tls_version == "2":
		version = 0x302
	elif tls_version == "3":
		version = 0x303
	elif tls_version == "4":
		version = 0x304
	else:
		raise Exception('Unknown TLS version.')
	packet = packet/TLS(version=version)
	return packet

def add_TLS_handshake(packet):
	packet['TLS'].type=22
	return packet

def add_TLS_client_hello(packet):
	payload = TLSClientHello(ciphers=[0])
	length = len(payload) 
	if packet['TLS'].len == None:
		packet['TLS'].len = length
	else:
		packet['TLS'].len = packet['TLS'].len + length
	packet = packet/payload
	return packet

def add_TLS_server_hello(packet):
	payload = TLSServerHello(cipher=0)
	length = len(payload) 
	if packet['TLS'].len == None:
		packet['TLS'].len = length
	else:
		packet['TLS'].len = packet['TLS'].len + length
	packet = packet/payload
	return packet

def add_TLS_application_data(packet, data):
	packet['TLS'].type=23
	payload = TLSApplicationData(data=data)
	length = len(payload) 
	if packet['TLS'].len == None:
		packet['TLS'].len = length
	else:
		packet['TLS'].len = packet['TLS'].len + length
	packet = packet/payload
	return packet

def get_TCP_payload_length(packet):
	if packet['TCP'].payload != None:
		return len(packet['TCP'].payload)
	else:
		return 0