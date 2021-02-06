import argparse
import logging

try:
    from .. import apples
except (ImportError, ValueError):
    import apples

if __name__ == "__main__":
    # Totally cribbed from https://stackoverflow.com/questions/57192387/how-to-set-logging-level-from-command-line
    parser = argparse.ArgumentParser()
    parser.add_argument("-log",
                        "--loglevel",
                        default="warning",
                        help="Provide logging level. Example --loglevel debug, default=warning")

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    logging.info(f"Loglevel set to {args.loglevel.upper()}.")

    apples.init()

    apples.setup()

    while True:
        try:
            apples.loop()
        except apples.ApplesExit as exit_exception:
            apples.cleanup()
            exit(exit_exception.code)
