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

    def strip_parens(self, input: str) -> str:
        return input.strip("(").strip(")")

    def get_base_expression(self, input: str) -> str:
        """Gets innermost expression inside parentheses."""
        start, end = 0, len(input)
        for i in range(len(input)):
            char = input[i]
            if char == "(":
                start = i
            elif char == ")":
                end = i + 1
                break
        return input[start:end]

    def compute_expression(self, expr_list: list[str]) -> float:
        """Recursively computes a base expression from left to right."""
        if len(expr_list) == 1:
            return float(expr_list[0])
        l_expr = expr_list[:3]
        r_expr = expr_list[3:]
        lval, rval = float(l_expr[0]), float(l_expr[2])
        op = l_expr[1]
        if op in self.operator_list:
            match op:
                case "+":
                    result = lval + rval
                case "-":
                    result = lval - rval
                case "*":
                    result = lval * rval
                case "/":
                    result = lval / rval
            return self.compute_expression([str(result)] + r_expr)

    def evaluate_expression(self, expression: str) -> float:
        """Evaluates an arithmetic equation string."""
        expression = self.strip_parens(expression)
        while any(op in expression for op in self.operator_list):
            base_expr = self.get_base_expression(expression)
            base_stripped = self.strip_parens(base_expr)
            base_list = re.split("([\-\+])", base_stripped)
            for i, val in enumerate(base_list):
                if not val:
                    neg = base_list[i + 1] + base_list[i + 2]
                    base_list[i] = neg
                    del base_list[i + 1 : i + 3]
            for i, val in enumerate(base_list):
                if "/" in val or "*" in val:
                    exp_list = re.split("([\/\*])", val)
                    result = self.compute_expression(exp_list)
                    base_list[i] = result
            result = self.compute_expression(base_list)
            expression = expression.replace(base_expr, str(result))
            LOG.debug(f"Expr: {expression}")
        return float(expression)

    def run(self, input: str) -> None:
        """Runs the calculator."""
        LOG.info(f"Input: {input}")
        try:
            result = str(self.evaluate_expression(input))
            LOG.info(f"Output [irene]: {result}")
            result = float(sympify(input))
            LOG.info(f"Output [sympy]: {result}")
        except Exception as e:
            e = str(e).replace("\n", " ")
            result = f"Error: {e}"
            LOG.error(e)
        return result


if __name__ == "__main__":
    calc = Calculator()
