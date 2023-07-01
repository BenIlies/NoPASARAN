from ipsecparse import loads
from collections import OrderedDict
import os

class IpsecConf():
    """
    The IpsecConf class provides the functionality to load and configure the IPsec
    configuration file located at /etc/ipsec.conf. It has methods to both set up
    the configuration and to run the IPsec service using the newly created configuration.

    For more information on how to setup and configure StrongSwan, an open-source IPsec-based 
    VPN Solution, visit: https://wiki.strongswan.org/projects/strongswan/wiki/UserDocumentation
    """
    def configure_ipsec(self, controller_section, left='', leftsubnet='', right='', rightsubnet='', leftcert='', leftid='', rightid=''):
        """
        This method sets the parameters for the IPsec service. It takes as arguments 
        identifiers and addresses for two nodes (the 'left' and 'right' nodes) 
        as well as their respective subnets, certificates, and IDs. The method creates
        an IPsec connection configuration for these two nodes in the 'controller_section' 
        of the /etc/ipsec.conf file. It removes any previous configurations for this section.
        If any of the arguments are empty strings, they are not included in the new configuration.
        The method then writes the new configuration to the /etc/ipsec.conf file.

        Args:
            controller_section (str): Controller section name.
            left (str): Left IP.
            leftsubnet (str): Left Subnet.
            right (str): Right IP.
            rightsubnet (str): Right Subnet.
            leftcert (str): Left Certificate.
            leftid (str): Left ID.
            rightid (str): Right ID.
        """
        conf = loads(open('/etc/ipsec.conf').read())

        if ('conn', controller_section) in conf:
            del conf['conn', controller_section]

        conf['conn', controller_section] = OrderedDict(
            left=left,
            leftsubnet=leftsubnet,
            right=right,
            rightsubnet=rightsubnet,
            ike='aes256-sha2_256-modp1024!',
            esp='aes256-sha2_256!',
            keyingtries='0',
            ikelifetime='1h',
            lifetime='8h',
            dpddelay='30',
            dpdtimeout='120',
            dpdaction='restart',
            leftcert=leftcert,
            leftid=leftid,
            rightid=rightid,
            auto='start',
            keyexchange='ikev2',
            type='tunnel',
            forceencaps='yes'
        )	

        empty_keys = [k for k, v in conf['conn', controller_section].items() if v == '']
        for empty_key in empty_keys:
            del conf['conn', controller_section][empty_key]

        with open('/etc/ipsec.conf', 'w') as fd:
            fd.write(conf.dumps())

    def run(self):
        """
        This method simply executes the 'ipsec restart' command, which 
        restarts the IPsec service. This applies any changes made to the configuration file.
        """
        os.system('ipsec restart')


class ProxyIpsecConf(IpsecConf):
    """
    The ProxyIpsecConf class is a specialized version of the IpsecConf class 
    for the proxy's IPsec configuration. It is initialized with a left certificate and left ID,
    and it sets up an IPsec connection from the proxy to any node ('%any') 
    on the 192.0.0.0/24 subnet.
    """
    def __init__(self, leftcert, leftid):
        """
        Initializer for the ProxyIpsecConf class.
        Args:
            leftcert (str): Left Certificate.
            leftid (str): Left ID.
        """
        self.configure_ipsec(controller_section='tunnel-to-node', leftsubnet='192.0.0.0/24', right='%any', rightsubnet='192.0.0.0/24', leftcert=leftcert, leftid=leftid)

class WorkerIpsecConf(IpsecConf):
    """
    The WorkerIpsecConf class is a specialized version of the IpsecConf class
    for a worker's IPsec configuration. It is initialized with a right IP, right subnet,
    left certificate, left ID, and right ID, and sets up an IPsec connection from the worker
    to a specific proxy on the 192.0.0.0/24 subnet.
    """
    def __init__(self, right, rightsubnet, leftcert, leftid, rightid):
        """
        Initializer for the WorkerIpsecConf class.
        Args:
            right (str): Right IP.
            rightsubnet (str): Right Subnet.
            leftcert (str): Left Certificate.
            leftid (str): Left ID.
            rightid (str): Right ID.
        """
        self.configure_ipsec(controller_section='tunnel-to-proxy', left='%any', leftsubnet='192.0.0.0/24', right=right, rightsubnet=rightsubnet, leftcert=leftcert, leftid=leftid, rightid=rightid)
