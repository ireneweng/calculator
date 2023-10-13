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

    def resolve_negatives(self, expr_list: list[str]) -> list[str]:
        """
        Resolves negative numbers in expression list.
        Ex. input "7/-4-3*-2" as list:
                -> ['7', '/', '', '-', '4', '-', '3', '*', '', '-', '2']
                -> ['7', '/', '-4', '-', '3', '*', '-2']
        """
        for i, val in enumerate(expr_list):
            if not val:
                neg = expr_list[i + 1] + expr_list[i + 2]
                expr_list[i] = neg
                del expr_list[i + 1 : i + 3]
        LOG.debug(f"Resolved negatives: {expr_list}")
        return expr_list

    def resolve_mul_div(self, expr_list: list[str]) -> list[str]:
        """
        Recursively solves the multiplication/division parts of an equation.
        Returns the expression list with only addition/subtraction left.
        Ex. input "7/-4-3*-2" as list:
                -> ['7', '/', '-4', '-', '3', '*', '-2']
                -> [-1.75, '-', -6.0]
        """
        for i, val in enumerate(expr_list):
            if val in ["*", "/"]:
                sol = self.compute_expression(expr_list[i - 1 : i + 2])
                expr_list = expr_list[: i - 1] + [sol] + expr_list[i + 2 :]
                break
        while "*" in expr_list or "/" in expr_list:
            LOG.debug(f"Resolving mul/div: {expr_list}")
            expr_list = self.resolve_mul_div(expr_list)
        return expr_list

    def compute_expression(self, expr_list: list[str]) -> float:
        """
        Recursively computes an expression from left to right.
        NOTE: Does not follow order of operations; use resolve_mul_div() first.
        Ex. input "7/-4-3":
                -> ['7', '/', '-4', '-', '3']
                -> -4.75
        Ex. input "7/-4-3*-2" ignores PEMDAS:
                -> ['7', '/', '-4', '-', '3', '*', '-2']
                -> 9.5
        """
        if len(expr_list) == 1:
            return float(expr_list[0])
        l_expr = expr_list[:3]
        r_expr = expr_list[3:]
        lval, rval = float(l_expr[0]), float(l_expr[2])
        op = l_expr[1]
        if op in self.operator_list:
            LOG.debug(f"Sub-equation: {expr_list}")
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
            base_list = re.split("([\/\*\-\+])", base_stripped)
            base_list = self.resolve_negatives(base_list)
            base_list = self.resolve_mul_div(base_list)
            result = self.compute_expression(base_list)
            expression = expression.replace(base_expr, str(result))
            if len(base_list) == 1:
                break
        return result

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
