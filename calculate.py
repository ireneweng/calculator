import argparse
import sys

from PySide6 import QtWidgets

import calculator_ui


def parse_args():
    desc = "Simple Python calculator."
    parser = argparse.ArgumentParser(
        prog="Calculator",
        description=desc,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--input", "-i", type=str, help="Calculation to solve.\n"
    )
    args = parser.parse_args()
    return args


def main():
    """
    Launch the tool.
    """
    # args = parse_args()
    # if args.input:
    #     calc = calculator_ui.Calculator(args.input)
    #     result = calc.run()
    #     return result
    # else:
    app = QtWidgets.QApplication(sys.argv)
    calc = calculator_ui.CalculatorUI()
    calc.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
