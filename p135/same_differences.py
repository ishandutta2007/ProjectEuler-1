# same_differences.py
# Find all n below 10 ** 6 such that there are exactly ten arithmetic
# progressions (of positive integers) whereby the square of the largest
# integer minus n equals the sum of the squares of the other two integers
# Return the sum of these n


import sys, os, inspect, time, itertools, operator
from math import log
from bisect import bisect_right

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve

# Determine the max exponent of p that divides x1
# known is the least known exponent that satisfies
def max_exponent_prime_factor (x1, p, known):

    n = 0
    exp = known + 2 ** n
    while x1 % (p ** exp) == 0:
        n += 1
        exp = known + 2 ** n

    if n == 0:
        return known
    if n == 1:
        return (known + 1)
    
    return max_exponent_prime_factor (x1, p, known + 2 ** (n-1))

# If 2 is not a prime factor, this calculates the number of divisors of num
# Otherwise, it counts the factors where 2 has a positive but not maximal
# exponent
def calc_num_factors (num, num_list, prime_set):
    if num in prime_set:
        return 2, [1]

    factor_list = num_list[num][1]

    factor_exp_list = []
    num_factors_prod = 1
    for factor in factor_list:
        factor_exp = (max_exponent_prime_factor(num, factor, 1))
        factor_exp_list.append (factor_exp)
        if factor != 2:
            num_factors_prod *= (factor_exp + 1)
        else:
            if factor_exp == 1 or factor_exp == 3:
                num_factors_prod = 0
            elif factor_exp == 2:
                num_factors_prod *= 1
            else:
                rel_factors = 0

                for test_exp in range (2, factor_exp-1):
                    if num / (2 ** test_exp) >= (1 + 2 ** (test_exp - 2)):
                        rel_factors += 1
                        
                num_factors_prod *= (rel_factors)
            
    return num_factors_prod, factor_exp_list

#------------------------------------------------------------------------------
# Looking for more than one progression with the same difference
def count_num_solutions (num, num_factors, factor_list, factor_exp_list,
                         target_count):



    all_factor_list = sorted(generate_all_factors(num, factor_list,
                                               factor_exp_list))
    all_factor_set = set(all_factor_list)
    init_count = bisect_right (all_factor_list, num ** 0.5)


    # differences in this range will yield 2 solutions
    min_diff = (num ** 0.5)/2

    max_diff = (num ** 0.5) / (3 ** 0.5)
        
    max_factor = int(2 * min_diff)
    if max_factor * max_factor == num: # perfect square will not yield 2 solns
        max_factor -= 1
        
    min_factor = int(map_diff_factor(num, max_diff)) + 1
    if min_factor * min_factor == (num / 3) and num % 3 == 0:
        min_factor += 1
        
    possible_factor_set = set(range(min_factor, max_factor + 1))

    if init_count + len (possible_factor_set) < target_count:
        return 0

    init_count += len(possible_factor_set.intersection (all_factor_set))
    
    if init_count == target_count:
        # print num
        return 1
    return 0
    
# Maps the difference to the corresponding factor of num
def map_diff_factor (num, diff):
   
    return (2 * diff - (4 * diff * diff - num) ** 0.5)

# Generates all factors given the prime factors and their exponents
def generate_all_factors (num, factor_list, factor_exp_list):
    master_list = []
    for i in range(len(factor_list)):
        factor = factor_list[i]
        factor_exp = factor_exp_list[i]
        
        if factor != 2:
            exp_list = [factor ** j for j in range(factor_exp_list[i]+1)]
        else:
            if factor_exp == 2:
                exp_list = [factor ** j for j in range(1, factor_exp_list[i])]
            else:
                exp_list = []
                for test_exp in range (2, factor_exp-1):
                    if num / (2 ** test_exp) >= (1 + 2 ** (test_exp - 2)):
                        exp_list.append(factor ** test_exp)
                
        master_list.append(exp_list)
    all_factor_list = [reduce(operator.mul, element) for
                       element in itertools.product (*master_list)]
    return all_factor_list
#---------------------------------------------------------------------------------


def check_perf_square (num):
    if int(num ** 0.5) ** 2 == num:
        return 1
    return 0
    
def main():
    start_time = time.time()
    max_num = 10 ** 6 - 1
    target_count = 10
    start_num = 1155
    condition_count = 0
    
    prime_list, num_list = gen_co_prime_sieve (max_num)
    prime_set = set(prime_list)

    i = start_num
    interval = 1
        
    while i <= max_num:
            
        num_factors, fact_exp_list = calc_num_factors (i, num_list, prime_set)

        if num_factors >= target_count/2 and num_factors <= 2 * target_count:

            factor_list = num_list[i][1]
            condition_count += count_num_solutions (i, num_factors, factor_list,
                                    fact_exp_list, target_count)

        i += interval
        interval = 4 - interval
        
    print condition_count
    print time.time() - start_time
main()
