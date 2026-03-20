from typing import Callable


class FiniteDifferential:
    """Utility class for finite-difference derivative approximations."""

    @staticmethod
    def fd_1st_central(f: Callable[[float], float], x: float, dx: float) -> float:
        """Fd 1st central.

        Args:
            f (Callable[[float], float]): Function to evaluate in the finite-difference formula.
            x (float): Point where the derivative approximation is evaluated.
            dx (float): Step size used by the finite-difference approximation.

        Returns:
            float: Computed result of the operation.
        """
        return 0.5 * (f(x + dx) - f(x - dx)) / dx

    @staticmethod
    def fd_1st_forward(f: Callable[[float], float], x: float, dx: float) -> float:
        """Fd 1st forward.

        Args:
            f (Callable[[float], float]): Function to evaluate in the finite-difference formula.
            x (float): Point where the derivative approximation is evaluated.
            dx (float): Step size used by the finite-difference approximation.

        Returns:
            float: Computed result of the operation.
        """
        return (f(x + dx) - f(x)) / dx

    @staticmethod
    def fd_1st_backward(f: Callable[[float], float], x: float, dx: float) -> float:
        """Fd 1st backward.

        Args:
            f (Callable[[float], float]): Function to evaluate in the finite-difference formula.
            x (float): Point where the derivative approximation is evaluated.
            dx (float): Step size used by the finite-difference approximation.

        Returns:
            float: Computed result of the operation.
        """
        return (f(x) - f(x - dx)) / dx

    @staticmethod
    def fd_2nd_central(f: Callable[[float], float], x: float, dx: float) -> float:
        """Fd 2nd central.

        Args:
            f (Callable[[float], float]): Function to evaluate in the finite-difference formula.
            x (float): Point where the derivative approximation is evaluated.
            dx (float): Step size used by the finite-difference approximation.

        Returns:
            float: Computed result of the operation.
        """
        return (f(x + dx) - 2 * f(x) + f(x - dx)) / (dx * dx)
