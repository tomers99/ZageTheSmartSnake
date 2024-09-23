# import random
# import time
#
# data = []
#
# for digits1 in range(1,101):
#     for digits2 in range(1,101):
#         avg_time = 0
#         for itr in range (0,100):
#
#             num1 = random.randint(10 ** (digits1 - 1), 10 ** (digits1) - 1)
#             num2 = random.randint(10 ** (digits2 - 1), 10 ** (digits2) - 1)
#
#             ptime0 = time.perf_counter()
#             sum = num1 + num2
#             avg_time += time.perf_counter() - ptime0
#
#         avg_time = avg_time/100
#         data.append(((digits1, digits2), avg_time))
#
# print (data)
#
#
#
# def time_counter(my_function, parameters):
#     ptime0 = time.perf_counter()
#     my_function(parameters)
#     total_time = time.perf_counter() - ptime0
#     return total_time

import random
x = random.randint(1,1000001)

def f(x):
    if x % 2 == 0:
        x /= 2
        print(x)
        f(x)
    elif x != 1:
        x = 3*x + 1
        print(x)
        f(x)
    else:
        print(f"We have finished, x is {x}")

f(x)