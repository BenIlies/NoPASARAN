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
        prog='NoPASARAN',
        description='NoPASARAN: Internet Route Testing Framework for Network Middleboxes',
        epilog="See '<command> --help' for more information."
    )

    # Add arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-l", "--log", dest="log_file", default="conf.log", help="Path to the log file (default: %(default)s)")
    parser.add_argument("-ll", "--log-level", choices=["debug", "info", "warning", "error"], help="Log level for output")
    parser.add_argument("-t", "--test", required=True, help="JSON file for the state machine indicating the test the Worker has to run")

    # Parse command line arguments
    args = parser.parse_args()

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

    logging.info('[Main] Loading JSON test file...')
    try:
        with open(args.test) as f:
            state_json = json.load(f)
    except Exception as e:
        logging.error(f'[Main] Error loading JSON test file: {str(e)}')
        return

    logging.info('[Main] JSON test file loaded')
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
