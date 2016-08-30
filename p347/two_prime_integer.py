# two_prime_integer.py
# Find the largest integer lower than 10 MM divisible by
# exactly 2 primes. Find the suitable integer across all
# pairs of prime and sum them

import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")

from factors import gen_prime_list, is_prime

def sieve_primes (max_num):
    num_list = [0] * (max_num+1)
    primes = []
    for i in xrange (2, max_num+1):
        if num_list[i] == 0:
            # primes.append (i)
            num_list[i] = [1]
            k = i
            while (k * i <= max_num):
                if num_list[k*i] == 0:
                    num_list[k*i] = 1, (i,k)
                k += 1
    return num_list
#  If num is a product of powers of p1 and p2, then return 1
# Otherwise return 0
def check_exactly_two_factors (num, p1, p2):
    if num % p1 != 0 or num % p2 != 0:
        return 0
    test_num = num
    i = 1
    while (num % (p1 ** i) == 0):
        test_num = test_num / p1
        i += 1

    i = 1
    while (num % (p2 ** i) == 0):
        test_num = test_num / p2
        i += 1

    if test_num == 1:
        return 1
    return 0
    
max_num = 10 ** 6

num_list = sieve_primes (max_num)

prime_list = []
two_prime_dict = {}

for i in xrange (2, max_num+1):

    if len (num_list[i]) == 1:
        prime_list.append(i)
        continue
    
    p1, k = num_list[i][1][0], num_list[i][1][1]

    while (k % p1 == 0):
        k = k / p1
    if k == 1:  # power of a prime, not relevant
        continue
    if k in set(prime_list): 
        two_prime_dict[p1,k] = i
        continue
    
    p2 = num_list[k][1][0]
        
    if check_exactly_two_factors (i, p1, p2) == 1:
        two_prime_dict[p1,p2] = i

    if i % 100000 == 0:
        print i
        
print sum(two_prime_dict.values())


