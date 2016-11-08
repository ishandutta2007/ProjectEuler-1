# primes_with_runs.py
# For each digit 0-9, find the primes with 10 digits
# that have the most repeated instances of each digit. If more than one,
# (e.g. 5 primes with 9 occurrences of 8), return them all. Sum them all

import sys, os, inspect, time
from math import factorial
from copy import copy

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import is_prime, sieve_primes
import itertools

#---------------------------------------------------------------------------------------
# Returns list of all n-digit numbers in which the digit d recurs k times
# Numbers are in the form of a list of digits
def repeated_dig_nums (n, d, k):
    if k > n:
        return []
    initial_list = [d] * n
    if k == n:
        return initial_list

    total_digits = 10
    num_other_digits = n - k
    other_num_range = set(range(total_digits)) - set([d])
    
    other_digit_indices = copy(list(itertools.combinations(range(n), num_other_digits)))

    
    other_digit_possibles = itertools.product(other_num_range, repeat= num_other_digits)
    total_num_list = []

    for dig_list in other_digit_possibles:
        total_num_list +=  gen_possible_nums (initial_list, other_digit_indices,
                                              dig_list)
    return total_num_list

# Initial list consists of all the same digit
# Function will insert the values in dig_list at the indices in the
# other_digit_indices list within initial_list
def gen_possible_nums (initial_list, other_digit_indices, dig_list):

    dig_list_copy = copy(dig_list)

    num_list = []
    for indices in other_digit_indices:
        new_init_list = initial_list[:]

        for counter in range(len(indices)):
            new_index = indices[counter]
            new_digit = dig_list_copy[counter]
            new_init_list[new_index] = new_digit
        num_list.append (new_init_list)
    return num_list

#---------------------------------------------------------------------------------------
# This takes the list of numbers, where each number is in the form of a list of digits
# It checks if the number is valid in general (doesn't start with zero)
# Then it does quick primality tests to see if it's worth checking formally (e.g even)
# It returns a list of all valid numbers as actual numbers
def check_valid_nums (num_list):

    final_num_list = []
    for test_num in num_list:
        if test_num[0] == 0: # first digit zero
            continue

        # From here, function will do primality checks for 2, 3, and 5
        if test_num[-1] % 2 == 0:
            continue
        if sum(test_num) % 3 == 0:
            continue
        if test_num[-1] % 5 == 0:
            continue
        test_str = [str(i) for i in test_num]
        final_num_list.append (int(''.join(test_str)))
    return final_num_list
#------------------------------------------------------------------------------------

def main ():
    start_time = time.time()
    num_digit_choices = 10
    num_test_digits = 10 # number of digits in the test numbers
    max_num = 10 ** num_test_digits
    prime_list = sieve_primes (int(max_num ** 0.5))

    relevant_primes = []
    for i in range(num_digit_choices):
        for k in range(num_test_digits - 1, 0, -1):
            num_list = repeated_dig_nums (num_test_digits, i, k)
            final_num_list = check_valid_nums (num_list)
            counter = 0
            for num in final_num_list:
                if is_prime(num, prime_list) == 1:
                    relevant_primes.append(num)
                    counter += 1
            if counter > 0:
                break
            
    print sum(relevant_primes)
    
    print time.time() - start_time

main()
