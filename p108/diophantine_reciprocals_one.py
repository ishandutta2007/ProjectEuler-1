# diophantine_reciprocals_one.py
# Find the least n, such that 1/n can be represented as 1/x + 1/y in
# more than 1000 distinct ways

# Can show mathematically that number of representations is a function of
# prime factorization exponents. If those exponents are n1, n2, n3, the
# representations will number: ((2n1+1)*(2n2+1)*(2n3+1)+1)/2

from math import log

import sys, os, inspect, time

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import sieve_primes


def find_least_representation (prime_list, max_num, curr_list, target):

    # Base case

    if calc_actual_number (prime_list, curr_list) > max_num:
        return max_num
    
    if calc_total_representations (curr_list) > target:
        
        return calc_actual_number (prime_list, curr_list)

    

    if len(curr_list) == 0:
        curr_representations = 1
    else:
        curr_representations = calc_total_representations (curr_list)
    
    min_range = 1
    max_range = int((target / (curr_representations * 1.0) - 1)/2) + 1

    max_ratio = max_num / (1.0*calc_actual_number (prime_list, curr_list))
    max_range = min (max_range,
                     int(log(max_ratio)/log(prime_list[len(curr_list)])))
    if len(curr_list) > 1:
        max_range = min(max_range, curr_list[-1])
    
    for i in range(min_range, max_range+1):
        new_list = curr_list[:]
        new_list.append(i)
        test_num = find_least_representation (prime_list, max_num, new_list,
                                              target)
 
        max_num = min(test_num, max_num)
    return max_num

def calc_total_representations (exponent_list):
    rep_product = 1
    for exp in exponent_list:
        rep_product *= (2 * exp + 1)
    return rep_product

def calc_actual_number (prime_list, exponent_list):
    num_prod = 1
    for num_index in range(len(exponent_list)):
        num_prod *= (prime_list[num_index] ** exponent_list[num_index])
    return num_prod
#------------------------------------------------------------------------------

def main():
    start_time = time.time()
    target = 4000000
    effective_target = 2 * target - 1
    max_primes_needed = int(log (effective_target) / log(3)) + 1
    if max_primes_needed < 20:
        prime_num = 100
    else:
        prime_num = 10000 # can calculate more precisely if needed
        
    prime_list = sieve_primes (prime_num)
    max_num = 1
    for i in range(max_primes_needed):
        max_num *= prime_list[i]
    
    print find_least_representation (prime_list, max_num, [],
                                     effective_target)
    print time.time() - start_time
main()
