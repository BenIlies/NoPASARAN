from nopasaran.decorators import parsing_decorator
import socket
from scapy.all import IP, TCP, UDP, sniff, conf
from nopasaran.utils import group_ports


class PortProbingPrimitives:
    """
    Class containing port probing primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def probe_udp_ports(inputs, outputs, state_machine):
        """
        Send UDP packets to all possible ports (0-65535) using L3 sockets.

        Number of input arguments: 2
        Number of output arguments: 0
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the source port (int).
                - The name of the variable containing the target IP address (str).
            outputs (List[str]): No output arguments needed.
            state_machine: The state machine object.

        Returns:
            None
        """
        source_port = int(state_machine.get_variable_value(inputs[0]))
        destination_ip = state_machine.get_variable_value(inputs[1])

        # Create raw socket at IP level
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # Scan all possible UDP ports (0-65535)
        for port in range(65536):
            try:
                # Create UDP packet
                udp_packet = IP(dst=destination_ip)/UDP(sport=source_port, dport=port)
                # Send raw packet
                sock.sendto(bytes(udp_packet), (destination_ip, 0))
            except Exception:
                continue

        sock.close()

    @staticmethod
    @parsing_decorator(input_args=2, output_args=0)
    def probe_tcp_syn_ports(inputs, outputs, state_machine):
        """
        Send TCP SYN packets to all possible ports.

        Number of input arguments: 2
        Number of output arguments: 0
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the source port (int).
                - The name of the variable containing the target IP address (str).
            outputs (List[str]): No output arguments needed.
            state_machine: The state machine object.

        Returns:
            None
        """
        source_port = int(state_machine.get_variable_value(inputs[0]))
        destination_ip = state_machine.get_variable_value(inputs[1])

        # Create raw socket at IP level
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # Scan all possible TCP ports (0-65535)
        for port in range(65536):
            try:
                # Create SYN packet
                syn_packet = IP(dst=destination_ip)/TCP(sport=source_port, dport=port, flags='S')
                # Send raw packet
                sock.sendto(bytes(syn_packet), (destination_ip, 0))
            except Exception:
                continue

        sock.close()


    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def listen_tcp_probes(inputs, outputs, state_machine):
        """
        Listen for TCP probes and track which ports received traffic from a specific source IP.

        Number of input arguments: 2
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the timeout in seconds.
                - The name of the variable containing the source IP to track.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the dictionary of {"received": [ports]} or {"received": None} if timeout.
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = float(state_machine.get_variable_value(inputs[0]))
        source_ip = state_machine.get_variable_value(inputs[1])

        # Dictionary to store results: {"received": set()}
        results = {"received": set()}
        received_packets = False

        try:
            # Configure scapy for better performance
            conf.verb = 0
            
            # Create a packet list to store results
            packets = sniff(filter=f"tcp and src host {source_ip}", 
                          timeout=timeout,
                          store=True)  # Store packets for batch processing
            
            # Process all packets at once
            for pkt in packets:
                if pkt.haslayer(TCP) and pkt[IP].src == source_ip:
                    results["received"].add(pkt[TCP].dport)
                    received_packets = True

        except Exception:
            pass

        # If no packets were received, set to None
        if not received_packets:
            results["received"] = None
        else:
            # Convert set to list and group consecutive ports
            results["received"] = group_ports(list(results["received"]))

        state_machine.set_variable_value(outputs[0], results)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def listen_udp_probes(inputs, outputs, state_machine):
        """
        Listen for UDP probes and track which ports received traffic from a specific source IP.

        Number of input arguments: 2
        Number of output arguments: 1
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the timeout in seconds.
                - The name of the variable containing the source IP to track.
            outputs (List[str]): The list of output variable names. It contains one mandatory output argument:
                - The name of the variable to store the dictionary of {"received": [ports]} or {"received": None} if timeout.
            state_machine: The state machine object.

        Returns:
            None
        """
        timeout = float(state_machine.get_variable_value(inputs[0]))
        source_ip = state_machine.get_variable_value(inputs[1])

        # Dictionary to store results: {"received": set()}
        results = {"received": set()}
        received_packets = False

        try:
            # Configure scapy for better performance
            conf.verb = 0
            
            # Create a packet list to store results
            packets = sniff(filter=f"udp and src host {source_ip}", 
                          timeout=timeout,
                          store=True)  # Store packets for batch processing
            
            # Process all packets at once
            for pkt in packets:
                if pkt.haslayer(UDP) and pkt[IP].src == source_ip:
                    results["received"].add(pkt[UDP].dport)
                    received_packets = True

        except Exception:
            pass

        # If no packets were received, set to None
        if not received_packets:
            results["received"] = None
        else:
            # Convert set to list and group consecutive ports
            results["received"] = group_ports(list(results["received"]))

        state_machine.set_variable_value(outputs[0], results)
