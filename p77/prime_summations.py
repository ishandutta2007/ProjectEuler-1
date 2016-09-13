# prime_summations.py
# Find the smallest number which can be expressed as the sum of primes
# in 5000 ways

import sys, os, inspect, time
from math import factorial


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import sieve_primes


# This determines all pairs of primes which sum to num
# It modifies the prime threshold dictionary to account for these pairs too
def sum_pair_primes (num, prime_list, prime_sum_thresh_dict):

    total_sums = 0
    index = 0
    for p1 in prime_list:
        if p1 > num / 2.0:
            break
        if (num - p1) in set(prime_list):
            total_sums += 1
            prime_sum_thresh_dict [num, p1] = 1 # number of sums with p1 minimum
        else:
            prime_sum_thresh_dict [num, p1] = 0 # number of sums with p1 minimum
        index += 1

    return total_sums, prime_sum_thresh_dict, index - 1

def count_prime_sums (num, prime_list, prime_sum_dict, prime_sum_thresh_dict):

    total_sums, prime_sum_thresh_dict, final_index = sum_pair_primes (num, prime_list,
                                                         prime_sum_thresh_dict)

    
    for p1 in prime_list:
        if p1 > num / 3.0:
            break
        if (num - p1) in prime_sum_dict:
            if p1 == 2:
                p1_sums = prime_sum_dict [num - p1]
            else:
                p1_sums = prime_sum_thresh_dict [num - p1, p1]
            total_sums += p1_sums
            prime_sum_thresh_dict [num, p1] += p1_sums


    if final_index > 0:
        for i in range (final_index-1, -1, -1):
            prime_sum_thresh_dict[num, prime_list[i]] += prime_sum_thresh_dict[num, prime_list[i+1]]
    
    
            
    print num, total_sums
    prime_sum_dict[num] = total_sums
    return prime_sum_dict, prime_sum_thresh_dict

def main():
    start_time = time.time()
    max_prime = 10 ** 6
    prime_list = sieve_primes (max_prime)
    target_num = 5000
    max_num = 10**3
    
    prime_sum_dict = {}
    prime_sum_thresh_dict = {}

    for num in range (2, max_num+1):
        prime_sum_dict, prime_sum_thresh_dict = count_prime_sums (num, prime_list, prime_sum_dict,
                                                                          prime_sum_thresh_dict)
        # print num, prime_sum_dict[num]
        
        if prime_sum_dict[num] > target_num:
            print num, prime_sum_dict[num]
            break
        
    print time.time() - start_time

main()
