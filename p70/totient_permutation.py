# totient_permutation.py
# Find x such that phi (x) is a permutation of the digits of x, and
# x / phi(x) is minimized for x <= 10 MM

import sys, os, inspect, time

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
    phi = calc_totient (i, prime_list, min_ratio)
    if phi == 0:  # Means phi must have less digits than i
        continue
    if (i / (phi + 0.0)) > min_ratio and min_ratio > 0:
        continue
    if check_if_permutation (phi, i) == 1:
        if min_ratio == 0:
            min_ratio = i / (phi + 0.0)
            min_num = i
        else:
            if i / (phi + 0.0) < min_ratio:
                min_ratio = i / (phi + 0.0)
                min_num = i

                
print min_num, min_ratio
print time.time() - start_time

