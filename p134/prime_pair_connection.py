# prime_pair_connection.py
# For each pair of consecutive primes, p1 and p2, find the smallest number n
# such that the end digits are formed by p1, and the complete number is
# divisible by p2
# Return the sum of these numbers for prime pairs up to 10 ** 6

import sys, os, inspect, time, operator
from math import log

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))


from factors import sieve_primes

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

    base = base % mod_class
    for i in range (len(digit_list)):
        if i == 0:
            total_prod *= ((base ** digit_list[-i-1]) % mod_class)
        elif i == 1:
            base_num_exp = ((base ** rep_base) % mod_class)
            if base_num_exp > mod_class / 2:
                base_num_exp = base_num_exp - mod_class
          
            total_prod *= ((base_num_exp ** digit_list[-i-1]) % mod_class)
            total_prod %= mod_class
        else:
            base_num_exp = ((base_num_exp ** rep_base) % mod_class)
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

# Returns the smallest number n such that the end digits are prime1, and n
# is divisible by prime 2
def first_prime_connection (prime1, prime2):
    len_prime = len(str(prime1))
    ten_power = 10 ** len_prime
    ten_power_inverse = efficient_mod_exponentiation (ten_power,
                                                      prime2 - 2, prime2)
    init_digits = (ten_power_inverse * (-1 * prime1)) % prime2
    return init_digits * ten_power + prime1

def main():
    start_time = time.time()
    max_sieve_prime = 11 * 10 ** 5
    prime_target = 10 ** 6
    init_prime = 5

    sum_connections = 0
    prime_list = sieve_primes (max_sieve_prime)
    while prime_list[0] < init_prime:
        prime_list.pop(0)
    
    for i in xrange(len(prime_list)-1):
        prime1, prime2 = prime_list[i], prime_list[i+1]
        sum_connections += first_prime_connection (prime1, prime2)
        if prime2 > prime_target:
            break
    print sum_connections
    print time.time() - start_time
    
main()
