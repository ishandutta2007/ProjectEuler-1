# pandigital_prime_sets.py
# Find all ways to create a set of prime numbers such that across all members
# in each set, the digits 1-9 are used exactly once

import sys, os, inspect, time, itertools

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import is_prime

# Custom prime sieve
# This will maintain a separate list where the primes with unique digits
# and no zero digits are maintained
# Also, it will create a dictionary mapping sorted digits to the primes that
# are permutations of their digits

def sieve_primes (max_num):
    num_list = [0] * (max_num + 1)
    prime_list = [2]
    custom_prime_list = []
    prime_dict = {}
    prime_dict[2] = [2]

    for j in range (2+2, max_num+1, 2):
        num_list[j] = 1

    
    for i in xrange (3, max_num+1, 2):
        if num_list[i] == 0:
            prime_list.append(i)

            # Custom code-----------------------------------------------------
            if check_unique_zero_digits (i) == 1:
                custom_prime_list.append(i)
                sorted_dig_int = int(''.join(sorted(list(str(i)))))
                                     
                if sorted_dig_int in prime_dict:
                    prime_dict[sorted_dig_int].append(i)
                else:
                    prime_dict[sorted_dig_int] = [i]
            #-----------------------------------------------------------------
            
            for j in range (2*i, max_num+1, i):
                num_list[j] = 1


    return prime_list, custom_prime_list, prime_dict

# Check for unique digits and zero digits
def check_unique_zero_digits (num):

    num_str = str(num)
    if '0' in num_str:
        return 0
    num_set = set(list(num_str))
    if len(num_set) == len(num_str):
        return 1
    return 0
#------------------------------------------------------------------------------

# This finds all the primes with num_digits digits comprised of the digits
# 1 through 9 with no repeats. These are put in a list
# Finally, it adds these numbers to the prime_dict dictionary
def produce_prime_check_set (num_digits, prime_list, custom_prime_list,
                             prime_dict):
    prime_check_list = []
    total_digits = 9
    digit_list = range (1, total_digits + 1)

    perm_gen = itertools.permutations (digit_list, num_digits)
    
    for perm in perm_gen:
        if quick_prime_check (perm) == 1:
            perm_str = [str(dig) for dig in perm]
            perm_num = int(''.join(perm_str))
            prime_check_list.append(perm_num)
            
    prime_actual_list = [num_check for num_check in prime_check_list
                         if is_prime (num_check, prime_list) == 1]

    for prime in prime_actual_list:
        sorted_dig_int = int(''.join(sorted(list(str(prime)))))
                                     
        if sorted_dig_int in prime_dict:
            prime_dict[sorted_dig_int].append(prime)
        else:
            prime_dict[sorted_dig_int] = [prime]

    custom_prime_list += prime_actual_list
    
    return custom_prime_list, prime_dict

# Checks if num_tuple is divisible by 2,3, or 5. If so, returns 0, else 1
def quick_prime_check (num_tuple):
    if num_tuple[-1] % 2 == 0:
        return 0
    if num_tuple[-1] % 5 == 0:
        return 0
    if sum(num_tuple) % 3 == 0:
        return 0
    return 1
#------------------------------------------------------------------------------
# Counts all the sets that can be created from the digit_list consisting of
# all prime numbers using precisely all the digits inputted less than max_num
# Function is recursive, calling itself on the remaining digits when a prime is located
def gen_prime_sets (digit_list, prime_dict, max_num):

    count = 0
    for num_len in range(min([len(digit_list), len(str(max_num))]), 0, -1):
        
        # Generate the list of all primes of length num_len using these digits
        test_num_gen = itertools.combinations (digit_list, num_len)
        test_num_list =  list(test_num_gen)

        for test_tuple in test_num_list:
            sorted_tuple = sorted(list(test_tuple))
            tuple_str = [str(i) for i in sorted_tuple]
            test_int = int(''.join(tuple_str))
            
            # Dictionary gives all the primes that can be formed as permutations
            # of the test_int number
            if test_int in prime_dict:
                test_int_list = [prime for prime in prime_dict[test_int]
                                 if prime < max_num]
                
                remaining_digits = list(set(digit_list) - set(test_tuple))

                if len(remaining_digits) == 0:
                    count += len(test_int_list)
                else:
                    for prime in test_int_list:
                        rem_digits_copy = remaining_digits[:]
                        count +=  gen_prime_sets (rem_digits_copy, 
                                                  prime_dict, prime)
    return count

def main():
    start_time = time.time()
    n = 10 ** 7  # prime sieve limit

    prime_list, custom_prime_list, prime_dict = sieve_primes(n)

    # gathers the relevant primes with 8 digits
    num_digits = 8
    custom_prime_list, prime_dict = produce_prime_check_set (num_digits,
                                                             prime_list,
                                                      custom_prime_list,
                                                      prime_dict)

    print time.time() - start_time
    max_num = 10 ** 9 - 1 # largest 9 digit number
    test_digit_range = range(1,10)
    
    print gen_prime_sets (test_digit_range, prime_dict, max_num)
    
    print time.time() - start_time
    
main()
