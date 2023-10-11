import logging

from sympy import sympify

LOG = logging.getLogger(__name__)


class Calculator(object):
    def __init__(self):
        """Class to calculate arithmetic string inputs."""
        pass

    def run(self, input: str) -> None:
        LOG.info(f"Input: {input}")
        try:
            result = float(sympify(input))
            result = f"{result:.8f}"
            LOG.info(f"Output: {result}")
        except Exception as e:
            e = str(e).replace("\n", " ")
            result = f"Error: {e}"
            LOG.error(e)
        return result
