# product_sum_numbers.py
# For each number k, find the smallest set of size k such that the
# sum of the numbers equals its product
# Small is determined by the sum calculated this way
from copy import copy
from math import log
import time

def locate_valid_sets (k, n, set_list, prod_list):

    # Base cases
    if prod_list >= k:
        return 0
    
    if len (set_list) == (n - 1):
        factor_one = ((k - n + sum (set_list)) /
                      (prod_list - 1.0))
        if int(factor_one) == factor_one and factor_one > 0:
            return factor_one * prod_list
        return 0

    # Setup the recurring algo
    if len(set_list) == 0:
        max_num = k ** (1.0/ (n - 1))
        max_num = int(max_num)
        min_num = 2
        prod_list = 1
    else:
        rem_nums = (n - 1 - len(set_list))
        max_num = (k / (prod_list + 0.0)) ** (1.0 / rem_nums)
        max_num = int (max_num)
        min_num = set_list[-1]
        
    min_prod = 0

    for num in xrange (min_num, max_num+1):
        test_list = copy (set_list)
        test_list.append (num)
        running_list = prod_list
        running_list *= num
        final_prod = locate_valid_sets (k, n, test_list, running_list) 
        if final_prod != 0:
            if min_prod == 0:
                min_prod = final_prod
            else:
                min_prod = min(final_prod, min_prod)

    return int(min_prod)

def main():
    start_time = time.time()
    N_list = []
    max_num = 846
    for test_num in xrange(2,max_num+1):
        min_N = 2 * test_num
        for num_factors in xrange(2, int(log(test_num) / log(2)) + 2):
            test_N =  locate_valid_sets (test_num, num_factors, [], 1)
            if test_N > 0:
                min_N = min(min_N, test_N)
        N_list.append (min_N)
        print test_num, min_N
    print sum(set(N_list))
    
    print time.time() - start_time
main()
