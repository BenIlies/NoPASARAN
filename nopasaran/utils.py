import base64
import pickle
import random
import socket
import select

from scapy.all import IP, TCP, UDP, ICMP

def serialize_log_data(log_data):
    def serialize_object(obj):
        try:
            # Serialize the object to a byte stream
            byte_stream = pickle.dumps(obj)
            # Encode the byte stream to a base64 string
            base64_string = base64.b64encode(byte_stream).decode('utf-8')
            return base64_string
        except Exception as e:
            return None

    def serialize_value(value):
        if value is None:
            return None
        if isinstance(value, dict):
            return {k: serialize_value(v) for k, v in value.items()}
        return serialize_object(value)
    
    serialized_data = {k: serialize_value(v) for k, v in log_data.items()}
    # Encode the final serialized data into a base64 string
    return base64.b64encode(pickle.dumps(serialized_data)).decode('utf-8')

def deserialize_log_data(base64_data):
    def deserialize_object(base64_string):
        try:
            # Decode the base64 string to a byte stream
            byte_stream = base64.b64decode(base64_string)
            # Deserialize the byte stream to the original object
            obj = pickle.loads(byte_stream)
            return obj
        except Exception as e:
            return None

    def deserialize_value(value):
        if value is None:
            return None
        if isinstance(value, dict):
            return {k: deserialize_value(v) for k, v in value.items()}
        return deserialize_object(value)
    
    try:
        # Decode the base64 data to a byte stream
        byte_stream = base64.b64decode(base64_data)
        # Deserialize the byte stream to the serialized data
        serialized_data = pickle.loads(byte_stream)
        return {k: deserialize_value(v) for k, v in serialized_data.items()}
    except Exception as e:
        return None

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

def get_TCP_seq(packet):
    return packet['TCP'].seq

def get_TCP_ack(packet):
    return packet['TCP'].ack

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


def send_request(ip, port, request_packet):
    response = b""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip, port))
            s.sendall(request_packet)
            
            while True:
                ready_to_read, _, _ = select.select([s], [], [], 0.5)
                if ready_to_read:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                else:
                    break
    except (socket.error, socket.timeout) as e:
        return None
    
    return response