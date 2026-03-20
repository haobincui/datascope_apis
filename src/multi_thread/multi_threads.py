import logging
import multiprocessing
import threading
import time
from functools import singledispatch, singledispatchmethod
from typing import Callable, NoReturn, Tuple, List, Union


class MultiThreads:
    """Lightweight thread launcher for running repeated callables in parallel."""

    def __init__(self, funcs: Union[List[Callable], Callable], nums_of_thread: int = None):
        """Initialize worker callables and thread capacity.

        Args:
            funcs (Union[List[Callable], Callable]): Callable or callable list executed by worker threads.
            nums_of_thread (int): Number of worker threads to allocate. Defaults to CPU count.

        Returns:
            None: No value is returned.
        """
        self.nums_of_thread = nums_of_thread if nums_of_thread else self.get_nums_of_cpu()
        if isinstance(funcs, list):
            self.funcs = funcs
        elif isinstance(funcs, Callable):
            self.funcs = [funcs] * self.nums_of_thread
        self.threads = []

    def get_nums_of_cpu(self):
        """Return the local CPU core count.

        Returns:
            int: Number of CPU cores reported by the runtime.
        """
        nums = multiprocessing.cpu_count()
        if self.nums_of_thread is None:
            self.nums_of_thread = nums
        return nums

    @singledispatchmethod
    def allocate_input_to_threads(self, function_input: List[Tuple]) -> None:
        """Allocate tuple inputs per thread using positional mapping.

        Args:
            function_input (List[Tuple]): Per-thread argument tuples in thread index order.

        Returns:
            None: No value is returned.
        """
        for i in range(self.nums_of_thread):
            t = threading.Thread(target=self.funcs[i], args=function_input[i])
            self.threads.append(t)

    @allocate_input_to_threads.register
    def _(self, function_input: tuple) -> None:
        """Allocate the same tuple input to each worker thread.

        Args:
            function_input (tuple): Input payload forwarded to worker threads.

        Returns:
            None: No value is returned.
        """
        for i in range(self.nums_of_thread):
            t = threading.Thread(target=self.funcs[i], args=function_input)
            self.threads.append(t)

    @allocate_input_to_threads.register
    def _(self, function_input: float) -> None:
        """Allocate the same scalar float input to each worker thread.

        Args:
            function_input (float): Input payload forwarded to worker threads.

        Returns:
            None: No value is returned.
        """
        for i in range(self.nums_of_thread):
            t = threading.Thread(target=self.funcs[i], args=(function_input,))
            self.threads.append(t)

    def start_calc(self) -> NoReturn:
        """Start all configured threads and block until completion.

        Returns:
            NoReturn: This method returns only when all threads have joined.
        """
        # res = []
        for i in self.threads:
            # try:
            i.start()  # start sending
            # except Exception as e:
            #     logging.info(f'Multi thread Error, message: [{e}]')
            #     continue

        for i in self.threads:
            i.join()  # wait for all thread finish
