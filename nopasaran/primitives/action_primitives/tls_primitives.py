import ssl
import socket
import tempfile
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from nopasaran.definitions.events import EventNames
from nopasaran.decorators import parsing_decorator
import nopasaran.utils as utils

class TLSPrimitives:
    """
    Class containing TLS action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=3, output_args=1)
    def get_certificate(inputs, outputs, state_machine):
        """
        Retrieve the certificate from a given IP address, port, and hostname, and store it in an output variable in the machine's state.

        Number of input arguments: 3

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains three mandatory input arguments (IP address, port, and hostname).

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the retrieved certificate.

            state_machine: The state machine object.

        Returns:
            None
        """
        ip_address = state_machine.get_variable_value(inputs[0])
        port = int(state_machine.get_variable_value(inputs[1]))
        hostname = state_machine.get_variable_value(inputs[2])

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conn.connect((ip_address, port))
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

    @staticmethod
    @parsing_decorator(input_args=5, output_args=0)
    def start_ssl_server(inputs, outputs, state_machine):
        """
        Start an SSL server with the given certificate, key, host, port, and timeout.

        Number of input arguments: 5

        Number of output arguments: 0

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains five mandatory input arguments:
                - The name of the variable containing the certificate bytes.
                - The name of the variable containing the key bytes.
                - The name of the variable containing the host.
                - The name of the variable containing the port.
                - The name of the variable containing the timeout.

            outputs (List[str]): The list of output variable names. (None for this method)

            state_machine: The state machine object.

        Returns:
            None
        """
        cert_bytes = state_machine.get_variable_value(inputs[0])
        key_bytes = state_machine.get_variable_value(inputs[1])
        host = state_machine.get_variable_value(inputs[2])
        port = int(state_machine.get_variable_value(inputs[3]))
        timeout = float(state_machine.get_variable_value(inputs[4]))

        # Create a socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        server_socket.settimeout(timeout)  # Set the timeout for accepting connections

        # Create temporary files for the certificate and key
        with tempfile.NamedTemporaryFile(delete=True) as cert_tempfile, tempfile.NamedTemporaryFile(delete=True) as key_tempfile:
            cert_tempfile.write(cert_bytes)
            cert_tempfile.flush()
            key_tempfile.write(key_bytes)
            key_tempfile.flush()

            # Wrap the socket with SSL
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=cert_tempfile.name, keyfile=key_tempfile.name)

            try:
                # Accept and handle a single client connection
                client_socket, _ = server_socket.accept()
                ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
                utils.handle_client_connection(ssl_client_socket)
                state_machine.trigger_event(EventNames.CONNECTION_ENDING.name)
            except socket.timeout:
                state_machine.trigger_event(EventNames.TIMEOUT.name)
            except Exception:
                state_machine.trigger_event(EventNames.ERROR.name)
            finally:
                # Close the server socket
                server_socket.close()
                
