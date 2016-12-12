# brute_force.py
# Find all n below 10 ** 6 such that there are exactly ten arithmetic
# progressions (of positive integers) whereby the square of the largest
# integer minus n equals the sum of the squares of the other two integers
# Return the sum of these n


import sys, os, inspect, time, itertools, operator
from math import log

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import sieve_primes

def gen_square_set (max_num):
    return set([x ** 2 for x in range(1, max_num+1)])

def count_solutions (num, square_set):
    sol_count = 0
    if check_square(num) == 1:
        sol_count += 1
        min_bound = int((num/4) ** 0.5 + 1)
    else:
        min_bound = int((num ** 0.5)/2) + 1

    if check_square(num/3) == 1 and num % 3 == 0:
        sol_count += 1
        max_bound = int((num/3) ** 0.5 - 1)
        new_min_bound = max_bound + 2
    else:
        max_bound = int ((num ** 0.5) / (3 ** 0.5))
        new_min_bound = max_bound + 1
        

    test_sq_range = set([4 * x * x - num for x in
                         range(min_bound, max_bound + 1)])
    num_solutions = 2
    sol_count += num_solutions * len (test_sq_range.intersection (square_set))

    min_bound = new_min_bound
    max_bound = (num + 1) / 4
    
    test_sq_range = set([4 * x * x - num
                         for x in range(min_bound, max_bound + 1)])

    num_solutions = 1
    sol_count += num_solutions * len (test_sq_range.intersection (square_set))

    return sol_count

def check_square (num):
    test = int(num ** 0.5)
    if test*test == num:
        return 1
    return 0

def main():
    start_time = time.time()
    max_num = 5 * 10 ** 4
    max_square_num = max_num / 2           
    target_count = 10
    start_num = 10 **3 - 1
    condition_count = 0
    
    prime_list = sieve_primes (max_num)
    prime_set = set(prime_list)
    square_set = gen_square_set (max_square_num)
    
    i = start_num
    interval = 4 - start_num % 4
        
    while i <= max_num:
        
        i_count = count_solutions (i, square_set)
        if i_count == target_count:
            print i
            condition_count += 1
        i += interval
        interval = 4 - interval
        
    print condition_count
    print time.time() - start_time
main()
