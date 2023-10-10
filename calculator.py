from sympy import sympify, Float


class Calculator(object):
    def __init__(self, input_string):
        """Class to calculate arithmetic string inputs."""
        self.input = input_string

    def run(self):
        result = float(sympify(self.input))
        return result
