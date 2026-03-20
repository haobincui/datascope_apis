import numpy as np


def squared_error(x, y, weights=None):
    """Squared error.

    Args:
        x (object): Point where the derivative approximation is evaluated.
        y (object): Input value for y.
        weights (object): Input value for weights.

    Returns:
        object: Computed result of the operation.
    """
    if weights is None:
        return np.power(np.subtract(x, y), 2).sum()
    return (np.power(np.subtract(x, y), 2) * weights).sum()


def root_squared_error(x, y, weights=None):
    """Root squared error.

    Args:
        x (object): Point where the derivative approximation is evaluated.
        y (object): Input value for y.
        weights (object): Input value for weights.

    Returns:
        object: Computed result of the operation.
    """
    if weights is None:
        return np.sqrt(np.power(np.subtract(x, y), 2).sum())
    return np.sqrt(np.power(np.subtract(x, y), 2) * weights).sum()
