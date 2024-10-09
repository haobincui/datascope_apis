
a = 1
def add(a, b):
    return a + b
try:
    print(add(a, b))
except Exception as e:
    raise ValueError('error in add function')

