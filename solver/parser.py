from sympy import sympify, lambdify
import numpy as np

class EquationParser:
    @staticmethod
    def parse(equations_str):
        equations = [sympify(eq) for eq in equations_str]
        variables = list(equations[0].free_symbols)
        f = lambdify(variables, equations, modules='numpy')
        def equations_func(x):
            return np.array(f(*x), dtype=float)
        return equations_func
