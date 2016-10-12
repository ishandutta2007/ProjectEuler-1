# amicable_chains.py
# Find the smallest member of the longest amicable chain for all
# numbers under a million

import sys, os, inspect, time
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


def prime_factorize (num, factor_list):
    if len (factor_list) == 1:
        exp = int(log(num) / log (factor_list[0]))
        return [(factor_list[0], exp)]
    prime_factor_list = []
    for factor in factor_list:
        exp = 1
        while num % (factor ** exp) == 0:
            exp += 1
        prime_factor_list.append((factor, exp - 1))
    return prime_factor_list


def gen_factor_sums (min_num, max_num, factor_list, prime_list):
    factor_sum_list = [[0]] * min_num
    for i in xrange(min_num, max_num+1):
        if i in set(prime_list):
            factor_sum_list.append([1 + i, 1])  # factor sum and exponent for least factor
        elif len(factor_list[i][1]) == 1:
            base =  factor_list[i][1][0]
            new_sum = factor_sum_list[i/base][0] + i
            exp = factor_sum_list[i/base][1] + 1
            factor_sum_list.append([new_sum, exp])
        else:
            first_factor = factor_list[i][1][0]
            if (i / first_factor) % first_factor == 0:
                exp = factor_sum_list[i/first_factor][1] + 1
                prev_sum =  factor_sum_list[i/first_factor][0]
                x1 = prev_sum / ((first_factor ** exp - 1)/ (first_factor - 1))
                factor_sum_list.append([prev_sum + (first_factor ** exp)*x1, exp])
            else:
                prev_sum =  factor_sum_list[i/first_factor][0]
                factor_sum_list.append([prev_sum * (1 + first_factor), 1])
    return factor_sum_list

def calc_amicable (num, factor_list, amicable_dict, orig_num):


    prime_factor_list = prime_factorize (num, factor_list)
    num_factor_sum = factor_sum (num, prime_factor_list) - num
    if num_factor_sum < orig_num:    
        return 0
    if num_factor_sum in amicable_dict:
        return 0
    return num_factor_sum

def main():
    start_time = time.time()
    max_num = 10 ** 6
    prime_list, factor_list = gen_co_prime_sieve (max_num)
    print time.time() - start_time
    # factor_sum_list = gen_factor_sums (2, max_num, factor_list, prime_list)
    print time.time() - start_time
    # sys.exit()
    # list of nums that are not amicable
    non_amicable_list = []
    # maps amicable nums to their chain length
    amicable_dict = {}
    max_chain_len = 1


    for i in xrange (2, max_num+1):

        chain_len = 1
        chain_list = [i]
        if i in set(prime_list):
            continue
        if i in amicable_dict:
            continue
        if i % 10**4 == 0:
            print i, time.time() - start_time
        factor_line = factor_list[i][1]        
        next_sum = calc_amicable (i, factor_line, 
                                  amicable_dict, i)

        while next_sum not in set([0,1,i]):

            chain_len += 1
            if next_sum in set(prime_list) or next_sum > max_num or (next_sum in
                                                                     chain_list):
                next_sum = 1
            else:
                chain_list.append (next_sum)
                if next_sum in set(prime_list):
                    next_sum = 1
                else:
                    factor_line = factor_list[next_sum][1]        
                    next_sum = calc_amicable (next_sum, factor_line,
                                          amicable_dict, i)
                 

        if next_sum == i:

            for num in chain_list:
                amicable_dict[num] = chain_len
            if chain_len > max_chain_len:
                max_chain_len = chain_len
                min_member = min(chain_list)
                print min_member, chain_len
                
    print time.time() - start_time
main()
