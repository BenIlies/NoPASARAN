from nopasaran.decorators import parsing_decorator
import socket
import struct
from scapy.all import sniff, UDP, IP, conf

class ReplayPrimitives:
    """
    Class containing packet replay primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=5, output_args=0)
    def replay_udp_packets(inputs, outputs, state_machine):
        """
        Replay UDP packets to a specific port multiple times using L3 sockets.

        Number of input arguments: 5
        Number of output arguments: 0
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains five mandatory input arguments:
                - The name of the variable containing the target IP address.
                - The name of the variable containing the source port.
                - The name of the variable containing the destination port.
                - The name of the variable containing the number of times to replay.
                - The name of the variable containing the payload to send.
            outputs (List[str]): No output arguments needed.
            state_machine: The state machine object.

        Returns:
            None
        """
        destination_ip = state_machine.get_variable_value(inputs[0])
        source_port = int(state_machine.get_variable_value(inputs[1]))
        destination_port = int(state_machine.get_variable_value(inputs[2]))
        replay_count = int(state_machine.get_variable_value(inputs[3]))
        payload = state_machine.get_variable_value(inputs[4])

        # Ensure payload is bytes
        if isinstance(payload, str):
            payload = payload.encode()

        payload_length = len(payload)

        # Create raw socket at IP level
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # IP header
        ip_total_length = 20 + 8 + payload_length  # IP header (20 bytes) + UDP header (8 bytes) + payload
        ip_header = struct.pack('!BBHHHBBH4s4s',
            69,  # Version (4) + IHL (5)
            0,   # Type of Service
            ip_total_length,  # Total Length
            0,   # Identification
            0,   # Flags and Fragment Offset
            64,  # TTL
            17,  # Protocol (UDP)
            0,   # Header Checksum (kernel will fill)
            socket.inet_aton('0.0.0.0'),  # Source IP (still 0.0.0.0)
            socket.inet_aton(destination_ip)  # Destination IP
        )

        # UDP header
        udp_length = 8 + payload_length
        udp_header = struct.pack('!HHHH',
            source_port,       # Source Port
            destination_port,  # Destination Port
            udp_length,        # Length (UDP header + payload)
            0                  # Checksum (optional)
        )

        # Combine headers and payload
        packet = ip_header + udp_header + payload

        # Replay the packet specified number of times
        for _ in range(replay_count):
            try:
                sock.sendto(packet, (destination_ip, 0))
            except Exception:
                continue

        sock.close()


    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def listen_udp_replays(inputs, outputs, state_machine):
        """
        Listen for UDP packets and return the count of packets received for a specific source IP and destination port.

        Number of input arguments: 3
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names:
                - The name of the variable containing the timeout in seconds.
                - The name of the variable containing the source IP to filter by.
                - The name of the variable containing the destination port to filter by.
            outputs (List[str]): The list of output variable names:
                - The name of the variable to store the dictionary of {"received": count} or {"received": None} if timeout.
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = float(state_machine.get_variable_value(inputs[0]))
        source_ip = state_machine.get_variable_value(inputs[1])
        destination_port = int(state_machine.get_variable_value(inputs[2]))

        results = {"received": 0}
        received_packets = False

        try:
            # Configure scapy for quiet operation
            conf.verb = 0

            # Sniff UDP packets matching source IP and destination port
            packets = sniff(
                filter=f"udp and src host {source_ip} and dst port {destination_port}",
                timeout=timeout,
                store=True
            )

            # Count matching packets
            count = 0
            for pkt in packets:
                if pkt.haslayer(UDP) and pkt.haslayer(IP):
                    if pkt[IP].src == source_ip and pkt[UDP].dport == destination_port:
                        count += 1

            if count > 0:
                results["received"] = count
                received_packets = True

        except Exception as e:
            print(f"Error in UDP packet capture: {str(e)}")
            results["received"] = None

        # If no packets were received, set to None
        if not received_packets:
            results["received"] = None

        state_machine.set_variable_value(outputs[0], results)