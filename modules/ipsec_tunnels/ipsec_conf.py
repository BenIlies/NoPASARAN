from ipsecparse import loads
from collections import OrderedDict
import os

class IpsecConf():
    def configure_ipsec(self, controller_section, left='', leftsubnet='', right='', rightsubnet='', leftcert='', leftid='', rightid=''):
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
        os.system('ipsec restart')


class ProxyIpsecConf(IpsecConf):
    def __init__(self, leftcert, leftid):
        self.configure_ipsec(controller_section='tunnel-to-node', leftsubnet='192.0.0.0/24', right='%any', rightsubnet='192.0.0.0/24', leftcert=leftcert, leftid=leftid)

class NodeIpsecConf(IpsecConf):
    def __init__(self, right, leftcert, leftid, rightid):
        self.configure_ipsec(controller_section='tunnel-to-proxy', left='%any', leftsubnet='192.0.0.0/24', right=right, rightsubnet='192.0.0.0/24', leftcert=leftcert, leftid=leftid, rightid=rightid)
