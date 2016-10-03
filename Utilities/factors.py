# factors.py
from math import fabs

# Sum of all proper divisors of n
def sum_all_proper_divisors (n):
    divisor_sum = 1

    if n == 2:
        return divisor_sum
    
    if n % 2 != 0: # don't have to check odd divisors
        incr = 1
    else:
        incr = 1

        divisor_sum += 2
        if (n/2) != 2:
            divisor_sum += (n/2)
        
    for div in range (3, int(n**0.5)+1, incr):
        if n % div == 0:
            divisor_sum += div
            if (n/div) != div:
                divisor_sum += (n/div)
                
    return divisor_sum

# check if number is prime
def is_prime (n, prime_list = []):

    if n < 2:
        return 0
    if n == 2:
        return 1
    if n % 2 == 0:
        return 0

    if len(prime_list) == 0:

        for div in xrange(3, int(n**0.5)+1, 2):
            if n % div == 0:
                return 0
        return 1

    for prime in prime_list:
        if n % prime == 0:
            return 0
        if prime > n ** 0.5:
            return 1
        
    if max(prime_list) == 2:
        test_prime = 3
    else:
        test_prime = max(prime_list) + 2

    for i in xrange (test_prime, int(n ** 0.5), 2):
        if n % i == 0:
            return 0
    return 1
 
# generates list of primes up to n
def gen_prime_list (n, prime_list):
    prime_list.append (2)

    for i in range(3, n+1, 2):
        for prime in prime_list:
            if i % prime == 0:
                break
            if prime > i ** 0.5:
                prime_list.append(i)
                break

# calculates greatest common divisor of a list of integers
# recursively runs through the list
def gcd (num_list):

# eliminate same numbers from the list

    test_list = list(set(num_list))

    test_list_pos = [x for x in test_list if x >= 0]
    test_list_neg = [-1 * x for x in test_list if x < 0]
    test_list = test_list_pos + test_list_neg

    if len(test_list) == 1:
        if test_list[0] >= 0:
            return test_list[0]
        else:
            return -1 * test_list[0]

    
    if len (test_list) == 2:
        max_num = max(test_list)
        min_num = min(test_list)
        if min_num == 0:
            return 0
        if min_num < 0:
            print "Error - cannot take gcd of negative number"
            exit
        
        remainder = max_num % min_num
        while remainder > 0:
            max_num = min_num
            min_num = remainder
            remainder = max_num % min_num
        return min_num

    else:
        interim_gcd = gcd(test_list[1:])
        return gcd ([test_list[0], interim_gcd])


def gen_totient_list (max_num):
    tot_list = range(max_num+1)
    tot_list[1] = 0
    
    for i in xrange (2, max_num+1):
        if tot_list[i] == i:   # prime
            tot_list[i] = i-1
            for j in xrange (2*i, max_num+1, i):
                tot_list[j] *= (1 - 1.0/i)
    return tot_list

def sieve_primes (max_num):
    num_list = [0] * (max_num + 1)
    prime_list = [2]

    for j in range (2+2, max_num+1, 2):
        num_list[j] = 1

    
    for i in xrange (3, max_num+1, 2):
        if num_list[i] == 0:
            prime_list.append(i)
            for j in range (2*i, max_num+1, i):
                num_list[j] = 1


    return prime_list

def gen_co_prime_sieve (max_num):
    prime_list = []
    nums = [0] * (max_num+1)
    for i in range (2, max_num+1):
        if nums[i] == 0:
            prime_list.append (i)
            for j in range (2*i, max_num+1, i):
                if nums[j] == 0:
                    nums[j] = 1, [i]
                else:
                    nums[j][1].append(i)
                    
    return prime_list, nums

def gen_all_products (n, start=2):
    

    for i in xrange (start, int(n**0.5) + 1):
        if n % i == 0:
            for factor_list in gen_all_products(n/i, i):
                factor_list.append(i)
                yield factor_list
    yield [n]
