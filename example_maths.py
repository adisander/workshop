import math
import sympy

from libs.log import *


def compare_outputs():
    standard = math.sqrt(8)
    readable = sympy.sqrt(8)
    info(f"The standard library's square root output: {standard}")
    info(f"Sympy's square root output: {readable}")


def symbolic_computing():
    x, y = sympy.symbols('x y')

    expression = x + 2*y
    info(f"Printing the expression keeps its form: {expression}")
    info(f"From there you can do some general maths: {expression} - x -> {expression - x}")
    info(f"Or multiplication: {expression} * x -> {expression * x}")

    expanded = sympy.expand(expression * x)
    info(f"Which we can then expand if desired: {expanded}")
    info(f"Or factor again: {sympy.factor(expanded)}")

    expression = sympy.sin(2*x)
    info(f"Or we can start differentiating: {expression} -> {sympy.diff(expression)}")
    info(f"Integrating too: {expression} by x from 0 to pi/2 -> {sympy.integrate(expression, (x, 0, sympy.pi/2))}")

    expression = sympy.sin(x) / x
    info(f"Finding limits: {expression} by x towards 0 -> {sympy.limit(expression, x, 0)}")
    info(f"Or outright solving: {expression} = 0 -> x = {sympy.solve(expression, x)}")
    

if __name__ == '__main__':
    compare_outputs()
    symbolic_computing()
