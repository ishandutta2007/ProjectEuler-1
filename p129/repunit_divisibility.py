# repunit_divisibility.py
# Find the smallest number such that the smallest repunit that it factors
# has more than a million digits


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

    if num in prime_set:
        return num - 1
    factor_list = num_list[num][1]
    
    return int(num * reduce (operator.mul, [(1-1.0/p) for p in factor_list]))
#------------------------------------------------------------------------------
# This checks ten's order within num's multiplicative group.
# If its order is less than a million, and 3 does not divide num, then we know
# that num cannot be the answer. 
# If we cannot eliminate num on this basis, we directly calculate the required
# repunit to see if it is divisible by num
def ten_order_mod_class (num, target_num, prime_set, num_list):
    phi_num =  phi (num, prime_set, num_list)
    
    if phi_num <= target_num and num % 3 != 0:
        return 0

    factor_list = num_list[phi_num][1]
    base = 10
    divisor_list, new_div_list = [], []
    for prime_factor in factor_list:
        if efficient_mod_exponentiation (base, phi_num/prime_factor, num) == 1:
            new_div_list.append (prime_factor)
            phi_num /= prime_factor

    while len(new_div_list) > 0:
        if num % 9 == 0:
            if phi_num * 9 <= target_num:
                return 0
        elif num % 3 == 0:
            if phi_num * 3 <= target_num:
                return 0
        else:
            if phi_num <= target_num:
                return 0
            
        divisor_list += new_div_list
        new_div_list = []
        factor_list = num_list[phi_num][1]
        for prime_factor in factor_list:
            if efficient_mod_exponentiation (base, phi_num/prime_factor,
                                             num) == 1:
                new_div_list.append (prime_factor)
                phi_num /= prime_factor
                
    if len(divisor_list) == 0: # 10 is primitive
        return 1


    if repunit_mod_class (phi_num, num) > target_num:
        
        return 1
    
# This function calculates the repunit of the inputted length modulo
# the inputted class. If it is zero, rep_length is returned. If not, it is multiplied
# until it becomes zero, and this length times the multiplication factor
# is returned
def repunit_mod_class (rep_length, mod_class):
    num_thousands = rep_length / 1000
    rep_remainder = rep_length % 1000

    # The product of the vbles below equals repunit 1000
    repunit_fifty = geo_sequence_sum (1, 10, 50, mod_class)
    complement_twenty = geo_sequence_sum (1,
                                          efficient_mod_exponentiation(10, 50,
                                                                       mod_class),
                                          20, mod_class)
    repunit_thousand = (repunit_fifty * complement_twenty) % mod_class

    complement_num_thousands = geo_sequence_sum (1,
                                                 efficient_mod_exponentiation(10,
                                                                              1000,
                                                                              mod_class),
                                                 num_thousands, mod_class)
    # This is repunit of length num_thousands
    part_repunit = (repunit_thousand * complement_num_thousands) % mod_class

    final_total = part_repunit
    for i in range(rep_remainder):
        final_total = ((10 * final_total) + 1) % mod_class

    if final_total == 0:
        return rep_length
    mult_factor = 1
    sum_total = final_total
    while sum_total != 0:
        sum_total = (sum_total + final_total) % mod_class
        mult_factor += 1
    return mult_factor * rep_length

    
# Gives the sum of a geometric sequence modulo mod_class    
def geo_sequence_sum (init_term, ratio, num_terms, mod_class):
    total_sum = 0
    prod = init_term
    for i in range(num_terms):
        if i > 0:
            prod *= ratio
            prod %= mod_class
            total_sum = (total_sum + prod) % mod_class
        else:
            total_sum += prod
    return total_sum
# Calculate base ** exp mod mod_class
# Handles large exponents by breaking them down into base 6
# and constantly taking remainders of the results
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
#------------------------------------------------------------------------------
        
def main():
    start_time = time.time()

    max_num = 12 * (10 ** 5)
    target_num = 10 ** 6
    prime_list, num_list = gen_co_prime_sieve (max_num)
    prime_set = set(prime_list)
    print time.time() - start_time
    
    test_num = target_num + 1
    
    while test_num < max_num:
        if ten_order_mod_class (test_num, target_num, prime_set, num_list):
            break
        test_num += 2
        if test_num % 5 == 0:
            test_num += 2
    print test_num

    print time.time() - start_time
main()
