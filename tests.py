import unittest

from sympy import sympify

from calculator import Calculator


class CalculatorTest(unittest.TestCase):
    """Class to check calculator implementation against library."""

    def __init__(self):
        super(CalculatorTest, self).__init__()
        self.tests = [
            "4/3",
            "4/-3",
            "-4/-3",
            "-4--5+3*9",
            "-4*((-5+3)/7)",
            "7/25-9/15",
            "7/(25-9)/15",
            "7/25/9+(-5/15)",
            "(((6 + ((4 + 2) * 9) + (8 + 1)) - 2) / 4)",
            "2+4-3+(4-5)*3/6-(3-54)",
            "2+4-3*3/6-(3-54*45)",
            "7-9*(4+5+7) / 4-(-5)",
            "(7-9*7+8) / (3+4-(-1431)) / (-4--56)",
        ]

    def run(self) -> None:
        calculator = Calculator()
        for test in self.tests:
            my_solution = calculator.evaluate_expression(test)
            library_check = float(sympify(test))
            self.assertAlmostEqual(my_solution, library_check, places=10)
        print("Woohoo! Everything passed.")


def main():
    tester = CalculatorTest()
    tester.run()


if __name__ == "__main__":
    main()
