import argparse
import json

from scapy.all import *
from twisted.internet import task

from modules.machines.machine import Machine
from modules.controllers.controller import NodeController, ProxyController

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
rechercher pour le control channel
dans les controleur --> bytes a lire pour séparation des données
'''

if __name__ == '__main__':
  '''
  parser = argparse.ArgumentParser()
  parser.add_argument("scenario_file", help="JSON scenario file for the finite state machine", type=str)
  parser.add_argument("-v","--variables-file", help="JSON variables for the scenario", type=str)
  args = parser.parse_args()
  xstate_json = json.load(open(args.scenario_file))
  if args.variables_file:
    machine = Machine(xstate_json=xstate_json, variables=json.load(open(args.variables_file)))
  else:
    machine = Machine(xstate_json=xstate_json)
  machine.start()
  print(machine.get_full_chain())
  '''
  parser = argparse.ArgumentParser(
    prog='ROLE', 
    epilog="See '<command> --help' to read about a specific sub-command."
  )

  base_parser = argparse.ArgumentParser(add_help=False)
  subparsers = parser.add_subparsers(dest='role', help='role for testing the end to end connection')
  base_parser.add_argument("-rc", "--root-certificate", required=True, help="trusted root certificate file")
  base_parser.add_argument("-pc", "--private-certificate", required=True, help="private certificate with private key file")

  node_parser = subparsers.add_parser("NODE", help="set the role of the node as an endpoint for testing the end to end connection", parents=[base_parser])
  node_parser.add_argument("-dh", "--destination-host", required=True, help="ip address of the proxy to connect to")
  node_parser.add_argument("-dp", "--destination-port", required=True, help="port of the proxy to connect to")
  node_parser.add_argument("-li", "--link-id", required=True, help="link identifier for peer connection")
  node_parser.add_argument("-s", "--scenario", required=True, help="JSON scenario file for the finite state machine")
  node_parser.add_argument("-v", "--variables", required=False, help="JSON variables file for the scenario")

  proxy_parser = subparsers.add_parser("PROXY", help="set the role of the node as a proxy for control link", parents=[base_parser])
  proxy_parser.add_argument("-lp", "--listening-port", required=True, help="listening port for the proxy")

  args = parser.parse_args()

  if args.role == 'NODE':
    xstate_json = json.load(open(args.scenario))
    if args.variables:
      machine = Machine(xstate_json=xstate_json, variables=json.load(open(args.variables)))
    else:
      machine = Machine(xstate_json=xstate_json)
    controller = NodeController(machine, args.root_certificate, args.private_certificate, args.link_id)

    controller.configure(args.destination_host, int(args.destination_port))
    task.react(controller.start)
  elif args.role == 'PROXY':
    controller = ProxyController(args.root_certificate, args.private_certificate)
    controller.configure(int(args.listening_port))
    task.react(controller.start)
