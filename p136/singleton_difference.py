# singleton_difference.py
# The solutions to this problem are 4 * p, 16 * p (p odd prime), and then all
# primes that equal 3 mod 4. The program counts these three pieces of the
# solution

import sys, os, inspect, time, itertools, operator
from math import log
from bisect import bisect_right

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import sieve_primes, fast_sieve_primes

# Find the primes that are 3 mod 4
def custom_sieve_primes (start_num, max_num, prime_list):

    mod_prime_list = [prime for prime in prime_list if prime % 4 == 3]

    num_list = [0] * (max_num + 1)
    
    for prime in mod_prime_list:
        if start_num % prime == 0:
            init_elt = start_num
        else:
            init_elt = (start_num / prime + 1) * prime
        if (max_num - init_elt) % prime == 0:
            num_elts = (max_num - init_elt) / prime + 1
        else:
            num_elts = (max_num - init_elt) / prime + 1
            

        num_list[init_elt::prime] = [1] * num_elts

    new_prime_list = [num for num in xrange(start_num,max_num+1)
                      if num_list[num] == 0 and num % 4 == 3]
    
    return mod_prime_list + new_prime_list


def main():

    start_time = time.time()

    # each factor below * p, odd prime, corresponds to a solution to the
    # problem
    factor1, factor2 = 4, 16  
    max_num = 50 * 10 ** 6
    init_max_num = max_num / factor1

    fast_prime_list = fast_sieve_primes (init_max_num)
    fast_prime_list.remove(2) # solutions will only correspond to odd primes

    factor1_piece = len (fast_prime_list) + 1
    factor2_piece = bisect_right (fast_prime_list, max_num / factor2) + 1
    
    
    mod_prime_list = custom_sieve_primes (init_max_num + 3, max_num,
                                          fast_prime_list)
    final_piece = len(mod_prime_list)
    
    print (factor1_piece + factor2_piece + final_piece)
    print time.time() - start_time

main()
