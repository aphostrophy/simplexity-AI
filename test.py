import multiprocessing
import random

a = multiprocessing.Value('i', random.randint(0, 2))
print(a)