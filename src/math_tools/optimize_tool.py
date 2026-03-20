import logging

import numpy as np
from scipy import optimize


def optimize_tool(target_func, initial_guess, bounds, max_iter=20, eps = 1e-12):
    """Optimize tool.

    Args:
        target_func (object): Input value for target func.
        initial_guess (object): Input value for initial guess.
        bounds (object): Input value for bounds.
        max_iter (object): Input value for max iter.
        eps (object): Input value for eps.

    Returns:
        object: Computed result of the operation.
    """
    status = False
    i = 0
    logging.info(f'Start Optimize')
    res = None
    while i + 1 <= max_iter and status is False:
        res = optimize.minimize(target_func, initial_guess, bounds=bounds, tol=eps)
        # k, theta, sigma, x_t, r_t = res.x
        cost = res.fun
        status = res.success
        logging.info(f'Finished iter [{i}], status [{status}], with cost [{cost}]')
        i += 1
        logging.debug(f'finished {i - 1}')
        rand_num = np.random.normal() * 0.001
        initial_guess = np.array([ele + rand_num for ele in res.x])
    logging.debug(f'Finished all iters, total iter times [{i}], final status [{status}] with cost [{cost}]')
    logging.debug(f'Optimized value: [{res.x}]')
    if res is None:
        raise ValueError('Failed to optimized')
    return res
