from nopasaran.decorators import parsing_decorator
import socket
import struct
from scapy.all import IP, TCP, UDP, sniff, conf

class ReplayPrimitives:
    """
    Class containing packet replay primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def replay_udp_packets(inputs, outputs, state_machine):
        """
        Replay UDP packets to a specific port multiple times using L3 sockets.

        Number of input arguments: 3
        Number of output arguments: 0
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the target IP address.
                - The name of the variable containing the destination port.
                - The name of the variable containing the number of times to replay.
            outputs (List[str]): No output arguments needed.
            state_machine: The state machine object.

        Returns:
            None
        """
        destination_ip = state_machine.get_variable_value(inputs[0])
        destination_port = int(state_machine.get_variable_value(inputs[1]))
        replay_count = int(state_machine.get_variable_value(inputs[2]))
        
        # Create raw socket at IP level
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        # Create UDP packet
        # IP header
        ip_header = struct.pack('!BBHHHBBH4s4s',
            69,  # Version and IHL
            0,   # Type of service
            20 + 8,  # Total length (IP header + UDP header)
            0,   # Identification
            0,   # Flags and fragment offset
            64,  # TTL
            17,  # Protocol (UDP)
            0,   # Header checksum
            socket.inet_aton('0.0.0.0'),  # Source IP
            socket.inet_aton(destination_ip)  # Destination IP
        )
        
        # UDP header
        udp_header = struct.pack('!HHHH',
            0,  # Source port
            destination_port,  # Destination port
            8,  # Length (UDP header)
            0   # Checksum
        )
        
        # Combine headers
        packet = ip_header + udp_header
        
        # Replay the packet specified number of times
        for _ in range(replay_count):
            try:
                sock.sendto(packet, (destination_ip, 0))
            except Exception:
                continue
                
        sock.close()

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def replay_tcp_syn_packets(inputs, outputs, state_machine):
        """
        Replay TCP SYN packets to a specific port multiple times using L3 sockets.

        Number of input arguments: 3
        Number of output arguments: 0
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the target IP address.
                - The name of the variable containing the destination port.
                - The name of the variable containing the number of times to replay.
            outputs (List[str]): No output arguments needed.
            state_machine: The state machine object.

        Returns:
            None
        """
        destination_ip = state_machine.get_variable_value(inputs[0])
        destination_port = int(state_machine.get_variable_value(inputs[1]))
        replay_count = int(state_machine.get_variable_value(inputs[2]))
        
        # Create raw socket at IP level
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        # Create TCP SYN packet
        # IP header
        ip_header = struct.pack('!BBHHHBBH4s4s',
            69,  # Version and IHL
            0,   # Type of service
            20 + 20,  # Total length (IP header + TCP header)
            0,   # Identification
            0,   # Flags and fragment offset
            64,  # TTL
            6,   # Protocol (TCP)
            0,   # Header checksum
            socket.inet_aton('0.0.0.0'),  # Source IP
            socket.inet_aton(destination_ip)  # Destination IP
        )
        
        # TCP header
        tcp_header = struct.pack('!HHLLBBHHH',
            0,  # Source port
            destination_port,  # Destination port
            0,  # Sequence number
            0,  # Acknowledgment number
            5 << 4,  # Data offset and reserved bits
            0x02,  # Flags (SYN)
            8192,  # Window size
            0,     # Checksum
            0      # Urgent pointer
        )
        
        # Combine headers
        packet = ip_header + tcp_header
        
        # Replay the packet specified number of times
        for _ in range(replay_count):
            try:
                sock.sendto(packet, (destination_ip, 0))
            except Exception:
                continue
                
        sock.close()

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def listen_tcp_replays(inputs, outputs, state_machine):
        """
        Listen for TCP packets and return the count of packets received.

        Number of input arguments: 3
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the timeout in seconds.
                - The name of the variable containing the source IP to filter by.
                - The name of the variable containing the destination port to filter by.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the dictionary of {"received": count} or {"received": None} if timeout.
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = float(state_machine.get_variable_value(inputs[0]))
        source_ip = state_machine.get_variable_value(inputs[1])
        destination_port = int(state_machine.get_variable_value(inputs[2]))

        # Dictionary to store results
        results = {"received": 0}

        try:
            # Configure scapy for better performance
            conf.verb = 0
            
            # Create a packet list to store results
            packets = sniff(filter=f"tcp and src host {source_ip} and dst port {destination_port}", 
                          timeout=timeout,
                          store=True)
            
            # Count packets
            for pkt in packets:
                if pkt.haslayer(TCP) and pkt[IP].src == source_ip:
                    results["received"] += 1

        except Exception:
            results["received"] = None

        state_machine.set_variable_value(outputs[0], results)

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def listen_udp_replays(inputs, outputs, state_machine):
        """
        Listen for UDP packets and return the count of packets received.

        Number of input arguments: 3
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments:
                - The name of the variable containing the timeout in seconds.
                - The name of the variable containing the source IP to filter by.
                - The name of the variable containing the destination port to filter by.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the dictionary of {"received": count} or {"received": None} if timeout.
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = float(state_machine.get_variable_value(inputs[0]))
        source_ip = state_machine.get_variable_value(inputs[1])
        destination_port = int(state_machine.get_variable_value(inputs[2]))

        # Dictionary to store results
        results = {"received": 0}

        try:
            # Configure scapy for better performance
            conf.verb = 0
            
            # Create a packet list to store results
            packets = sniff(filter=f"udp and src host {source_ip} and dst port {destination_port}", 
                          timeout=timeout,
                          store=True)
            
            # Count packets
            for pkt in packets:
                if pkt.haslayer(UDP) and pkt[IP].src == source_ip:
                    results["received"] += 1

        except Exception:
            results["received"] = None

        state_machine.set_variable_value(outputs[0], results)
