from modules.controllers.factory import NodeFactory, ProxyFactory
from twisted.internet.ssl import Certificate, PrivateCertificate


class Controller():
    def __init__(self, root_certificate_file, own_private_certificate_file):        
        file_root = open(root_certificate_file, "rb")
        root_certificate = file_root.read()
        file_root.close()
        file_private = open(own_private_certificate_file, "rb")
        own_private_certificate = file_private.read()
        file_private.close()
        self._trusted_authority_certificate = Certificate.loadPEM(root_certificate)
        self._own_private_certificate = PrivateCertificate.loadPEM(own_private_certificate)

class NodeController(Controller):
    def __init__(self, state_machine, root_certificate_file, client_private_certificate_file, link_id):
        super().__init__(root_certificate_file, client_private_certificate_file)
        self._factory = NodeFactory(state_machine, link_id)

    def configure(self, dst_ip, dst_port):
        self.__dst_ip = dst_ip
        self.__dst_port = dst_port
    
    def start(self, reactor):
        reactor.connectSSL(self.__dst_ip, self.__dst_port, self._factory, self._own_private_certificate.options(self._trusted_authority_certificate))
        return self._factory.deferred

class ProxyController(Controller):
    def __init__(self, root_certificate_file, server_private_certificate_file):
        super().__init__(root_certificate_file, server_private_certificate_file)
        self._factory = ProxyFactory()

    def configure(self, src_port):
        self.__src_port = src_port

    def start(self, reactor):
        reactor.listenSSL(self.__src_port, self._factory, self._own_private_certificate.options(self._trusted_authority_certificate))
        return self._factory.deferred