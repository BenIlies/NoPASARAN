import argparse
import json
import logging
from twisted.internet.threads import deferToThread
from twisted.internet import reactor
from nopasaran.machines.machine import Machine

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        prog='ROLE',
        description='NoPASARAN: Internet Route Testing Framework for Network Middleboxes',
        epilog="See '<command> --help' for more information on a command."
    )

    # Set up base parser
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    base_parser.add_argument("--log", dest="log_file", default="conf.log", help="Path to the log file (default: %(default)s)")
    base_parser.add_argument("--log-level", choices=["info", "warning", "error"], help="Log level for output")

    # Create subparsers for the role
    subparsers = parser.add_subparsers(dest='role', help='Define the role for the machine in the architecture')

    # Parser for WORKER role
    worker_parser = subparsers.add_parser("WORKER", help="The Worker performs a test campaign to evaluate network middleboxes. It can be either the client machine that tests its connection path to another endpoint or a trusted machine registered in the network.", parents=[base_parser])
    worker_parser.add_argument("-s", "--scenario", required=True, help="JSON scenario file for the state machine indicating the test campaign the Worker has to run")

    # Parser for PROXY role
    proxy_parser = subparsers.add_parser("PROXY", help="The Proxy does not perform any tests. It should be accessible to remote Workers, allowing them to communicate when they are unreachable from the Internet, such as when blocked by a firewall.", parents=[base_parser])

    # Parse command line arguments
    args = parser.parse_args()

    # If role is not selected, print help message
    if args.role is None:
        parser.print_help()
        return

    # Set log level based on debug flag or --log-level argument
    log_level = logging.DEBUG if hasattr(args, 'debug') and args.debug else getattr(logging, args.log_level.upper()) if hasattr(args, 'log_level') and args.log_level else logging.INFO

    # Configure logging
    log_file = getattr(args, 'log_file', 'conf.log')
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p %Z'
    )

    # If role is WORKER, load JSON file and start the machine
    if args.role == 'WORKER':
        if not args.scenario:
            parser.error("The 'WORKER' role requires the '--scenario' argument.")
            return

        logging.info('Loading JSON scenario file...')
        try:
            xstate_json = json.load(open(args.scenario))
        except Exception as e:
            logging.error(f'Error loading JSON scenario file: {str(e)}')
            return

        logging.info('JSON scenario file loaded')
        machine = Machine(xstate_json=xstate_json)

        logging.info('Starting the machine')
        try:
            deferToThread(machine.start).addCallback(lambda _: reactor.stop())
            reactor.run()
        except Exception as e:
            logging.error(f'Error starting the machine: {str(e)}')

    logging.info('Application finished')

main()
