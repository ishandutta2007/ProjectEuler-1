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

def check_if_square (num):
    test = num ** 0.5
    if int(test) ** 2 == num:
        return 1
    return 0

# This returns that minimum x satisfying the above equation for integers
# We generate the CFE for sqrt(D) until a pair satisfies this equation

def find_min_x (D):

    if check_if_square (D + 1) == 1:
        return (D+1) ** 0.5

    test_x, test_y = int (D ** 0.5), 1
    
    if (test_x ** 2 == D * test_y ** 2 + 1):
        return test_x
    
    conv = test_x
    remainder = Alg_Rational_add (Algebraic_Rational(0,1,1,D),
                                  Algebraic_Rational(-1*test_x, 0, test_y, 0))
    next_index = int((Alg_Rational_invert (remainder)).val)
    
    prev_x, prev_y = test_x, test_y
    test_x, test_y = (next_index) * prev_x + 1, next_index
    if (test_x ** 2 == D * test_y ** 2 + 1):
        return test_x
    conv = test_x / (test_y + 0.0)
    
    while (1):
        remainder = Alg_Rational_add (Alg_Rational_invert (remainder),
                                      Algebraic_Rational(-1*next_index,0,1,D))
        next_index = int((Alg_Rational_invert (remainder)).val)
        
        new_test_x, new_test_y = (next_index) * test_x + prev_x, next_index * test_y + prev_y
        prev_x, prev_y = test_x, test_y
        test_x, test_y = new_test_x, new_test_y

        if (test_x ** 2 == D * test_y ** 2 + 1):
            return test_x

                    
def main():
    start_time = time.time()
    max_num = 1000
    max_x = 0
    for D in range (61, max_num + 1):
        if check_if_square (D) == 1:
            continue
        d_val = find_min_x (D)
        if d_val > max_x:
            print D, d_val
            max_x = max (max_x, d_val)
            max_d = D
    
    print max_d, max_x
    print time.time() - start_time
    
main()
    
