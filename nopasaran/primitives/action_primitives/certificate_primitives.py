from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption

from datetime import datetime, timedelta

from nopasaran.decorators import parsing_decorator


class CertificatePrimitives:
    """
    Class containing Certificate action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def generate_private_key(inputs, outputs, state_machine):
        """
        Generate an RSA private key and store it in an output variable in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the generated private key.
            
            state_machine: The state machine object.

        Returns:
            None
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        state_machine.set_variable_value(outputs[0], private_key)

    @staticmethod
    @parsing_decorator(input_args=0, output_args=1)
    def prepare_certificate_subject(inputs, outputs, state_machine):
        """
        Prepare an empty certificate subject and store it in an output variable in the machine's state.

        Number of input arguments: 0

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the certificate subject.

            state_machine: The state machine object.

        Returns:
            None
        """
        subject = x509.Name([])
        state_machine.set_variable_value(outputs[0], subject)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_country_name(inputs, outputs, state_machine):
        """
        Add a country name attribute to the certificate subject.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the certificate subject.
                - The value of the country name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the updated certificate subject.

            state_machine: The state machine object.

        Returns:
            None
        """
        subject = state_machine.get_variable_value(inputs[0])
        country_name = state_machine.get_variable_value(inputs[1])

        oid = x509.NameOID.COUNTRY_NAME
        name_attribute = x509.NameAttribute(oid, country_name)

        if all(isinstance(attr, x509.NameAttribute) for attr in subject):
            updated_subject = x509.Name([*subject, name_attribute])
        else:
            updated_subject = x509.Name([name_attribute])

        state_machine.set_variable_value(outputs[0], updated_subject)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_state_or_province_name(inputs, outputs, state_machine):
        """
        Add a state or province name attribute to the certificate subject.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the certificate subject.
                - The value of the state or province name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the updated certificate subject.

            state_machine: The state machine object.

        Returns:
            None
        """
        subject = state_machine.get_variable_value(inputs[0])
        state_or_province_name = state_machine.get_variable_value(inputs[1])

        oid = x509.NameOID.STATE_OR_PROVINCE_NAME
        name_attribute = x509.NameAttribute(oid, state_or_province_name)

        if all(isinstance(attr, x509.NameAttribute) for attr in subject):
            updated_subject = x509.Name([*subject, name_attribute])
        else:
            updated_subject = x509.Name([name_attribute])

        state_machine.set_variable_value(outputs[0], updated_subject)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_locality_name(inputs, outputs, state_machine):
        """
        Add a locality name attribute to the certificate subject.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the certificate subject.
                - The value of the locality name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the updated certificate subject.

            state_machine: The state machine object.

        Returns:
            None
        """
        subject = state_machine.get_variable_value(inputs[0])
        locality_name = state_machine.get_variable_value(inputs[1])

        oid = x509.NameOID.LOCALITY_NAME
        name_attribute = x509.NameAttribute(oid, locality_name)

        if all(isinstance(attr, x509.NameAttribute) for attr in subject):
            updated_subject = x509.Name([*subject, name_attribute])
        else:
            updated_subject = x509.Name([name_attribute])

        state_machine.set_variable_value(outputs[0], updated_subject)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_organization_name(inputs, outputs, state_machine):
        """
        Add an organization name attribute to the certificate subject.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the certificate subject.
                - The value of the organization name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the updated certificate subject.

            state_machine: The state machine object.

        Returns:
            None
        """
        subject = state_machine.get_variable_value(inputs[0])
        organization_name = state_machine.get_variable_value(inputs[1])

        oid = x509.NameOID.ORGANIZATION_NAME
        name_attribute = x509.NameAttribute(oid, organization_name)

        if all(isinstance(attr, x509.NameAttribute) for attr in subject):
            updated_subject = x509.Name([*subject, name_attribute])
        else:
            updated_subject = x509.Name([name_attribute])

        state_machine.set_variable_value(outputs[0], updated_subject)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def add_common_name(inputs, outputs, state_machine):
        """
        Add a common name attribute to the certificate subject.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the certificate subject.
                - The value of the common name.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the updated certificate subject.

            state_machine: The state machine object.

        Returns:
            None
        """
        subject = state_machine.get_variable_value(inputs[0])
        common_name = state_machine.get_variable_value(inputs[1])

        oid = x509.NameOID.COMMON_NAME
        name_attribute = x509.NameAttribute(oid, common_name)

        if all(isinstance(attr, x509.NameAttribute) for attr in subject):
            updated_subject = x509.Name([*subject, name_attribute])
        else:
            updated_subject = x509.Name([name_attribute])

        state_machine.set_variable_value(outputs[0], updated_subject)

    @staticmethod
    @parsing_decorator(input_args=2, output_args=1)
    def build_certificate(inputs, outputs, state_machine):
        """
        Build a certificate using the provided private key and subject, and store it in an output variable in the machine's state.

        Number of input arguments: 2

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains two mandatory input arguments:
                - The name of the variable containing the private key.
                - The name of the variable containing the certificate subject.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the built certificate.

            state_machine: The state machine object.

        Returns:
            None
        """
        private_key = state_machine.get_variable_value(inputs[0])
        subject = state_machine.get_variable_value(inputs[1])

        validity_period = timedelta(days=365)
        today = datetime.utcnow()

        certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(subject)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(today)
            .not_valid_after(today + validity_period)
            .sign(private_key, hashes.SHA256(), default_backend())
        )
        state_machine.set_variable_value(outputs[0], certificate)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def convert_private_key_to_pem(inputs, outputs, state_machine):
        """
        Convert the private key to PEM format and store it in an output variable in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the private key.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the private key in PEM format.

            state_machine: The state machine object.

        Returns:
            None
        """
        private_key = state_machine.get_variable_value(inputs[0])
        private_key_pem = private_key.private_bytes(
            Encoding.PEM,
            PrivateFormat.TraditionalOpenSSL,
            NoEncryption()
        )
        state_machine.set_variable_value(outputs[0], private_key_pem)

    @staticmethod
    @parsing_decorator(input_args=1, output_args=1)
    def convert_certificate_to_pem(inputs, outputs, state_machine):
        """
        Convert the certificate to PEM format and store it in an output variable in the machine's state.

        Number of input arguments: 1

        Number of output arguments: 1

        Optional input arguments: No

        Optional output arguments: No

        Args:
            inputs (List[str]): The list of input variable names. It contains one mandatory input argument, which is the name of the variable containing the certificate.

            outputs (List[str]): The list of output variable names. It contains one mandatory output argument, which is the name of the variable to store the certificate in PEM format.

            state_machine: The state machine object.

        Returns:
            None
        """
        certificate = state_machine.get_variable_value(inputs[0])
        certificate_pem = certificate.public_bytes(Encoding.PEM)
        state_machine.set_variable_value(outputs[0], certificate_pem)
