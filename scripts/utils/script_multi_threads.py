import threading
import time

from src.multi_thread import MultiThreads

res = []


def f(x, y):
    time.sleep(1)
    tem_res = x + y
    res.append(tem_res)
    print(threading.current_thread().name, time.ctime())


def f_2(x, y, z):
    time.sleep(1)

    def _f_1():
        return x + y

    def _f_2(a):
        return x + y + a

    def _f_3(b):
        return z + b

    r_1 = _f_1()
    r_2 = _f_2(r_1)
    r_3 = _f_3(r_2)
    print(threading.current_thread().name, time.ctime())
    res.append(r_3)


# a = f

num_of_thread = 4
# threads = MultiThreads(func=a, nums_of_thread=num_of_thread)
f_input = (2, 3)

f_2_input = (1, 2, 3,)
# f = f_2

# threads.allocate_function_to_threads(function_input=f_input)
threads = MultiThreads(func=f_2, nums_of_thread=num_of_thread)
threads.allocate_input_to_threads(function_input=f_2_input)

threads.start_calc()
print(res)
