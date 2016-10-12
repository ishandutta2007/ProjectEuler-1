# amicable_chains.py
# Find the smallest member of the longest amicable chain for all
# numbers under a million

import sys, os, inspect, time, operator
from math import log


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve, prime_factorize

# Calculates sum of factors of num
def factor_sum (num, full_factor_list):
    factor_sum = 1

    for num_pair in full_factor_list:
        exp = num_pair[1]
        factor = num_pair[0]
        factor_sum *= (factor ** (exp + 1) - 1) / (factor - 1)
    return factor_sum


def calc_amicable (num, first_factor,
                   past_factor_sum, past_exp, scale_dict, max_num):

    if (num / first_factor) % first_factor != 0:
        factor_sum = past_factor_sum * (1 + first_factor) - num
        if factor_sum > max_num:
            return 0,0
        else:
            return factor_sum, 1

    if (first_factor, past_exp + 1) not in scale_dict:
    
        return 0, 0
    
    factor_sum = (past_factor_sum / scale_dict[first_factor, past_exp] *
            scale_dict[first_factor, past_exp+1]) - num

    if factor_sum > max_num:
        return 0,0
    return factor_sum, past_exp + 1
    


def make_scale_dict (prime_list, max_num):
    scale_dict = {}
    for prime in prime_list:

        scale_dict[prime,1] = 1 + prime
        i = 2
        while scale_dict[prime, i-1] + prime ** i <= max_num:
            scale_dict[prime, i] = scale_dict[prime, i-1] + prime ** i
            i += 1
    return scale_dict

# This function will generate the mapped values from applying the factor sum function
def determine_chains (new_values, factor_sum_list):
    chain_dict = {}
    max_chain_len = 0
    for val in new_values:
        if val in chain_dict:
            continue
        chain_list = []
        link = val
        while factor_sum_list[link][0] != val:
            chain_list.append(link)
            link = factor_sum_list[link][0]
        chain_list.append(link)
        chain_len = len(chain_list)
        for link in chain_list:
            chain_dict[link] = chain_len
        if chain_len > max_chain_len:
            max_chain_len = chain_len
            min_val = min(chain_list)

    return min_val, max_chain_len
            
def main():
    start_time = time.time()
    max_num = 10 ** 6
    min_num = 2
    prime_list, factor_list = gen_co_prime_sieve (max_num)
    prime_set = set(prime_list)
    scale_dict = make_scale_dict (prime_list, max_num)
    factor_sum_list = [[0] for i in range(min_num)]
    
    for i in xrange (min_num, max_num+1):

        if i in prime_set:
            factor_sum_list.append([1, 1])
            continue

        first_factor = factor_list[i][1][0]
        past_factor_sum = factor_sum_list[i/first_factor][0] + i / first_factor
        past_exp =  factor_sum_list[i/first_factor][1]
        if factor_sum_list[i/first_factor][0] != 0:
            
            next_sum, new_exp  = calc_amicable (i, first_factor, past_factor_sum,
                                            past_exp, scale_dict, max_num)
        else:
            next_sum, new_exp = 0,0

        factor_sum_list.append([next_sum, new_exp])

    factor_values = set([factor_sum_list[i][0] for i in range(len(factor_sum_list))])
    old_len = len(factor_values)
    new_values = set([factor_sum_list[i][0] for i in factor_values])
    new_len = len(new_values)
    while old_len != new_len:
        old_len = new_len
        new_values = set([factor_sum_list[i][0] for i in new_values])
        new_len = len(new_values)

    print determine_chains (new_values, factor_sum_list)

    print time.time() - start_time
main()
