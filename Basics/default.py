'''
This file shows examples from some in-built python modules
'''

import math
from collections import deque

'''
'''
# Use math module for some in-built mathematical calculation methods
def calculate_square_root(n):
    if n < 0:
        raise ValueError("Cannot compute square root of negative number")
    return math.sqrt(n)
# print(calculate_square_root(25))

def calculate_factorial(n):
    return math.factorial(n)
# print(calculate_factorial(5))

'''
Use collections module for some interesting data structures available already there
'''
def show_queue():
    queue = deque()
    queue.append("task1")
    queue.append("task2")
    queue.append("task3")

    queue.appendleft("urgent_task")
    queue.appendleft("urgent_task1")
    # queue.pop()
    # queue.popleft()

    print(queue)
show_queue()

