from scapy.all import IP, UDP, DNS, DNSQR
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
    def disable_rd_flag(inputs, outputs, state_machine):
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
        dns_packet[DNS].rd = 0
        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def enable_rd_flag(inputs, outputs, state_machine):
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
        dns_packet[DNS].rd = 1
        state_machine.set_variable_value(outputs[0], dns_packet)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def get_transaction_id(inputs, outputs, state_machine):
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
        transaction_id = dns_packet[DNS].id
        state_machine.set_variable_value(outputs[0], transaction_id)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def set_transaction_id(inputs, outputs, state_machine):
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
        dns_packet[DNS].id = new_transaction_id
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

        dns_packet[DNS].qd = dns_query

        state_machine.set_variable_value(outputs[0], dns_packet)

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