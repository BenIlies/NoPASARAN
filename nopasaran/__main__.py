import argparse
import json
import logging
import sys
from twisted.internet.threads import deferToThread
from twisted.internet import reactor
from nopasaran.machines.state_machine import StateMachine

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        prog='ROLE',
        description='NoPASARAN: Internet Route Testing Framework for Network Middleboxes',
        epilog="See '<command> --help' for more information on a command."
    )

    # Set up base parser
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    # Add -l and -ll options as shorter names for --log and --log-level
    base_parser.add_argument("-l", "--log", dest="log_file", default="conf.log", help="Path to the log file (default: %(default)s)")
    base_parser.add_argument("-ll", "--log-level", choices=["debug", "info", "warning", "error"], help="Log level for output")

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

    # Set log level based on -ll argument
    log_level = getattr(logging, args.log_level.upper()) if args.log_level else logging.ERROR

    # Configure logging
    log_file = args.log_file
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p %Z'
    )

    # Set up console logging if -v option is provided
    if args.verbose:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        logging.getLogger().addHandler(console_handler)

    # If role is WORKER, load JSON file and start the machine
    if args.role == 'WORKER':
        if not args.scenario:
            parser.error("The 'WORKER' role requires the '--scenario' argument.")
            return

        logging.info('[Main] Loading JSON scenario file...')
        try:
            with open(args.scenario) as f:
                state_json = json.load(f)
        except Exception as e:
            logging.error(f'[Main] Error loading JSON scenario file: {str(e)}')
            return

        logging.info('[Main] JSON scenario file loaded')
        machine = StateMachine(state_json=state_json)

        logging.info('[Main] Starting the root machine')
        try:
            deferToThread(machine.start).addBoth(lambda _: reactor.stop())
            reactor.run()
        except Exception as e:
            logging.error(f'[Main] Error starting the machine: {str(e)}')

    logging.info('[Main] Application finished')

if __name__ == "__main__":
    main()