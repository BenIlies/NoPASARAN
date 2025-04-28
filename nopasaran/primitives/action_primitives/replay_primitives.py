from nopasaran.decorators import parsing_decorator
import socket
import struct
from nopasaran.sniffers.udp_probe_listener import UDPProbeListener

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

        results = {"received": 0}

        try:
            listener = UDPProbeListener(source_ip=source_ip, timeout=timeout, dports=[destination_port])
            listener.run()

            port_count = listener.port_counts.get(destination_port, 0)
            results["received"] = port_count if port_count > 0 else None

        except Exception as e:
            print(f"Error in UDP packet capture: {str(e)}")
            results["received"] = None

        state_machine.set_variable_value(outputs[0], results)