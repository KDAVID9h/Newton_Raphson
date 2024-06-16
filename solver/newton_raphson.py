import numpy as np

class NewtonRaphsonSolver:
    def __init__(self, equations, x0, tol):
        self.equations = equations
        self.x0 = np.array(x0, dtype=float)
        self.tol = tol

    def jacobian(self, f, x):
        h = 1e-8
        n = len(x)
        J = np.zeros((n, n), dtype=float)
        fx = f(x)
        for i in range(n):
            x1 = np.array(x, dtype=float)
            x1[i] += h
            J[:, i] = (f(x1) - fx) / h
        return J

    def solve(self):
        x = self.x0
        for _ in range(100):  # maximum iterations
            J = self.jacobian(self.equations, x)
            fx = self.equations(x)
            delta_x = self.gauss_seidel(J, -fx)
            x = x + delta_x
            if self.euclidean_norm(delta_x) < self.tol:
                return x, _ + 1
        raise Exception("La solution ne converge pas !")

    def gauss_seidel(self, A, b, max_iterations=100, eps=1e-10):
        n = len(b)
        x = np.zeros_like(b, dtype=float)
        for _ in range(max_iterations):
            x_new = np.copy(x)
            for i in range(n):
                s1 = np.dot(A[i, :i], x_new[:i])
                s2 = np.dot(A[i, i + 1:], x[i + 1:])
                x_new[i] = (b[i] - s1 - s2) / A[i, i]
            if np.allclose(x, x_new, atol=eps, rtol=0.):
                break
            x = x_new
        return x

    def euclidean_norm(self, v):
        return np.sqrt(np.sum(v ** 2))
