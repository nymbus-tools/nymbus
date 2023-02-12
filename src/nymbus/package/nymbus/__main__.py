import argparse
import logging
import os

from nymbus.cli.runner import Runner
from nymbus.cli.setupper import Setupper

logger = logging.getLogger(__name__)


def main():

    # Nymbus
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Print a stacktrace of errors", action="store_true")
    parser.set_defaults(action=lambda args: parser.parse_args(["-h"]))
    subparsers = parser.add_subparsers()

    # Setup
    setup = subparsers.add_parser("setup")
    setup.set_defaults(action=lambda args, rest: Setupper().manage(args.component))

    # Run
    run = subparsers.add_parser("run")
    run.add_argument("component", help="Path to the folder containing the <env>.yml files (relative or not)")
    run.add_argument("environment", help="Environment name (of the <env>.yml target file)")
    run.add_argument("--context", default=None, help="Path to the folder that will be visibile in docker steps")
    run.add_argument("--step", default=None, help="Step name (in the <env>.yml file)")
    run.set_defaults(action=lambda args, rest: Runner().run(args.component, args.environment, args.step, args.context))

    # Parse args
    arguments, remainder = parser.parse_known_args()

    try:

        # Invoke the corresponding functions
        arguments.action(arguments, remainder)
        logger.info("All done.")

    except Exception as e:

        if arguments.debug:
            logger.exception("")
        else:
            logger.error(e if str(e) else f"Error: {type(e)}")
        exit(1)


if __name__ == '__main__':
    main()
