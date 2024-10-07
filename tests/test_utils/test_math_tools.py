import unittest

from src.math_tools.finite_differential import FiniteDifferential


class TestFiniteDifferential(unittest.TestCase):

    def test_finite_differential_1nd(self):
        def f(x):
            return 2 * x

        dx = 0.00001
        x = 1
        target_result = 2
        eps = 1e-9

        calculator = FiniteDifferential()
        central_result = calculator.fd_1st_central(f, x, dx)
        forward_result = calculator.fd_1st_forward(f, x, dx)
        backward_result = calculator.fd_1st_backward(f, x, dx)

        self.assertAlmostEqual(central_result, target_result, delta=eps)
        self.assertAlmostEqual(forward_result, target_result, delta=eps)
        self.assertAlmostEqual(backward_result, target_result, delta=eps)

    def test_finite_differential_2nd(self):
        def f(x):
            return x * x

        dx = 0.0001
        x = 1
        target_result = 2
        eps = 2e-9

        calculator = FiniteDifferential()
        central_result = calculator.fd_2nd_central(f, x, dx)

        self.assertAlmostEqual(central_result, target_result, delta=eps)


