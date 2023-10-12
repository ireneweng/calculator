# built-in imports
import logging
import re

# third party imports
from sympy import sympify

LOG = logging.getLogger(__name__)


class Calculator(object):
    def __init__(self):
        """Class to calculate arithmetic string inputs."""
        self.operator_list = ["+", "-", "*", "/"]
        # print(self.evaluate_expression("(((6+ ((4 + 2) * 9)+(8 + 1)) - 2) / 4)"))
        # print(self.evaluate_expression("(3+2)/0"))

    def get_base_expression(self, input):
        start = 0
        end = len(input)
        for i, char in enumerate(input):
            if char == "(":
                start = i
            elif char == ")":
                end = i + 1
                break
        return input[start:end]

    def compute_expression(self, expr_list):
        if len(expr_list) == 1:
            return float(expr_list[0])
        l_expr = expr_list[:3]
        lval, rval = float(l_expr[0]), float(l_expr[2])
        op = l_expr[1]
        if op in self.operator_list:
            match expr_list[1]:
                case "+":
                    result = lval + rval
                case "-":
                    result = lval - rval
                case "*":
                    result = lval * rval
                case "/":
                    result = lval / rval
            return self.compute_expression([str(result)] + expr_list[3:])

    def evaluate_expression(self, expr):
        while any(op in expr for op in self.operator_list):
            base_expr = self.get_base_expression(expr)
            base_stripped = base_expr.strip("(").strip(")")
            base_list = re.split("([\/\*\-\+])", base_stripped)
            result = self.compute_expression(base_list)
            expr = expr.replace(base_expr, str(result))
        return float(expr)

    def run(self, input: str) -> None:
        LOG.info(f"Input: {input}")
        try:
            result = float(sympify(input))
            result = f"{result:.8f}"
            LOG.info(f"Output via sympy: {result}")

            result = str(self.evaluate_expression(input))
            LOG.info(f"Output via built-in: {result}")
        except Exception as e:
            e = str(e).replace("\n", " ")
            result = f"Error: {e}"
            LOG.error(e)
        return result


if __name__ == "__main__":
    calc = Calculator()
