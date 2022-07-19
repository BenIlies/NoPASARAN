import argparse
import json

from scapy.all import *
from twisted.internet import task

from modules.machines.machine import Machine
from modules.controllers.controller import ClientController, NodeController, ProxyController, ServerController
from modules.ipsec_tunnels.ipsec_conf import NodeIpsecConf, ProxyIpsecConf

#iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP 
#iptables -L "chain" --line-numbers

'''
  NEW FEATURES TO ADD:
  - Check sniffer filter/loop
  - RST and kernel
  - Logger
  - Exceptions
  - Controller
  - Server/Side


gérer les erreurs / exception handler avec evenement --> ex: interface down donc pas de packet sent

machine état finie rajouter les controles sur les différents états 
garder un lien pour cas ou pas de serveur dans la machine a état fini 


DOCUMENTATION PAR FONCTIONS doctest
https://docs.python.org/3/library/doctest.html

supprimer l'ancienne partie sur le controlleur
'''

'''
conn tunnel-to-proxy
        left=%any
        leftsubnet=192.0.0.0/24
        right=11.11.11.3
        rightsubnet=192.0.0.0/24
        ike=aes256-sha2_256-modp1024!
        esp=aes256-sha2_256!
        keyingtries=0
        ikelifetime=1h
        lifetime=8h
        dpddelay=30
        dpdtimeout=120
        dpdaction=restart
        leftcert=c1Cert.pem
        leftid="C=CH, O=c1, CN=c1"
        rightid="C=CH, O=proxy, CN=proxy"
        auto=start
        keyexchange=ikev2
        type=tunnel
        forceencaps=yes

conn tunnel-to-node
        leftsubnet=192.0.0.0/24
        right=%any
        rightsubnet=192.0.0.0/24
        ike=aes256-sha2_256-modp1024!
        esp=aes256-sha2_256!
        keyingtries=0
        ikelifetime=1h
        lifetime=8h
        dpddelay=30
        dpdtimeout=120
        dpdaction=restart
        leftcert=proxyCert.pem
        leftid="C=CH, O=proxy, CN=proxy"
        auto=start
        keyexchange=ikev2
        type=tunnel
        forceencaps=yes

  #ProxyIpsecConf(leftcert='proxyCert.pem', leftid='C=CH, O=proxy, CN=proxy')
  #NodeIpsecConf(right='11.11.11.3',leftcert='c1Cert.pem', leftid='C=CH, O=c1, CN=c1', rightid='C=CH, O=proxy, CN=proxy')
'''

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog='ROLE', 
    epilog="See '<command> --help' to read about a specific sub-command."
  )

  base_parser = argparse.ArgumentParser(add_help=False)
  subparsers = parser.add_subparsers(dest='role', help='role for testing the end to end connection')
  base_parser.add_argument("-c", "--controller-configuration", required=True, help="JSON controller configuration file for the parameters of the control link")

  node_parser = subparsers.add_parser("NODE", help="set the role of the node as an endpoint for testing the end to end connection", parents=[base_parser])
  node_parser.add_argument("-s", "--scenario", required=True, help="JSON scenario file for the finite state machine")
  node_parser.add_argument("-v", "--variables", required=False, help="JSON variables file for the scenario")

  proxy_parser = subparsers.add_parser("PROXY", help="set the role of the node as a proxy for control link", parents=[base_parser])

  args = parser.parse_args()
  controller_configuration = json.load(open(args.controller_configuration))
  if args.role == 'NODE':
    xstate_json = json.load(open(args.scenario))
    if args.variables:
      machine = Machine(xstate_json=xstate_json, variables=json.load(open(args.variables)))
    else:
      machine = Machine(xstate_json=xstate_json)
    ipsec = NodeIpsecConf(right=controller_configuration['ipsec_proxy_ip'] , leftcert=controller_configuration['ipsec_certificate'], leftid=controller_configuration['ipsec_local_id'], rightid=controller_configuration['ipsec_remote_id'])
    #ipsec.run()
    print(controller_configuration['role'])
    if controller_configuration['role'] == 'client':
      controller = ClientController(machine, controller_configuration['root_certificate'], controller_configuration['private_certificate'])
      controller.configure(controller_configuration['destination_ip'], int(controller_configuration['destination_port']))
      task.react(controller.start)
    elif controller_configuration['role'] == 'server':
      controller = ServerController(machine, controller_configuration['root_certificate'], controller_configuration['private_certificate'])
      controller.configure(int(controller_configuration['listening_port']))
      task.react(controller.start)
  elif args.role == 'PROXY':
    print(controller_configuration)
    ipsec = ProxyIpsecConf(leftcert=controller_configuration['ipsec_certificate'], leftid=controller_configuration['ipsec_local_id'])
    #ipsec.run()