import argparse
import logging

import calculator_ui

LOG_FILE = "calculator_log.txt"
LOG_FORMAT = "%(filename)-18s:%(lineno)d %(levelname)s - %(message)s"


def create_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format=f"[%(asctime)s] {LOG_FORMAT}",
        datefmt="%H:%M:%S",
    )
    root_logger = logging.getLogger("")
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root_logger.addHandler(console)


def parse_args():
    desc = "Simple Python calculator."
    parser = argparse.ArgumentParser(
        prog="Calculator",
        description=desc,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--input", "-i", type=str, help="Calculation to solve.\n")
    parser.add_argument("--server", "-s", type=str, help="Flag to use server.\n")
    args = parser.parse_args()
    return args


def main():
    """
    Launch the tool.
    """
    create_logger(LOG_FILE)

    args = parse_args()
    if args.input:
        calc = calculator_ui.Calculator()
        result = calc.run(args.input)
        return result
    else:
        calculator_ui.main()


if __name__ == "__main__":
    main()
