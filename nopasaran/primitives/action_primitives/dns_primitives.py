from scapy.all import IP, UDP, DNS, DNSQR, DNSRR
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

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the DNS packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the transaction ID.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        transaction_id = dns_packet['DNS'].id
        state_machine.set_variable_value(outputs[0], transaction_id)

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

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the DNS packet.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the DNS query.

            state_machine: The state machine object.

        Returns:
            None
        """
        dns_packet = state_machine.get_variable_value(inputs[0])
        dns_query = dns_packet.qd

        state_machine.set_variable_value(outputs[0], dns_query)

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
        dns_query.qtype = new_query_type
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