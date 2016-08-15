# prime_permutations.py
# Find arithmetic sequence of 3 primes such that
# all are permutations of the others' digits

home_path = "/home/osboxes/ProjEuler/"
import sys

sys.path.insert (0, home_path + "Utilities/")
from factors import gen_prime_list

# generate primes up to max_num
max_num = 10000
prime_list = []
gen_prime_list (max_num, prime_list)

# remove the primes below min_num
import bisect
min_num = 1000
start_pos = bisect.bisect_left (prime_list, min_num)
prime_list = prime_list[start_pos:]


def check_for_primes (num_list, prime_set):
    final_list = []
    for num in num_list:
        if num > 1000 and num in prime_set:
            final_list.append(num)

    return final_list
            
# checking for 3 element arithmetic sequence including first element
def check_for_sequence (init_elt, num_set):

    for num in num_set:
        diff = num - init_elt
        if num + diff in num_set and diff > 0:
            return init_elt, num, num + diff
    return [0]

import itertools

for prime in prime_list:
    perm_list = itertools.permutations (str(prime))
    perm_nums = [int("".join(x)) for x in perm_list]

    final_nums = check_for_primes (perm_nums, set(prime_list))
    while prime in final_nums:
        final_nums.remove (prime)
    
    if len(final_nums) >= 2:
        seq = check_for_sequence (prime, set(final_nums))
        if len (seq) == 3:
            print seq
    
