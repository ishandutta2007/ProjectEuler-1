# composites_prime_repunit.py
# Find first 25 composite numbers such that if RP(k) is the minimum digit
# repunit divisible by n, then k also divides n-1
# Return this sum

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

# Calculate gcd of two numbers using their prime factors
def generate_gcd (num1, num2, num_list, prime_set):

    x1, x2 = min(num1, num2), max(num1, num2)
    if x1 == x2:
        return x1
    if x2 % x1 == 0:
        return x1
    if x1 in prime_set or x2 in prime_set:
        return 1

    factor_list1, factor_list2 = set(num_list[x1][1]), set(num_list[x2][1])

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
#-----------------------------------------------------------------------------

def calc_repunit_remainder (num_digits, mod_class):
    repunit = 0
    for i in range(num_digits):
        repunit = (10 * repunit + 1) % mod_class
    return repunit

def main():
    start_time = time.time()
    max_check_num = 15000
    target_list_len = 25
    prime_list, num_list = gen_co_prime_sieve (max_check_num)
    prime_set = set(prime_list)
    composite_list = []

    for i in range(9, max_check_num, 2):
        if i in prime_set or i % 5 == 0:
            continue

        if i % 3 != 0:
            test_gcd = generate_gcd(phi(i, prime_set, num_list), i - 1,
                                    num_list, prime_set)

        else:
            max_three_exp = int(log(i) / log(3))
            three_exp = max_exponent_prime_factor (i, 3 ** max_three_exp, 3,1)

            test_gcd = generate_gcd (phi(i / 3 ** three_exp, prime_set, num_list)
                                     * 3 ** three_exp, i - 1, num_list, prime_set)
        if test_gcd <= 2:
            continue
        
        if calc_repunit_remainder(test_gcd, i) == 0:
            composite_list.append(i)

            if len(composite_list) == target_list_len:
                print sum(composite_list)
                break
    print time.time() - start_time
main()
