#!/usr/bin/env python3

import argparse
import logging
from time import gmtime, strftime

try:
    from .. import apples
except (ImportError, ValueError):
    try:
        import apples
    except (ImportError, ValueError):
        raise Exception("APPLES __init__.py not downloaded. " +
                        "Get it from https://github.com/The-Randalorian/APPLES/tree/0.2.0-Refactor.")


if __name__ == "__main__":
    # Totally cribbed from https://stackoverflow.com/questions/57192387/how-to-set-logging-level-from-command-line
    parser = argparse.ArgumentParser()
    parser.add_argument("-log",
                        "--loglevel",
                        default="warning",
                        help="Provide logging level. Example --loglevel debug, default=warning")
    parser.add_argument("-logfile",
                        "--logfile",
                        default=__file__[:-11] + "apples.log",
                        help="Provide logfile URL. Example --logfile apples.log, default=(empty)")

    args = parser.parse_args()
    logging.basicConfig(filename=args.logfile, filemode="w", level=args.loglevel.upper())
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info(f"Loglevel set to {args.loglevel.upper()}.")
    logging.info(f"Log file set to {args.logfile}.")

    apples.init()

    apples.setup()

    while True:
        try:
            apples.loop()
        except apples.ApplesExit as exit_exception:
            apples.cleanup()
            exit(exit_exception.code)
