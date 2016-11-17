# prime_square_remainders.py

import sys, os, inspect, time

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import sieve_primes

def remainder_function (prime_index, prime_num):
    return 2 * prime_index * prime_num % (prime_num ** 2)

def main():
    start_time = time.time()
    max_prime_num = 10**6
    prime_list = sieve_primes (max_prime_num)

    target_remainder = 10 ** 10
    start_index = 7037 # from problem

    while remainder_function (start_index, prime_list[start_index-1]) <= target_remainder:
        start_index += 2
    print start_index
    print time.time() - start_time

main()

    
