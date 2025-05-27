import base64
import pickle
import random
import socket
import select
import ssl
import struct
import logging
from dnslib import DNSRecord, QTYPE



from scapy.all import IP, TCP, UDP, ICMP, Raw



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

def set_UDP_payload(packet, payload_bytes):
    """
    Replace the payload of a UDP packet with payload_bytes without recreating
    the entire packet.

    If a Raw layer already exists, update its load; otherwise, append a new Raw layer.
    """
    if packet.haslayer(Raw):
        # Modify the existing Raw layer
        packet[Raw].load = payload_bytes
    else:
        # Append a new Raw layer to the UDP layer
        packet[UDP].add_payload(Raw(load=payload_bytes))
    return packet

def set_UDP_packet_bytes(packet, size):
    """
    Set the UDP packet's payload to a sequence of 'A' characters of length `size`.
    """
    payload_data = b"A" * int(size)
    return set_UDP_payload(packet, payload_data)

def set_ICMP_type(packet, icmp_type):
    packet['ICMP'].type = int(icmp_type)


def set_ICMP_code(packet, icmp_code):
    packet['ICMP'].code = int(icmp_code)


def get_ICMP_type(packet):
    return packet['ICMP'].type


def get_ICMP_code(packet):
    return packet['ICMP'].code






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
        if packet['TCP'].payload is not None and len(packet['TCP'].payload) > 0:
            increase = len(packet['TCP'].payload)
    packet['TCP'].seq = packet['TCP'].seq + increase

def set_TCP_automatic_packet_ack(ack_packet, original_packet):
    increase = 0
    if original_packet['TCP'].flags in ['S','F','SA','FA']:
        increase =  1
    elif original_packet['TCP'].flags in ['P','PA']:
        increase = len(original_packet['TCP'].payload)
    else:
        if original_packet['TCP'].payload is not None and len(original_packet['TCP'].payload) > 0:
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
    raw_layer = packet[ICMP].payload
    return raw_layer.load if raw_layer is not None else b""


def set_IP_df(packet):
    """
    Set the Don't Fragment (DF) flag on an IP packet.

    Scapy represents flags for the IP packet as an integer. 
    The value 2 (binary 010) corresponds to the DF flag.
    """
    # Ensure we are dealing with an IP packet at the top layer or
    # adjust to packet[IP] if the IP is nested.
    if hasattr(packet, 'flags'):
        packet.flags |= 2  # Set the DF bit
    return packet

def set_ICMP_payload(packet, payload_bytes):
    packet[ICMP].remove_payload()          
    packet[ICMP].add_payload(payload_bytes)  

    return packet



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
    except (socket.error, socket.timeout):
        return None
    
    return response


def get_UDP_payload_size(packet):
    """
    Return the size (in bytes) of the UDP payload.
    """
    if packet.haslayer(Raw):
        payload = packet[Raw].load
    else:
        payload = b""
    return len(payload)


def send_echo_once_tcp (ip, port, message, timeout=0.5):
    """
    Open a TCP connection to the echo server, send the message,
    receive any echoed data, then close the connection.
    Returns the echoed string or None on error/timeout.
    """
    response = b""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            s.sendall(message.encode())

            # Read all available data until no more arrives or timeout
            while True:
                ready_to_read, _, _ = select.select([s], [], [], timeout)
                if ready_to_read:
                    chunk = s.recv(4096)
                    if not chunk:
                        break  # Server closed connection
                    response += chunk
                else:
                    break  # No more data within 'timeout' seconds
    except (socket.error, socket.timeout):
        return None

    return response.decode('utf-8', errors='ignore')

def send_echo_once_udp(ip, port, message, timeout=0.5):
    """
    Send a single UDP datagram to (ip, port), then wait for up to 'timeout'
    seconds for the echo response. Return the echoed string or None on timeout/error.
    """
    response = b""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            # Send to the server
            s.sendto(message.encode(), (ip, port))
            # Wait to see if there's data to read
            ready_to_read, _, _ = select.select([s], [], [], timeout)
            if ready_to_read:
                data, _ = s.recvfrom(4096)
                response = data
            else:
                # No data returned within timeout
                return None
    except (socket.error, socket.timeout):
        return None

    return response.decode('utf-8', errors='ignore')

def send_https_sni_request(ip, port, request_packet, sni=None):
    """
    Send an HTTPS request with optional SNI and return the full response.

    Args:
        ip (str): The IP address to connect to.
        port (int): The port (usually 443).
        request_packet (bytes): The raw HTTP/1.1 request packet.
        sni (str): The server name to use in SNI. Defaults to ip if not provided.

    Returns:
        bytes or None: The raw HTTP response, or None if an error occurs.
    """
    response = b""
    context = ssl._create_unverified_context()
    
    try:
        with socket.create_connection((ip, port), timeout=2.0) as sock:
            with context.wrap_socket(sock, server_hostname=sni or ip) as tls_sock:
                tls_sock.settimeout(1.0)
                tls_sock.sendall(request_packet)

                while True:
                    ready, _, _ = select.select([tls_sock], [], [], 0.5)
                    if ready:
                        chunk = tls_sock.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                    else:
                        break
    except (socket.error, ssl.SSLError, TimeoutError):
        return None
    return response

