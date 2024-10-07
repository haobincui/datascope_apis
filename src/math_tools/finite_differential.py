from typing import Callable


class FiniteDifferential:

    @staticmethod
    def fd_1st_central(f: Callable[[float], float], x: float, dx: float) -> float:
        return 0.5 * (f(x + dx) - f(x - dx)) / dx

    @staticmethod
    def fd_1st_forward(f: Callable[[float], float], x: float, dx: float) -> float:
        return (f(x + dx) - f(x)) / dx

    @staticmethod
    def fd_1st_backward(f: Callable[[float], float], x: float, dx: float) -> float:
        return (f(x) - f(x - dx)) / dx

    @staticmethod
    def fd_2nd_central(f: Callable[[float], float], x: float, dx: float) -> float:
        return (f(x + dx) - 2 * f(x) + f(x - dx)) / (dx * dx)

