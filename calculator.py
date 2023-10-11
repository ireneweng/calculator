import logging

from sympy import sympify

LOG = logging.getLogger(__name__)


class Calculator(object):
    def __init__(self):
        """Class to calculate arithmetic string inputs."""
        pass

    def run(self, input):
        success = False
        try:
            result = float(sympify(input))
            result = f"{result:.10f}"
            success = True
        except Exception as e:
            result = f"Error: {e}".strip()
        return result, success
