from nopasaran.decorators import parsing_decorator
from scapy.all import sniff, UDP, IP, conf, Raw, send
import time
import logging

class ReplayPrimitives:
    """
    Class containing packet replay primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=7, output_args=0)
    def replay_udp_packets(inputs, outputs, state_machine):
        """
        Replay UDP packets to a specific port multiple times using Scapy in batches.

        Args:
            inputs (List[str]): The list of input variable names. It contains:
                - Target IP address.
                - Source port.
                - Destination port.
                - Number of packets per batch (batch_size).
                - Number of batches (num_batches).
                - Payload to send.
                - Time delay between batches in seconds.
            outputs (List[str]): No output arguments needed.
            state_machine: The state machine object.

        Returns:
            None
        """
        # Extracting the input values
        destination_ip = state_machine.get_variable_value(inputs[0])
        source_port = int(state_machine.get_variable_value(inputs[1]))
        destination_port = int(state_machine.get_variable_value(inputs[2]))
        batch_size = int(state_machine.get_variable_value(inputs[3]))
        num_batches = int(state_machine.get_variable_value(inputs[4]))
        payload = state_machine.get_variable_value(inputs[5])
        delay = float(state_machine.get_variable_value(inputs[6]))

        # Ensure the payload is in bytes if it's a string
        if isinstance(payload, str):
            payload = payload.encode()

        # Create the packet template
        packet = IP(dst=destination_ip) / UDP(sport=source_port, dport=destination_port) / Raw(load=payload)

        # Replay the packets in batches
        for batch_num in range(num_batches):
            logging.debug(f"Sending batch {batch_num + 1} of {num_batches}...")
            
            for _ in range(batch_size):
                try:
                    send(packet, verbose=False)  # Send each packet
                except Exception as e:
                    logging.debug(f"Error sending packet: {e}")
                    continue
            
            # Wait for the specified delay before sending the next batch
            if batch_num < num_batches - 1:  # Don't wait after the last batch
                logging.debug(f"Waiting for {delay} seconds before next batch...")
                time.sleep(delay)


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
            logging.debug(f"Error in UDP packet capture: {str(e)}")
            results["received"] = None

        # If no packets were received, set to None
        if not received_packets:
            results["received"] = None

        state_machine.set_variable_value(outputs[0], results)