# repunit_nonfactors.py
# Find all primes below 10 ** 5 that will never be factors of R(10 ** n)
# for all n. Return this sum

import sys, os, inspect, time, operator
from math import log

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve


#------------------------------------------------------------------------------
# Calculate gcd of an inputted number and 10 ** n for n unbounded
# Uses function below as well to determine max exponents
def generate_gcd (num1, num_list, prime_set, test_factors):

    num1_factors = set(num_list[num1][1])
    common_factors = (num1_factors.intersection (set(test_factors)))
    if len(common_factors) == 0:
        return 1
    prod = 1
    for factor in list(common_factors):
        prod = prod * (factor ** max_exponent_prime_factor (num1, factor, 1))
    return prod

    

# Determine the max exponent of p that divides x1
# known is the least known exponent that satisfies
def max_exponent_prime_factor (x1, p, known):

    n = 0
    exp = known + 2 ** n
    while x1 % (p ** exp) == 0:
        n += 1
        exp = known + 2 ** n

    if n == 0:
        return known
    if n == 1:
        return (known + 1)
    
    return max_exponent_prime_factor (x1, p, known + 2 ** (n-1))
#------------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Calculate base ** exp mod mod_class
# Handles large exponents by breaking them down into base 6
# and constantly taking remainders of the results
# Uses function below to determine representations in base 6
def efficient_mod_exponentiation (base, exp, mod_class):
    # we will use exp_base of 6 for convenience
    rep_base = 6
    digit_list = num2base (exp, rep_base) # puts number in base 6
    total_prod = 1

    for i in range (len(digit_list)):
        if i == 0:
            total_prod *= ((base ** digit_list[-i-1]) % mod_class)
        elif i == 1:
            base_num_exp = (base ** rep_base)
            if base_num_exp > mod_class / 2:
                base_num_exp = base_num_exp - mod_class
          
            total_prod *= ((base_num_exp ** digit_list[-i-1]) % mod_class)
            total_prod %= mod_class
        else:
            base_num_exp = (base_num_exp ** rep_base)
            if base_num_exp > mod_class / 2:
                base_num_exp = base_num_exp - mod_class
                
            total_prod *= ((base_num_exp ** digit_list[-i-1]) % mod_class)
            total_prod %= mod_class
    return (total_prod % mod_class)
            
# Given a base 10 number, will return a list of digits in the inputted base
def num2base (num, base):
    digits = []
    while num:
        digits = [num % base] + digits
        num = num/base
    return digits
#-----------------------------------------------------------------------------


def main():
    start_time = time.time()
    max_prime =  10 ** 5
    repunit_len_factors = [2,5]

    
    prime_list, num_list = gen_co_prime_sieve (max_prime)
    prime_set = set(prime_list)
    prime_nonfactor_list = []

    for prime in prime_list:
        if prime < 7:
            prime_nonfactor_list.append (prime)
            continue

        # In this case, test_gcd is the gcd between prime - 1
        # and 10 ** n where n is unbounded. 
        test_gcd = generate_gcd (prime - 1, num_list, prime_set,
                                 repunit_len_factors)

        if efficient_mod_exponentiation (10, test_gcd, prime) != 1:

            prime_nonfactor_list.append (prime)


    print sum(prime_nonfactor_list)
    print sum(prime_list)
    print time.time() - start_time
main()
