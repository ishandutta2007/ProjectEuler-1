# quad_primes.py
# Find a, b such that n**2+an+b generates
# the most consecutive primes starting w n = 0

import sys
sys.path.insert(0, '/home/osboxes/ProjEuler/Utilities')
from factors import is_prime
from factors import gen_prime_list

def count_consec_primes (a,b):
    check_prime = True
    n = 0
    while check_prime == True:
        num = n**2 + (a * n) + b
        if is_prime(num) == 0:
            check_prime = False
            return n-1
        n += 1


max_num = 1000
max_pair = 0,0
max_consec_primes = 0

prime_list = []
gen_prime_list (max_num, prime_list)


for b in range (3, max_num, 2):
    if b not in prime_list:
        continue
    for a in range (-1*b, max_num, 2):
        if (1 + a + b) not in prime_list:
            continue
        consec_primes =  count_consec_primes (a,b)
        if consec_primes > max_consec_primes:
            max_consec_primes = consec_primes
            max_pair = a,b
            
print max_pair, max_consec_primes
print max_pair[0] * max_pair[1]
