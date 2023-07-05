import logging

from twisted.internet import reactor
from twisted.internet.ssl import Certificate, PrivateCertificate

from nopasaran.controllers.factory import WorkerClientFactory, WorkerServerFactory


class Controller:
    """
    Base controller for managing the control channel.
    
    This controller handles loading certificates and provides common functionality for both client and server controllers.
    """

    def __init__(self, root_certificate_file, own_private_certificate_file):
        """
        Initialize the Controller.
        
        Args:
            root_certificate_file (str): The file path to the root certificate file.
            own_private_certificate_file (str): The file path to the own private certificate file.
        
        Raises:
            RuntimeError: If an error occurs while loading the control channel certificates.
        """
        try:
            root_cert_data = self._load_certificate_data(root_certificate_file)
            own_cert_data = self._load_certificate_data(own_private_certificate_file)
            self._trusted_authority_certificate = self._load_certificate(root_cert_data)
            self._own_private_certificate = self._load_private_certificate(own_cert_data)
            logging.info("[Control Channel] Control channel certificates loaded successfully.")
        except Exception as e:
            error_msg = f"Error loading control channel certificates: {str(e)}"
            logging.error("[Control Channel] " + error_msg)
            raise RuntimeError(error_msg)

    @staticmethod
    def _load_certificate_data(file_path):
        """
        Load certificate data from a file.
        
        Args:
            file_path (str): The file path to the certificate file.
        
        Returns:
            bytes: The certificate data.
        """
        with open(file_path, "rb") as cert_file:
            return cert_file.read()

    @staticmethod
    def _load_certificate(cert_data):
        """
        Load a certificate from certificate data.
        
        Args:
            cert_data (bytes): The certificate data.
        
        Returns:
            Certificate: The loaded certificate.
        """
        return Certificate.loadPEM(cert_data)

    @staticmethod
    def _load_private_certificate(cert_data):
        """
        Load a private certificate from certificate data.
        
        Args:
            cert_data (bytes): The certificate data.
        
        Returns:
            PrivateCertificate: The loaded private certificate.
        """
        return PrivateCertificate.loadPEM(cert_data)


class ClientController(Controller):
    """
    Controller for client-side control channel.
    
    This controller is used to configure and start the control channel for a client.
    """

    def __init__(self, state_machine, variable, root_certificate_file, client_private_certificate_file):
        """
        Initialize the ClientController.
        
        Args:
            state_machine: The state machine object.
            variable: The variable object.
            root_certificate_file (str): The file path to the root certificate file.
            client_private_certificate_file (str): The file path to the client private certificate file.
        """
        super().__init__(root_certificate_file, client_private_certificate_file)
        self.factory = WorkerClientFactory(state_machine, variable)

    def configure(self, dst_ip, dst_port):
        """
        Configure the client controller.
        
        Args:
            dst_ip (str): The destination IP address.
            dst_port (int): The destination port.
        """
        self.__dst_ip = dst_ip
        self.__dst_port = dst_port
        logging.info("[Control Channel] Client configuration complete. Destination: %s:%s", dst_ip, dst_port)

    def start(self):
        """
        Start the client controller.
        
        Raises:
            RuntimeError: If an error occurs while starting the client.
        """
        try:
            reactor.connectSSL(
                self.__dst_ip,
                self.__dst_port,
                self.factory,
                self._own_private_certificate.options(self._trusted_authority_certificate)
            )
            logging.info("[Control Channel] Client started. Control channel established on the client side.")
        except Exception as e:
            error_msg = f"Error starting client. Control channel failed on the client side: {str(e)}"
            logging.error("[Control Channel] " + error_msg)
            raise RuntimeError(error_msg)


class ServerController(Controller):
    """
    Controller for server-side control channel.
    
    This controller is used to configure and start the control channel for a server.
    """

    def __init__(self, state_machine, variable, root_certificate_file, server_private_certificate_file):
        """
        Initialize the ServerController.
        
        Args:
            state_machine: The state machine object.
            variable: The variable object.
            root_certificate_file (str): The file path to the root certificate file.
            server_private_certificate_file (str): The file path to the server private certificate file.
        """
        super().__init__(root_certificate_file, server_private_certificate_file)
        self.factory = WorkerServerFactory(state_machine, variable)

    def configure(self, src_port):
        """
        Configure the server controller.
        
        Args:
            src_port (int): The source port.
        """
        self.__src_port = src_port
        logging.info("[Control Channel] Server configuration complete. Source port: %s", src_port)

    def start(self):
        """
        Start the server controller.
        
        Raises:
            RuntimeError: If an error occurs while starting the server.
        """
        try:
            reactor.listenSSL(
                self.__src_port,
                self.factory,
                self._own_private_certificate.options(self._trusted_authority_certificate)
            )
            logging.info("[Control Channel] Server started. Control channel established on the server side.")
        except Exception as e:
            error_msg = f"Error starting server. Control channel failed on the server side: {str(e)}"
            logging.error("[Control Channel] " + error_msg)
            raise RuntimeError(error_msg)
