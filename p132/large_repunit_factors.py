# large_repunit_factors.py
# Find the first 40 prime factors of R(10 ** 9), repunit with a billion ones

import sys, os, inspect, time, operator
from math import log

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve

# Calculates number of elements i below num such that i and num are co-prime
# Aka the size of the multiplicative group of the integers mod n
def phi(num, prime_set, num_list):
    if num == 1:
        return 1
    if num in prime_set:
        return num - 1
    factor_list = num_list[num][1]
    
    return ((num * reduce (operator.mul, [(p-1) for p in factor_list]))/
            reduce (operator.mul, [p for p in factor_list]))


#------------------------------------------------------------------------------
# Calculate gcd of two numbers using their prime factors
# Uses function below as well to determine max exponents
def generate_gcd (num1, num_list, prime_set, num2, num2_factor_list):

    x1, x2 = min(num1, num2), max(num1, num2)
    if x1 == x2:
        return x1
    if x2 % x1 == 0:
        return x1
    if x1 in prime_set or x2 in prime_set:
        return 1

    factor_list1, factor_list2 = set(num_list[x1][1]), set(num2_factor_list)

    common_factors = list(factor_list1.intersection(factor_list2))
    if len(common_factors) == 0:
        return 1
    gcd_product = 1
    for factor in common_factors:
        gcd_product *= (factor ** max_exponent_prime_factor (x1, x2, factor, 1))
    return gcd_product

# Determine the max exponent of p that divides both x1 and x2
# known is the least known exponent that satisfies
def max_exponent_prime_factor (x1, x2, p, known):

    n = 0
    exp = known + 2 ** n
    while x1 % (p ** exp) == 0 and x2 % (p ** exp) == 0:
        n += 1
        exp = known + 2 ** n

    if n == 0:
        return known
    if n == 1:
        return (known + 1)
    
    return max_exponent_prime_factor (x1, x2, p, known + 2 ** (n-1))
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
    max_prime = 25 * 10 ** 5
    repunit_len = 10 ** 9
    repunit_len_factors = [2,5]
    target_size = 40
    
    prime_list, num_list = gen_co_prime_sieve (max_prime)
    prime_set = set(prime_list)
    prime_factor_list = []

    for prime in prime_list:
        if prime < 7:
            continue

        test_gcd = generate_gcd (prime - 1, num_list, prime_set,
                                 repunit_len, repunit_len_factors)

        if efficient_mod_exponentiation (10, test_gcd, prime) == 1:

            prime_factor_list.append (prime)
            if len(prime_factor_list) == target_size:
                break

    print sum(prime_factor_list)
    print time.time() - start_time
main()
