# sum_primes.py
import math

def check_if_prime (n, prime_list):
    for prime in prime_list:
        if n % prime == 0:
            return 0
        if prime > (n ** 0.5):
            break
    return 1

prime_list = [2,3]
min_no = 4
max_no = 2000000

for i in range(min_no, max_no+1):
    if check_if_prime (i, prime_list) == 1:
        prime_list.append (i)

print sum (prime_list), len(prime_list), max_no / math.log (max_no)
