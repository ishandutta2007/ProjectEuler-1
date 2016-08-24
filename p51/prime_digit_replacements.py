# prime_digit_replacements.py
# Find the smallest prime such that replacing several of its digits
# with the same digit yields primes for 8 digits

import sys
from bisect import bisect_left
import collections

home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")
from factors import gen_prime_list, is_prime


def digit_frequency (num):
    target_num = 3
    num_target_digits = 0
    digit_list = list(str(num))
    counter = collections.Counter (digit_list)
    digit_placement = []
    for x in counter.most_common(3):
        if x[1] >= target_num:
            target = x[0]
            target_loc = []
            for i in range(len(digit_list)):
                if digit_list[i] == target:
                    target_loc.append(i)
            target_tuple = (target, target_loc)
            digit_placement.append (target_tuple)
                        
    return digit_placement

# generate list of integers with 
def replace_target_digits (num, digit_list):
    num_list = list(str(num))

    replace_list = []
    num_digits = 10
    for i in xrange(num_digits):
        test_list = num_list
        for j in digit_list:
            test_list[j] = str(i)
        replace_list.append (int(''.join(test_list)))
    return replace_list

prime_list = []
max_num = 10 ** 6
gen_prime_list (max_num, prime_list)

min_prime = 10000 # given in problem
pos = bisect_left (prime_list, min_prime)
prime_list = prime_list[pos:]

for prime in prime_list:
    freq_list = digit_frequency(prime)
    if len(freq_list) > 0: # some digit appears more than 3 times
        for freq in freq_list:
            check_list =  replace_target_digits (prime, freq[1])
            no_count = 0
            check_success = []
            for check in check_list:

                if check not in set(prime_list):
                    no_count += 1
                    if no_count > 2:
                        break
                else:
                    check_success.append(check)
            if no_count <= 2:
                print check_success
                sys.exit(0)
                 
