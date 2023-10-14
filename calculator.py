# built-in imports
import logging
import re

# third party imports
from sympy import sympify

LOG = logging.getLogger(__name__)


class Calculator(object):
    """Class to calculate arithmetic string inputs."""

    def __init__(self):
        self.operator_list = ["+", "-", "*", "/"]

    def strip_parens(self, input: str) -> str:
        """Strips the outer parentheses of the given input."""
        return input.strip("(").strip(")")

    def expr_is_float(self, input: str) -> bool:
        """
        Checks if given input string is a float.
        Used as the break condition for evaluate_expression(),
        mainly to handle the case of negative numbers in parentheses.
        """
        try:
            float(input)
            return True
        except ValueError:
            return False

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
        Assumes empty string item exists between operator and negative sign.
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
        Recursively solves the multiplication/division parts of an expression.
        Returns the expression list with only addition/subtraction left.
        Ex. input "7/-4-3*-2" as list:
                -> ['7', '/', '-4', '-', '3', '*', '-2']
                -> [-1.75, '-', -6.0]
        """
        for i, val in enumerate(expr_list):
            if val in ["*", "/"]:
                l_idx = i - 1
                r_idx = i + 2
                sol = self.compute_expression(expr_list[l_idx:r_idx])
                expr_list = expr_list[:l_idx] + [sol] + expr_list[r_idx:]
                break
        while "*" in expr_list or "/" in expr_list:
            LOG.debug(f"Resolved mul/div: {expr_list}")
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

        op = expr_list[1]
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
        """
        Evaluates an arithmetic equation string.
        Assumes equation is provided in a valid format, i.e.
        no unmatched/empty parentheses or hanging operators.
        """
        expression = self.strip_parens(expression)
        while any(op in expression for op in self.operator_list):
            base_expr = self.get_base_expression(expression)
            base_stripped = self.strip_parens(base_expr)
            base_list = re.split("([\/\*\-\+])", base_stripped)
            base_list = self.resolve_negatives(base_list)
            base_list = self.resolve_mul_div(base_list)
            result = self.compute_expression(base_list)
            expression = expression.replace(base_expr, str(result))
            if self.expr_is_float(expression):
                break
        return result

    def run(self, input: str) -> None:
        """Runs the calculator."""
        LOG.info(f"Input: {input}")
        try:
            result = str(self.evaluate_expression(input))
            LOG.info(f"Output [irene]: {result}")
            # check solution against library
            # result = str(float(sympify(input)))
            # LOG.info(f"Output [sympy]: {result}")
        except Exception as e:
            e = str(e).replace("\n", " ")
            result = f"Error: {e}"
            LOG.error(e)
        return result


if __name__ == "__main__":
    calc = Calculator()
