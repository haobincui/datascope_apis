import logging
import multiprocessing
import threading
import time
from functools import singledispatch, singledispatchmethod
from typing import Callable, NoReturn, Tuple, List, Union


class MultiThreads:
    def __init__(self, funcs: Union[List[Callable], Callable], nums_of_thread: int = None):
        self.nums_of_thread = nums_of_thread if nums_of_thread else self.get_nums_of_cpu()
        if isinstance(funcs, list):
            self.funcs = funcs
        elif isinstance(funcs, Callable):
            self.funcs = [funcs] * self.nums_of_thread
        self.threads = []

    def get_nums_of_cpu(self):
        nums = multiprocessing.cpu_count()
        if self.nums_of_thread is None:
            self.nums_of_thread = nums
        return nums

    @singledispatchmethod
    def allocate_input_to_threads(self, function_input: List[Tuple]) -> None:

        for i in range(self.nums_of_thread):
            t = threading.Thread(target=self.funcs[i], args=function_input[i])
            self.threads.append(t)

    @allocate_input_to_threads.register
    def _(self, function_input: tuple) -> None:

        for i in range(self.nums_of_thread):
            t = threading.Thread(target=self.funcs[i], args=function_input)
            self.threads.append(t)

    @allocate_input_to_threads.register
    def _(self, function_input: float) -> None:
        for i in range(self.nums_of_thread):
            t = threading.Thread(target=self.funcs[i], args=(function_input,))
            self.threads.append(t)

    def start_calc(self) -> NoReturn:
        # res = []
        for i in self.threads:
            # try:
            i.start()  # start sending
            # except Exception as e:
            #     logging.info(f'Multi thread Error, message: [{e}]')
            #     continue

        for i in self.threads:
            i.join()  # wait for all thread finish
