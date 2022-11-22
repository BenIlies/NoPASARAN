import argparse
import json

from scapy.all import *
from twisted.internet.threads import deferToThread
from twisted.internet import reactor

from modules.machines.machine import Machine
from modules.ipsec_tunnels.ipsec_conf import NodeIpsecConf, ProxyIpsecConf

#iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP 
#iptables -L "chain" --line-numbers

'''
  NEW FEATURES TO ADD:
  - RST and kernel
  - Logger
  - Exceptions


gérer les erreurs / exception handler avec evenement --> ex: interface down donc pas de packet sent 


DOCUMENTATION PAR FONCTIONS doctest
https://docs.python.org/3/library/doctest.html

https://docs.python-guide.org/writing/documentation/#:~:text=Sphinx,manual%20pages%2C%20and%20plain%20text

PARTIE SUR LE SWITCH
-> ADAPTER LES CONNEXION TCP/ UTILISATION ADRESSE IP PRIVEE POUR LE TUNNEL IPSEC ?
'''
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog='ROLE', 
    epilog="See '<command> --help' to read about a specific sub-command."
  )

  base_parser = argparse.ArgumentParser(add_help=False)
  subparsers = parser.add_subparsers(dest='role', help='role for testing the end to end connection')

  node_parser = subparsers.add_parser("NODE", help="set the role of the node as an endpoint for testing the end to end connection", parents=[base_parser])
  node_parser.add_argument("-s", "--scenario", required=True, help="JSON scenario file for the finite state machine")

  proxy_parser = subparsers.add_parser("PROXY", help="set the role of the node as a proxy for control link", parents=[base_parser])
  controller_configuration = None

  args = parser.parse_args()

  if args.role == 'NODE':
    xstate_json = json.load(open(args.scenario))
    machine = Machine(xstate_json=xstate_json)
    main_thread = deferToThread(machine.start)
    main_thread.addCallback(lambda _: reactor.stop())
    reactor.run()

  