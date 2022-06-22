import argparse
import json

from scapy.all import *

from modules.machines.machine import Machine

#iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP 


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
  from twisted.internet import task
  from modules.controllers.controller import NodeController
  controller = NodeController("certificates/public.pem", "certificates/client.pem", "test")
  controller.configure("192.168.122.247", 8005)
  task.react(controller.start)
