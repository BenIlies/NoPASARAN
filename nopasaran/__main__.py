# Import libraries
import argparse
import json
from scapy.all import *
from twisted.internet.threads import deferToThread
from twisted.internet import reactor
from nopasaran.machines.machine import Machine

def main():
  # Set up argument parser
  parser = argparse.ArgumentParser(
    prog='ROLE', 
    epilog="See '<command> --help' for more information on a command."
  )

  # Set up base parser
  base_parser = argparse.ArgumentParser(add_help=False)

  # Create subparsers for the role 
  subparsers = parser.add_subparsers(dest='role', help='Define role for testing the connection')

  # Parser for NODE role
  node_parser = subparsers.add_parser("NODE", help="Define node role for testing", parents=[base_parser])
  node_parser.add_argument("-s", "--scenario", required=True, help="JSON scenario file for state machine")

  # Parser for PROXY role
  proxy_parser = subparsers.add_parser("PROXY", help="Define node role as a proxy", parents=[base_parser])

  # Parse command line arguments
  args = parser.parse_args()

  # If role is NODE, load JSON file and start the machine
  if args.role == 'NODE':
    xstate_json = json.load(open(args.scenario))
    machine = Machine(xstate_json=xstate_json)
    main_thread = deferToThread(machine.start)
    main_thread.addCallback(lambda _: reactor.stop())
    reactor.run()

main()