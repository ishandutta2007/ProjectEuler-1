# diophantine_equation.py
# Find minimal x such that x**2 = Dy**2 + 1 for D up to 1000
# Returns the maximum x value

import time
import sys, os, inspect, time
from math import factorial

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from alg_rational_class import *


from decimal import *

def check_if_square (num):
    test = num ** 0.5
    if int(test) ** 2 == num:
        return 1
    return 0

# This returns that minimum x satisfying the above equation for integers
# We generate the CFE for sqrt(D) until a pair satisfies this equation

def find_min_x (D):
    getcontext().prec = 100
    if check_if_square (D + 1) == 1:
        return (D+1) ** 0.5

    test_x, test_y = int (D ** 0.5), 1
    
    if (test_x ** 2 == D * test_y ** 2 + 1):
        return test_x
    
    conv = test_x
    remainder = Decimal((D ** 0.5)) - Decimal(test_x) / Decimal(test_y)
    next_index = int (Decimal(1.0) / Decimal(remainder))

    
    prev_x, prev_y = test_x, test_y
    test_x, test_y = (next_index) * prev_x + 1, next_index
    if (test_x ** 2 == D * test_y ** 2 + 1):
        return test_x
    conv = test_x / (test_y + 0.0)
    
    while (1):
        remainder = Decimal(1.0) / Decimal(remainder) - Decimal(next_index)
        next_index = int (Decimal(1.0) / Decimal(remainder))
        print remainder, next_index
        
        new_test_x, new_test_y = (next_index) * test_x + prev_x, next_index * test_y + prev_y
        prev_x, prev_y = test_x, test_y
        test_x, test_y = new_test_x, new_test_y
        print test_x, test_y, next_index, remainder
        if (test_x ** 2 == D * test_y ** 2 + 1):
            return test_x
        if test_x > 3 * 10 ** 9:
            break
                    
def main():
    start_time = time.time()
    max_num = 61
    max_x = 0
    for D in range (61, max_num + 1):
        if check_if_square (D) == 1:
            continue
        max_d = find_min_x (D)
        max_x = max (max_x, max_d)
        print D, max_d
    print max_x
    print time.time() - start_time
    
main()
    
