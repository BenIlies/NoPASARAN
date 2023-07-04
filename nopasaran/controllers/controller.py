import logging

from twisted.internet import reactor
from twisted.internet.ssl import Certificate, PrivateCertificate

from nopasaran.controllers.factory import WorkerClientFactory, WorkerServerFactory

class Controller:
    def __init__(self, root_certificate_file, own_private_certificate_file):
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
        with open(file_path, "rb") as cert_file:
            return cert_file.read()

    @staticmethod
    def _load_certificate(cert_data):
        return Certificate.loadPEM(cert_data)

    @staticmethod
    def _load_private_certificate(cert_data):
        return PrivateCertificate.loadPEM(cert_data)

class ClientController(Controller):
    def __init__(self, state_machine, variable, root_certificate_file, client_private_certificate_file):
        super().__init__(root_certificate_file, client_private_certificate_file)
        self.factory = WorkerClientFactory(state_machine, variable)

    def configure(self, dst_ip, dst_port):
        self.__dst_ip = dst_ip
        self.__dst_port = dst_port
        logging.info("[Control Channel] Client configuration complete. Destination: %s:%s", dst_ip, dst_port)

    def start(self):
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
    def __init__(self, state_machine, variable, root_certificate_file, server_private_certificate_file):
        super().__init__(root_certificate_file, server_private_certificate_file)
        self.factory = WorkerServerFactory(state_machine, variable)

    def configure(self, src_port):
        self.__src_port = src_port
        logging.info("[Control Channel] Server configuration complete. Source port: %s", src_port)

    def start(self):
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
