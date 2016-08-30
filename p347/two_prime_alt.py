# two_prime_integer.py
# Find the largest integer lower than 10 MM divisible by
# exactly 2 primes. Find the suitable integer across all
# pairs of prime and sum them

import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")

from factors import gen_prime_list, is_prime

from bisect import bisect_left
from math import log

def max_num_two_primes (max_num, p1, p2):
    closest_int = 0
    exp1 = int(log(max_num) / log(p1))

    for i in range (exp1-1, 0, -1):
        exp2 = int (log(max_num / (p1**i)) / log (p2))
        closest_int = max (closest_int, (p1 ** i) * (p2 ** exp2))
                    
    return closest_int

    
max_num = 10 ** 7
prime_list = []
gen_prime_list (max_num/2, prime_list)

pos = bisect_left (prime_list, int(max_num ** 0.5))
total_sum = 0

for i in xrange(pos+1):
    max_prime = max_num / prime_list[i]
    pos2 = bisect_left (prime_list, max_prime)
    
    for j in xrange(i+1, pos2+1):
        if j >= len(prime_list):
            break
        if prime_list[i] * prime_list[j] > max_num:
            break
        test = max_num_two_primes (max_num, prime_list[i], prime_list[j])
        total_sum += test


print total_sum


