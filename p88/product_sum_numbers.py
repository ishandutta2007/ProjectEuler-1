# product_sum_numbers.py
# For each number k, find the smallest set of size k such that the
# sum of the numbers equals its product
# Small is determined by the sum calculated this way
from copy import copy
from math import log

import sys, os, inspect, time


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve

# Recursive function that determines all the possible products that can be expressed
# as sums of length k, where sum and product come out equal
# Algo boils down to finding 
def locate_valid_sets (k, n, set_list, prod_list, min_test = 0):

    if min_test == 0:
        thresh_test = k
    else:
        thresh_test = min_test
        
    # Base cases
    if prod_list >= thresh_test:
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
        final_prod = locate_valid_sets (k, n, test_list, running_list, thresh_test) 
        if final_prod != 0:
            if min_prod == 0:
                min_prod = final_prod
            else:
                min_prod = min(final_prod, min_prod)
                thresh_test = min_prod / 2.0  # for remaining checks

    return int(min_prod)

def calc_prime_factorization (sieve_list, max_num):

    prime_factor_dict = {}
    for i in xrange(2, max_num+1):
        prime_factor_dict[i] = []
        if sieve_list[i] == 0:
            prime_factor_dict[i].append((i,1))  # prime number
        else:
            factor_list = sieve_list[i][1]
            for factor in factor_list:
                j = 1
                while i % (factor ** j) == 0:
                    j += 1
                prime_factor_dict[i].append ((factor, j-1))
    return prime_factor_dict

# Looking at simple prime factorizations, this calculates potential values for products equalling
# sums of some length k. Some k's will not be represented in these calculations
# We want to use these as min thresholds, when possible, to expedite the actual search for the minimum
def potential_N_values (prime_factor_dict, max_num):
    potential_min_dict = {}
    for i in xrange(2, max_num+1):
        if len (prime_factor_dict[i]) == 1 and prime_factor_dict[i][0][1] == 1: # prime
            continue
        sum_factors = 0
        num_factors = 0
        for factor_tuple in prime_factor_dict[i]:
            sum_factors += (factor_tuple[0] * factor_tuple[1])
            num_factors += factor_tuple[1]
        if i >= sum_factors:
            # Must add (i - sum_factors) 1's so that the sum equals the product i
            num_terms = (i - sum_factors) + num_factors
            if num_terms not in potential_min_dict:
                potential_min_dict[num_terms] = i
            else:
                potential_min_dict[num_terms] = min (i, potential_min_dict[num_terms])
    return potential_min_dict

def generate_all_factor_partitions (all_min_dict, N, factor_list, master_list = []):
    import operator
    
    # Base case
    if len (factor_list) == 0:
        new_list = []
        for mini_list in master_list:
            if len(mini_list) > 0:
                new_list.append (reduce(operator.mul, mini_list))
        k = N - sum (new_list) + len (new_list)
        if k in all_min_dict:
            all_min_dict[k] = min(N, all_min_dict[k])
        else:
            all_min_dict[k] = N
        return all_min_dict

    test_list = copy (factor_list)
    if len (master_list) == 0:
        if len(factor_list) == 1: # prime number
            return all_min_dict
        curr_list = []
        curr_list.append (test_list[0])
        del test_list[0]
        master_list.append (curr_list)
        master_list.append ([])

    # There are two options for each factor in the list from here on:
    # Either add to one of the lists in master_list, or make a new one

    for i in xrange(len(master_list)):
        test_master = copy (master_list)
        test_master[i].append (test_list[0])
        if len(test_master[-1]) > 0: # always ensure there's an empty list at the end
            test_master.append([])
        all_min_dict = generate_all_factor_partitions (all_min_dict, N, test_list[1:], test_master)
    return all_min_dict
            

# Determined all products that can equal N and determines their corresponding k value
# Doing this for all N will yield the minimum N for all k
def all_N_values (prime_factor_dict, max_num):
    all_min_dict = {}
    for N in xrange(2, max_num+1):
        if len (prime_factor_dict[N]) == 1 and prime_factor_dict[N][0][1] == 1: # prime
            continue
        factor_list = []
        for factor in prime_factor_dict[N]:
            mini_list = [factor[0]] * factor[1]
            factor_list += mini_list
        
def calc_min_num_factors (test_num, min_N):
    i = 2
    while True:
        factor = int(test_num ** (1.0/i))
        if factor == 1:
            break
        sum_factor = i * factor
        total_N = (test_num - i) + sum_factor
        if total_N < min_N:
            return i
        i += 1
    return i

def main():
    start_time = time.time()
    N_list = []
    max_num = 1000

    prime_list, sieve_list = gen_co_prime_sieve (max_num)
    prime_factor_dict = calc_prime_factorization (sieve_list, max_num)

    potential_min_dict = potential_N_values (prime_factor_dict, max_num)
    print time.time() - start_time
    for test_num in xrange(2,max_num+1):
        min_num_factors = 2
        min_N = 2 * test_num
        if test_num in potential_min_dict:
            min_N = potential_min_dict[test_num]
            min_num_factors = calc_min_num_factors (test_num, min_N)            
            
        for num_factors in xrange(min_num_factors, int(log(test_num) / log(2)) + 2):
            test_N =  locate_valid_sets (test_num, num_factors, [], 1, min_N / 2.0)
            if test_N > 0:
                min_N = min(min_N, test_N)
        N_list.append (min_N)
        if test_num % 1000 == 0:
            print test_num, min_N, time.time() - start_time
            
    print sum(set(N_list))
    
    print time.time() - start_time

main()
