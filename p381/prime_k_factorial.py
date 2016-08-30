# prime_k_factorial.py

import time
import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")

from factors import is_prime

# Find the sum of (p-1)!, ..., (p-5)! mod p
# This can be shown as the sum of (-2)^-1, (6)^-1, (-24)^-1
def factorial_sum (p1):
    total_sum = 0
    fact_dict = {}
    fact_dict[-2] = (-1 * ((p1 + 1) / 2)) % p1
    if p1 % 3 == 1:    
        fact_dict[-3] = (-1 * ((2*p1 + 1)/3)) % p1
    else:
        fact_dict[-3] = (-1 * ((p1 + 1)/3)) % p1
    fact_dict[6] = (fact_dict[-2] * fact_dict[-3]) % p1
    fact_dict[-4] = (-1 * (((p1 + 1) * (p1 + 1)) / 4)) % p1
    fact_dict[-24] = (fact_dict[6] * fact_dict[-4]) % p1

    return (fact_dict[-2] + fact_dict[6] + fact_dict[-24]) % p1


def sieve_primes (max_num):
    num_list = [0] * (max_num+1)
    primes = []
    for i in xrange (2, max_num+1):
        if num_list[i] == 0:
            primes.append (i)
            num_list[i] = [1]
            k = i
            while (k * i <= max_num):
                if num_list[k*i] == 0:
                    num_list[k*i] = 1
                k += 1
    return primes

start_time = time.time()

max_num = 10**8
start_num = 5
total_sum = 0

prime_list = sieve_primes (max_num)
end_time = time.time()
print end_time - start_time
prime_list.remove(2)
prime_list.remove(3)

for i in prime_list:
    total_sum += factorial_sum(i)
    

end_time1 = time.time()
print total_sum, end_time1 - end_time
    
