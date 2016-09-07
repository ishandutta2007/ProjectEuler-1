# totient_alt.py
# Find x such that phi (x) is a permutation of the digits of x, and
# x / phi(x) is minimized for x <= 10 MM

import sys, os, inspect, time
from math import factorial

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_prime_list

from itertools import permutations

# Returns the prime factorization of the number inputted
# Prime list needs all primes up to sqrt(num)
def prime_factorize (num, prime_list, min_scale):
    factor_list = []
    if num in set(prime_list):
        factor_list.append ((num, 1))
        return factor_list

    prod = 1
    prime_frac_prod = 1
    for prime in prime_list:
        index = 0
        while num % (prime ** (index + 1)) == 0:
            index += 1
        if index != 0:
            prime_frac_prod *= (1 - 1 / (prime+0.0))
            if 1 / (prime_frac_prod+0.0) > min_scale and min_scale != 0:
                return 0
            factor_list.append ((prime, index))
            prod *= prime ** index
            if prod == num:
                return factor_list
            if (num / prod) in prime_list:
                factor_list.append ((num/prod,1))
                return factor_list
            
    # At this point, we do not have a complete factorization
    # But, we know there can only be one more factor, and it must
    # be prime

    factor_list.append ((num/prod, 1))
    return factor_list

# This calculates the totient of num (# of rel prime numbers less than num)
# but it checks if that number must have one less digit than the
# the original number
# if so, it ends the calculation and returns 0
def calc_totient (num, prime_list, min_scale):

    factor_list = prime_factorize (num, prime_list, min_scale)
    if factor_list == 0:
        return 0
    totient_prod = 1
    prime_frac_prod = 1
    for factor in factor_list:
        prime, exp = factor[0], factor[1]
        if exp == 1:
            totient_factor = prime - 1
        else:
            totient_factor = (prime - 1) * (prime ** (exp - 1))
        totient_prod *= totient_factor

    return totient_prod

def check_if_permutation (num, test_num):

    if len(str(num)) != len(str(test_num)):
        return 0
    
    perm_set = set(map (''.join, permutations(str(num))))
    if str(test_num) in perm_set:
        return 1
    return 0

def output_possible_digits (test_list, curr_digits, min_num, max_num):

    # Base case
    if len(test_list) == 1:
        final_str = list(curr_digits) + test_list
        final_test_num = int(''.join(final_str))
        if final_test_num > min_num and final_test_num < max_num:
            return [final_test_num]
        else:
            return []

    
    # what digits can be added to keep curr_digits between min_num and max
    possible_list = []
    
    curr_len = len(curr_digits)
    if curr_digits == (str(min_num))[0:curr_len]:
        min_dig = str(min_num)[curr_len]
    else:
        min_dig = '0'

    if curr_digits == (str(max_num))[0:curr_len]:
        max_dig = str(max_num)[curr_len]
    else:
        max_dig = '9'

    for index in range(len(test_list)):
        if test_list[index] >= min_dig and test_list[index] <= max_dig:
            new_test_list = test_list[:]
            del new_test_list[index]
            possible_list += output_possible_digits (new_test_list,curr_digits + test_list[index],
                                  min_num, max_num)
            
    return possible_list
            
# Return all permutations that fall within the min_num and max_num bounds
def find_relevant_permutations (num, min_ratio):

    num_str = str(num)
    num_len = len(num_str)
    max_num = num
    if min_ratio == 0:
        min_num = 0
    else:
        min_num = max(num * (1.0 / min_ratio), 10 ** (num_len-1))

    if factorial (num_len) < 200:
    

        perm_list = list(map (''.join, permutations(str(num))))

        if min_ratio == 0:
            return perm_list

        final_list = filter (lambda x: int(x) < num and int(x) > (1 / (min_ratio+ 0.0)) * num, perm_list)
        return final_list

    # For larger numbers, we'll generate the list of possibilities

    first_digit = num_str[0]
    test_str = list(num_str)
    del test_str[0]
    
    final_list = output_possible_digits (test_str, num_str[0], min_num, max_num)
    return final_list
    
    
start_time = time.time()
max_num = 10 ** 7
prime_list = []
gen_prime_list (int(max_num ** 0.5) + 1, prime_list)
min_ratio = 0
min_num = 0

for i in xrange (3, max_num, 2):
    num_len = len(str(i))

    if i % 3 == 0 or i % 5 == 0 or i % 7 == 0:
        continue

    possible_list = find_relevant_permutations (i, min_ratio)

    if len(possible_list) == 0:     
        continue
    
    phi = calc_totient (i, prime_list, min_ratio)

    if phi in set(possible_list):

        min_ratio = i / (phi + 0.0)
        min_num = i

        
print min_num, min_ratio
print time.time() - start_time
