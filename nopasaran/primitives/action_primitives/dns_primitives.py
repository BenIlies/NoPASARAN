from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, DNSRROPT
import random
import string
import logging
from nopasaran.decorators import parsing_decorator


class DNSPrimitives:
    """
    Class containing DNS action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_DNS_packet(inputs, outputs, state_machine):
        """
        Create a DNS packet and store it in an output variable in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the created DNS packet.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = IP()/UDP()/DNS()
        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def disable_DNS_rd_flag(inputs, outputs, state_machine):
        """
        Disable the recursion desired (rd) flag in the DNS packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the DNS packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the modified DNS packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_packet['DNS'].rd = 0
        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def enable_DNS_rd_flag(inputs, outputs, state_machine):
        """
        Enable the recursion desired (rd) flag in the DNS packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the DNS packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the modified DNS packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_packet['DNS'].rd = 1
        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set_DNS_packet_query(inputs, outputs, state_machine):
        """
        Set the DNS packet as a query packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the DNS packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the modified DNS packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_packet['DNS'].qr = 0
        state_machine.set_variable_value(outputs[0], dns_packet)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def set_DNS_packet_response(inputs, outputs, state_machine):
        """
        Set the DNS packet as a response packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument:
                - The name of the variable containing the DNS packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the modified DNS packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_packet['DNS'].qr = 1
        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_DNS_transaction_id(inputs, outputs, state_machine):
        """
        Get the transaction ID from the DNS packet.
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_layer = None

        # Try to get the DNS layer directly
        if hasattr(dns_packet, 'haslayer') and dns_packet.haslayer(DNS):
            dns_layer = dns_packet.getlayer(DNS)

        # If no DNS layer, try to decode from Raw
        elif hasattr(dns_packet, 'haslayer') and dns_packet.haslayer('Raw'):
            try:
                dns_layer = DNS(dns_packet['Raw'].load)
            except Exception as e:
                logging.error(f"[Parsing] Failed to decode Raw payload as DNS: {e}")

        # Extract transaction ID if DNS layer is found
        if dns_layer:
            transaction_id = dns_layer.id
            state_machine.set_variable_value(outputs[0], transaction_id)
        else:
            logging.error("[Parsing] DNS layer not found in packet")
            state_machine.set_variable_value(outputs[0], None)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_DNS_transaction_id(inputs, outputs, state_machine):
        """
        Set the transaction ID in the DNS packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments. The first argument is the name of the variable containing the DNS packet, and the second argument is the name of the variable containing the new transaction ID.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the modified DNS packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        new_transaction_id = state_machine.get_variable_value(inputs[1])
        dns_packet['DNS'].id = new_transaction_id
        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_DNS_query(inputs, outputs, state_machine):
        """
        Create a DNS query (DNSQR) and store it in an output variable in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the created DNS query.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_query = DNSQR()
        state_machine.set_variable_value(outputs[0], dns_query)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_DNS_query_to_DNS_packet(inputs, outputs, state_machine):
        """
        Add a DNS query (DNSQR) to a DNS packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS packet.
                - The name of the variable containing the DNS query to be added.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the modified DNS packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_query = state_machine.get_variable_value(inputs[1])

        dns_packet['DNS'].qd = dns_query

        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_DNS_query_from_DNS_packet(inputs, outputs, state_machine):
        """
        Get the DNS query field (DNSQR) from a DNS packet.
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_layer = None

        # Try to get DNS layer directly if present
        if hasattr(dns_packet, 'haslayer') and dns_packet.haslayer(DNS):
            dns_layer = dns_packet.getlayer(DNS)

        # Attempt to decode Raw payload as DNS if DNS layer isn't directly present
        elif hasattr(dns_packet, 'haslayer') and dns_packet.haslayer('Raw'):
            try:
                dns_layer = DNS(dns_packet['Raw'].load)
            except Exception as e:
                logging.error(f"[Parsing] Failed to decode Raw payload as DNS: {e}")

        if dns_layer and getattr(dns_layer, "qd", None):
            dns_query = dns_layer.qd
            state_machine.set_variable_value(outputs[0], dns_query)
        else:
            logging.error("[Parsing] DNS query not found in packet")
            state_machine.set_variable_value(outputs[0], None)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_query_name(inputs, outputs, state_machine):
        """
        Set the domain name (qname) of a DNS query (DNSQR).

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS query.
                - The name of the variable containing the new query name (qname).

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the modified DNS query.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_query = state_machine.get_variable_value(inputs[0])
        new_query_name = state_machine.get_variable_value(inputs[1])
        dns_query.qname = new_query_name
        state_machine.set_variable_value(outputs[0], dns_query)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_query_name(inputs, outputs, state_machine):
        """
        Get the domain name (qname) of a DNS query (DNSQR).

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the DNS query.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the qualified domain name.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_query = state_machine.get_variable_value(inputs[0])
        qname = dns_query.qname.decode()

        state_machine.set_variable_value(outputs[0], qname)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_query_type(inputs, outputs, state_machine):
        """
        Set the query type (qtype) of a DNS query (DNSQR).

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS query.
                - The name of the variable containing the new query type.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the modified DNS query.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_query = state_machine.get_variable_value(inputs[0])
        new_query_type = state_machine.get_variable_value(inputs[1])
        dns_query.qtype = int(new_query_type)
        state_machine.set_variable_value(outputs[0], dns_query)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_query_class(inputs, outputs, state_machine):
        """
        Set the query class (qclass) of a DNS query (DNSQR).

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS query.
                - The name of the variable containing the new query class.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the modified DNS query.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_query = state_machine.get_variable_value(inputs[0])
        new_query_class = state_machine.get_variable_value(inputs[1])
        dns_query.qclass = new_query_class
        state_machine.set_variable_value(outputs[0], dns_query)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_DNS_resource_record(inputs, outputs, state_machine):
        """
        Create a DNS resource record without input arguments and store it in an output variable in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the created DNS resource record.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_resource_record = DNSRR()
        state_machine.set_variable_value(outputs[0], dns_resource_record)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_DNS_resource_record_domain(inputs, outputs, state_machine):
        """
        Set the domain name for a DNS resource record.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS resource record.
                - The name of the variable containing the domain name to set.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the modified DNS resource record.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_resource_record = state_machine.get_variable_value(inputs[0])
        domain_name = state_machine.get_variable_value(inputs[1])

        dns_resource_record.rrname = domain_name

        state_machine.set_variable_value(outputs[0], dns_resource_record)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_DNS_resource_record_value(inputs, outputs, state_machine):
        """
        Set the value for a DNS resource record.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS resource record.
                - The name of the variable containing the value to set.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the modified DNS resource record.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_resource_record = state_machine.get_variable_value(inputs[0])
        value = state_machine.get_variable_value(inputs[1])

        dns_resource_record.rdata = value

        state_machine.set_variable_value(outputs[0], dns_resource_record)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_DNS_resource_record_type(inputs, outputs, state_machine):
        """
        Set the record type for a DNS resource record.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS resource record.
                - The name of the variable containing the record type to set.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the modified DNS resource record.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_resource_record = state_machine.get_variable_value(inputs[0])
        record_type = state_machine.get_variable_value(inputs[1])

        dns_resource_record.type = record_type

        state_machine.set_variable_value(outputs[0], dns_resource_record)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_DNS_response_to_answer(inputs, outputs, state_machine):
        """
        Add a DNS response packet to the answer section of a DNS packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS packet.
                - The name of the variable containing the DNS response packet to be added to the answer section.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the modified DNS packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        response_packet = state_machine.get_variable_value(inputs[1])

        dns_packet['DNS'].an = response_packet

        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_DNS_answer_from_DNS_packet(inputs, outputs, state_machine):
        """
        Get the DNS answer field from a DNS packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the DNS packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the DNS answer.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_answer = dns_packet.an

        state_machine.set_variable_value(outputs[0], dns_answer)


    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_DNS_response_to_additional(inputs, outputs, state_machine):
        """
        Add a DNS response packet to the additional answer section of a DNS packet.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the DNS packet.
                - The name of the variable containing the DNS response packet to be added to the additional answer section.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is
                the name of the variable to store the modified DNS packet.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        additional_response = state_machine.get_variable_value(inputs[1])

        dns_packet['DNS'].ar = additional_response

        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_DNS_additional_answer_from_DNS_packet(inputs, outputs, state_machine):
        """
        Get the DNS additional answer field from a DNS packet.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the DNS packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the DNS additional answer.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_additional_answer = dns_packet.ar

        state_machine.set_variable_value(outputs[0], dns_additional_answer)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def append_random_label_to_qname(inputs, outputs, state_machine):
        """
        Append a random label to the existing qname in a DNS query packet.

        Number of input arguments: 1
        - The name of the variable containing the DNS packet (which must have a DNSQR layer).

        Number of output arguments: 1
        - The name of the variable to store the modified DNS packet.

        Args:
            inputs (List[str]): The list of input variable names, containing one mandatory argument:
                - The DNS query packet variable name.
            outputs (List[str]): The list of output variable names, containing one mandatory argument:
                - The modified DNS packet variable name.
            state_machine: The state machine object.
        """
     
        
        dns_packet = state_machine.get_variable_value(inputs[0])

        # Copy the packet so we don't mutate the original in place:
        dns_packet = dns_packet.copy()

        if not dns_packet.haslayer(DNSQR):
            state_machine.set_variable_value(outputs[0], dns_packet)
            return

        original_qname = dns_packet[DNSQR].qname.decode().rstrip('.')
        rand_label = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        new_qname = f"{rand_label}.{original_qname}"

        dns_packet[DNSQR].qname = new_qname.encode()
        state_machine.set_variable_value(outputs[0], dns_packet)


    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_dns_rcode_from_dns_packet(inputs, outputs, state_machine):
        """
        Extract the DNS RCODE (e.g., NXDOMAIN is 3) from a DNS packet.

        Number of input arguments: 1 (the name of the variable containing the DNS packet)
        Number of output arguments: 1 (the name of the variable to store the DNS rcode)

        Args:
            inputs (List[str]): The list of input variable names. 
                                inputs[0] is the variable name storing the DNS packet.
            outputs (List[str]): The list of output variable names.
                                outputs[0] is the variable name to store the DNS rcode.
            state_machine: Your state machine object for variable management.

        Returns:
            None
        """
        # Get the DNS packet from the state machine
        dns_packet = state_machine.get_variable_value(inputs[0])
        
        # Extract the DNS response code (0 = NoError, 3 = NXDOMAIN, etc.)
        dns_rcode = dns_packet.rcode
        
        # Store the rcode in the specified output variable
        state_machine.set_variable_value(outputs[0], dns_rcode)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def create_dns_query_packet_with_qdcount_mismatch (inputs, outputs, state_machine):
            """
            Create a malformed DNS packet (e.g., claims QDCOUNT=1 but provides no DNSQR).
            
            Number of input arguments: 0
            Number of output arguments: 1
            Optional input arguments: No
            Optional output arguments: No

            Args:
                inputs (List[str]): The list of input variable names. Not used in this method.
                outputs (List[str]): The list of output variable names. Contains one mandatory output argument:
                    - The name of the variable to store the malformed DNS packet.
                state_machine: The state machine object.

            Returns:
                None
            """
            # Create a baseline IP/UDP/DNS packet
            dns_packet = IP()/UDP()/DNS()

            dns_packet[DNS].qdcount = 1

            # ...but DO NOT actually attach a DNSQR object, so it's inconsistent and malformed
            dns_packet[DNS].qd = None

            # Store the malformed DNS packet in the state machine
            state_machine.set_variable_value(outputs[0], dns_packet)
    
    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def format_dns_query_packet(inputs, outputs, state_machine):
        """
        Extracts metadata from a DNS Query packet and stores the formatted dictionary.
        """
        packet = state_machine.get_variable_value(inputs[0])
        dns_layer = None

        # Try to get DNS layer directly
        if hasattr(packet, 'haslayer') and packet.haslayer(DNS):
            dns_layer = packet.getlayer(DNS)

        # Try to parse Raw layer if DNS is not present
        elif hasattr(packet, 'haslayer') and packet.haslayer('Raw'):
            try:
                dns_layer = DNS(packet['Raw'].load)
            except Exception as e:
                logging.error(f"[Parsing] Failed to decode Raw payload as DNS: {e}")
        
        # If DNS still not found, return error
        if not dns_layer:
            formatted_query = {"error": "No DNS layer found in packet"}
        else:
            formatted_query = {
                "transaction_id": dns_layer.id,
                "rd": dns_layer.rd,
                "opcode": dns_layer.opcode,
                "questions": []
            }

            if getattr(dns_layer, "qdcount", 0) > 0 and getattr(dns_layer, "qd", None):
                try:
                    formatted_query["questions"].append({
                        "qname": dns_layer.qd.qname.decode() if isinstance(dns_layer.qd.qname, bytes) else dns_layer.qd.qname,
                        "qtype": dns_layer.qd.qtype,
                        "qclass": dns_layer.qd.qclass
                    })
                except Exception as e:
                    logging.error(f"[Parsing] Error extracting DNS question: {e}")

            # Clean up empty or default values
            formatted_query = {k: v for k, v in formatted_query.items() if v not in [None, 0, "", [], {}]}

        state_machine.set_variable_value(outputs[0], formatted_query)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def format_dns_response_packet(inputs, outputs, state_machine):
        """
        Extracts metadata from a DNS Response packet and stores the formatted dictionary.
        """

        packet = state_machine.get_variable_value(inputs[0])

        dnsatypes = {
            1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX", 16: "TXT",
            28: "AAAA", 33: "SRV", 38: "A6", 43: "DS", 46: "RRSIG", 47: "NSEC",
            48: "DNSKEY", 255: "ANY"
        }

        dns_layer = None

        # Try to extract DNS layer directly or from Raw
        if hasattr(packet, 'haslayer') and packet.haslayer(DNS):
            dns_layer = packet.getlayer(DNS)
        elif hasattr(packet, 'haslayer') and packet.haslayer('Raw'):
            try:
                dns_layer = DNS(packet['Raw'].load)
            except Exception as e:
                logging.error(f"[Parsing] Failed to decode Raw payload as DNS: {e}")

        if not dns_layer:
            formatted_response = {"error": "No DNS layer found in packet"}
        else:
            formatted_response = {
                "transaction_id": dns_layer.id,
                "qr": dns_layer.qr,
                "opcode": dns_layer.opcode,
                "aa": dns_layer.aa,
                "tc": dns_layer.tc,
                "rd": dns_layer.rd,
                "ra": dns_layer.ra,
                "z": dns_layer.z,
                "rcode": dns_layer.rcode,
                "questions": [],
                "answers": []
            }

            # Parse questions
            try:
                if getattr(dns_layer, "qdcount", 0) > 0 and getattr(dns_layer, "qd", None):
                    question = dns_layer.qd
                    formatted_response["questions"].append({
                        "qname": question.qname.decode() if isinstance(question.qname, bytes) else question.qname,
                        "qtype": question.qtype,
                        "qtype_name": dnsatypes.get(question.qtype, f"Unknown({question.qtype})"),
                        "qclass": question.qclass
                    })
            except Exception as e:
                logging.error(f"[Parsing] Failed to parse DNS question: {e}")

            # Parse answers (assuming it's a list or iterable)
            try:
                answers = dns_layer.an
                if isinstance(answers, list):
                    answer_rrs = answers
                else:
                    answer_rrs = [answers]  # wrap single DNSRR for uniform handling

                for ans in answer_rrs:
                    if isinstance(ans, DNSRR):
                        answer_info = {
                            "rrname": ans.rrname.decode() if isinstance(ans.rrname, bytes) else ans.rrname,
                            "type": ans.type,
                            "type_name": dnsatypes.get(ans.type, f"Unknown({ans.type})"),
                            "rclass": ans.rclass,
                            "ttl": ans.ttl,
                            "rdata": ans.rdata.decode() if isinstance(ans.rdata, bytes) else str(ans.rdata),
                            "rdlen": getattr(ans, "rdlen", None)
                        }
                        formatted_response["answers"].append(answer_info)
            except Exception as e:
                logging.error(f"[Parsing] Failed to parse DNS answers: {e}")

        state_machine.set_variable_value(outputs[0], formatted_response)









