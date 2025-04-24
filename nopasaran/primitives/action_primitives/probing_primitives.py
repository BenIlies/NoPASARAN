from nopasaran.decorators import parsing_decorator
import socket
import threading
import time
from scapy.all import IP, TCP, UDP

class PortProbingPrimitives:
    """
    Class containing port probing primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def probe_udp_ports(inputs, outputs, state_machine):
        """
        Send UDP packets to all possible ports (0-65535) using L3 sockets.

        Number of input arguments: 1
        Number of output arguments: 0
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the target IP address.
            outputs (List[str]): No output arguments needed.
            state_machine: The state machine object.

        Returns:
            None
        """
        destination_ip = state_machine.get_variable_value(inputs[0])
        
        # Create raw socket at IP level
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        # Scan all possible UDP ports (0-65535)
        for port in range(65536):
            try:
                # Create UDP packet
                udp_packet = IP(dst=destination_ip)/UDP(dport=port)
                # Send raw packet
                sock.sendto(bytes(udp_packet), (destination_ip, 0))
            except Exception:
                continue
                
        sock.close()

    @staticmethod
    @parsing_decorator(input_args=1, output_args=0)
    def probe_tcp_syn_ports(inputs, outputs, state_machine):
        """
        Send TCP SYN packets to all possible ports.

        Number of input arguments: 1
        Number of output arguments: 0
        Optional input arguments: No
        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the target IP address.
            outputs (List[str]): No output arguments needed.
            state_machine: The state machine object.

        Returns:
            None
        """
        destination_ip = state_machine.get_variable_value(inputs[0])
        
        # Create raw socket at IP level
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        # Scan all possible TCP ports (0-65535)
        for port in range(65536):
            try:
                # Create SYN packet
                syn_packet = IP(dst=destination_ip)/TCP(dport=port, flags='S')
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
        packet_queue = []

        try:
            # Create TCP socket
            tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            tcp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Bind to all interfaces
            tcp_sock.bind(('0.0.0.0', 0))
            tcp_sock.settimeout(timeout)

            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    # Try to receive TCP packet
                    tcp_data, addr = tcp_sock.recvfrom(65535)
                    packet_queue.append((tcp_data, addr))
                except socket.timeout:
                    break
                except Exception:
                    continue

        except Exception:
            pass
        finally:
            tcp_sock.close()

        # Process all collected packets
        for tcp_data, addr in packet_queue:
            if addr[0] == source_ip:
                # Extract destination port from TCP header (bytes 2-3)
                dest_port = int.from_bytes(tcp_data[2:4], byteorder='big')
                results["received"].add(dest_port)
                received_packets = True

        # If no packets were received, set to None
        if not received_packets:
            results["received"] = None
        else:
            # Convert set to list for JSON serialization
            results["received"] = list(results["received"])

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
        packet_queue = []

        try:
            # Create UDP socket
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
            udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Bind to all interfaces
            udp_sock.bind(('0.0.0.0', 0))
            udp_sock.settimeout(timeout)

            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    # Try to receive UDP packet
                    udp_data, addr = udp_sock.recvfrom(65535)
                    packet_queue.append((udp_data, addr))
                except socket.timeout:
                    break
                except Exception:
                    continue

        except Exception:
            pass
        finally:
            udp_sock.close()

        # Process all collected packets
        for udp_data, addr in packet_queue:
            if addr[0] == source_ip:
                # Extract destination port from UDP header (bytes 2-3)
                dest_port = int.from_bytes(udp_data[2:4], byteorder='big')
                results["received"].add(dest_port)
                received_packets = True

        # If no packets were received, set to None
        if not received_packets:
            results["received"] = None
        else:
            # Convert set to list for JSON serialization
            results["received"] = list(results["received"])

        state_machine.set_variable_value(outputs[0], results)
