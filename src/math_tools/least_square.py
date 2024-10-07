import numpy as np


def squared_error(x, y, weights=None):
    if weights is None:
        return np.power(np.subtract(x, y), 2).sum()
    return (np.power(np.subtract(x, y), 2) * weights).sum()


def root_squared_error(x, y, weights=None):
    if weights is None:
        return np.sqrt(np.power(np.subtract(x, y), 2).sum())
    return np.sqrt(np.power(np.subtract(x, y), 2) * weights).sum()