def group_ports(ports):
    """
    Group consecutive ports into ranges.
    
    Args:
        ports (list): List of port numbers
        
    Returns:
        list: List of port numbers and ranges
    """
    if not ports:
        return []
        
    # Sort and remove duplicates
    ports = sorted(set(ports))
    result = []
    start = ports[0]
    prev = ports[0]
    
    for port in ports[1:]:
        if port == prev + 1:
            prev = port
        else:
            if start == prev:
                result.append(str(start))
            else:
                result.append(f"{start}-{prev}")
            start = port
            prev = port
    
    # Add the last range or single port
    if start == prev:
        result.append(str(start))
    else:
        result.append(f"{start}-{prev}")
        
    return result 




def send_tcp_dns_query(server_ip, server_port, domain, query_type="A"):
    dnsatypes = {
        1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX",
        16: "TXT", 28: "AAAA", 33: "SRV", 43: "DS",
        46: "RRSIG", 47: "NSEC", 48: "DNSKEY", 255: "ANY"
    }

    result = {"query": None, "response": None, "error": None}
    supported_types = ', '.join([f"{v}({k})" for k, v in dnsatypes.items()])
    lookup_by_name = {v.upper(): k for k, v in dnsatypes.items()}
    query_type_str = str(query_type).strip().upper()

    logging.debug(f"Received query_type: {query_type_str}")

    if query_type_str.isdigit():
        qtype = int(query_type_str)
        if qtype not in dnsatypes:
            result["error"] = f"Unsupported numeric query type: {query_type}.\nSupported types are: {supported_types}"
            logging.error(result["error"])
            return result
    else:
        qtype = lookup_by_name.get(query_type_str)
        if qtype is None:
            result["error"] = f"Unsupported string query type: {query_type}.\nSupported types are: {supported_types}"
            logging.error(result["error"])
            return result

    try:
        logging.debug(f"Building DNS query for domain {domain} with type {query_type_str} ({qtype})")
        dns_query = DNSRecord.question(domain, qtype=dnsatypes[qtype])
        dns_query.header.id = random.randint(0, 65535)
        query_packet = dns_query.pack()
        result["query"] = dns_query.toZone()

        logging.debug("Opening TCP socket")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            logging.debug(f"Connecting to {server_ip}:{server_port}")
            sock.connect((server_ip, server_port))

            length_prefix = struct.pack("!H", len(query_packet))
            logging.debug("Sending DNS query")
            sock.sendall(length_prefix + query_packet)

            logging.debug("Waiting for response")
            length_data = sock.recv(2)
            if len(length_data) < 2:
                result["error"] = "Incomplete length prefix"
                logging.error(result["error"])
                return result

            expected_length = struct.unpack("!H", length_data)[0]
            response_data = b""
            while len(response_data) < expected_length:
                chunk = sock.recv(expected_length - len(response_data))
                if not chunk:
                    break
                response_data += chunk

            logging.debug("Received response data")
            parsed_response = DNSRecord.parse(response_data)
            result["response"] = str(parsed_response).replace("\n", "").replace(";;", "")
            return result

    except Exception as e:
        result["error"] = f"Exception occurred: {str(e)}"
        logging.error("An error occurred while sending the TCP DNS query")
        return result

def send_udp_dns_query(server_ip, server_port, domain, query_type="A"):
    dnsatypes = {
        1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX",
        16: "TXT", 28: "AAAA", 33: "SRV", 43: "DS",
        46: "RRSIG", 47: "NSEC", 48: "DNSKEY", 255: "ANY"
    }

    result = {"query": None, "response": None, "error": None}
    supported_types = ', '.join([f"{v}({k})" for k, v in dnsatypes.items()])
    lookup_by_name = {v.upper(): k for k, v in dnsatypes.items()}
    query_type_str = str(query_type).strip().upper()

    logging.debug(f"Received query_type: {query_type_str}")

    if query_type_str.isdigit():
        qtype = int(query_type_str)
        if qtype not in dnsatypes:
            result["error"] = f"Unsupported numeric query type: {query_type}.\nSupported types are: {supported_types}"
            logging.error(result["error"])
            return result
    else:
        qtype = lookup_by_name.get(query_type_str)
        if qtype is None:
            result["error"] = f"Unsupported string query type: {query_type}.\nSupported types are: {supported_types}"
            logging.error(result["error"])
            return result

    try:
        logging.debug(f"Building DNS query for domain {domain} with type {query_type_str} ({qtype})")
        dns_query = DNSRecord.question(domain, qtype=dnsatypes[qtype])
        dns_query.header.id = random.randint(0, 65535)
        query_packet = dns_query.pack()
        result["query"] = dns_query.toZone()

        logging.debug("Opening UDP socket")
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2)
            logging.debug(f"Sending UDP DNS query to {server_ip}:{server_port}")
            sock.sendto(query_packet, (server_ip, server_port))

            logging.debug("Waiting for UDP response")
            response_data, _ = sock.recvfrom(4096)

            logging.debug("Received UDP response")
            parsed_response = DNSRecord.parse(response_data)
            result["response"] = str(parsed_response).replace("\n", "").replace(";;", "")
            return result

    except Exception as e:
        result["error"] = f"Exception occurred: {str(e)}"
        logging.error("An error occurred while sending the UDP DNS query")
        return result
