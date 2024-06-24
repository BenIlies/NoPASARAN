import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from nopasaran.decorators import parsing_decorator

class TLSPrimitives:
    """
    Class containing TLS action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def get_certificate(inputs, outputs, state_machine):
        """
        Retrieve the certificate from a given hostname and port, and store it in an output variable in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments (hostname and port).

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the retrieved certificate.

            state_machine: The state machine object.

        Returns:
            None
        """
        hostname = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conn.connect((hostname, port))
        cert_bin = conn.getpeercert(True)
        conn.close()

        cert_pem = ssl.DER_cert_to_PEM_cert(cert_bin)
        state_machine.set_variable_value(outputs[0], cert_pem)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def extract_public_key(inputs, outputs, state_machine):
        """
        Extract the public key from a PEM-encoded certificate and store it in an output variable in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the PEM-encoded certificate.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the extracted public key in PEM format.

            state_machine: The state machine object.

        Returns:
            None
        """
        cert_pem = state_machine.get_variable_value(inputs[0])
        cert = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())

        public_key = cert.public_key()

        pub_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        state_machine.set_variable_value(outputs[0], pub_key_pem.decode('utf-8'))
