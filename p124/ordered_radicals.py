# ordered_radicals.py
# Matching each number to its radical up to 100,000 and sorting by radical
# return the 10,000th value in the list

import sys, os, inspect, time, operator
from math import log

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve

# Counts the numbers below max_num whose radical equals rad_num
# Recursive function in number of rad_num_factors, where base case is one or two
def count_radical_num (max_num, rad_num_factors):
    rad_count = 0
    if len (rad_num_factors) == 1:
        return int (log (max_num) / log (rad_num_factors[0]))
    
    if len(rad_num_factors) == 2:
        factor1, factor2 = rad_num_factors[0], rad_num_factors[1]
        max_exp_2 = int(log (max_num) / log (factor2))
        count_list = [int(log(max_num / factor2 ** i) / log(factor1))
                      for i in range(1, max_exp_2+1)]
        return sum(count_list)

    
    factor_n = rad_num_factors[-1]
    max_exp_n = int(log (max_num) / log (factor_n))
    for i in range(1, max_exp_n + 1):
        rad_count += count_radical_num (max_num / (factor_n ** i),
                                        rad_num_factors[:-1])
    return rad_count

# This generates and sorts all the numbers below max_num whose radical
# is the product of rad_factors. It returns the sorted list.
# Function is recursive and follows same form of count_radical_num
def sort_radical_domain (max_num, rad_num_factors):
    rad_list = []
    if len (rad_num_factors) == 1:
        factor = rad_num_factors[0]
        max_exp = int (log (max_num) / log (factor))
        return [factor ** i for i in range(1, max_exp + 1)]

    if len(rad_num_factors) == 2:
        factor1, factor2 = rad_num_factors[0], rad_num_factors[1]
        max_exp_2 = int(log (max_num) / log (factor2))
        num_list = []
        for j in range (1, max_exp_2+1):
            for i in range (1, int(log(max_num/factor2**j)/log(factor1))+1):
                num_list.append ((factor1 ** i) * (factor2 ** j))
        return num_list

    num_list = []
    factor_n = rad_num_factors[-1]
    max_exp_n = int(log (max_num) / log (factor_n))
    for i in range(1, max_exp_n + 1):
        rad_list = sort_radical_domain (max_num / (factor_n ** i),
                                        rad_num_factors[:-1])
        if len(rad_list) > 0:
            num_list += [(factor_n ** i) * x for x in rad_list]
    return sorted(num_list)
#------------------------------------------------------------------------------
# Tests if number can be a possible radical (i.e. is squarefree)
def is_possible_radical (num, num_factors, prime_set):
    if num in prime_set:
        return 1
    factor_list = num_factors[1]
    if num == reduce (operator.mul, factor_list):
        return 1
    return 0
#------------------------------------------------------------------------------

def main():
    start_time = time.time()
    max_num = 100000
    tgt_index = 10000

    prime_list, num_list = gen_co_prime_sieve(max_num)
    prime_set = set(prime_list)
    total_count = 1  # assume that the radical of 1 is 1
    num = 1
    while total_count < tgt_index:
        num += 1
        if is_possible_radical (num, num_list[num], prime_set) == 1:
            if num in prime_set:
                num_factor_list = [num]
            else:
                num_factor_list = num_list[num][1]

            rad_count =  count_radical_num (max_num, num_factor_list)

            total_count += rad_count

    num_radical_list = sort_radical_domain (max_num, num_factor_list)
    rad_index = (len(num_radical_list) - 1) - (total_count - tgt_index) 
    print num_radical_list[rad_index]
    print time.time() - start_time

main()
    
