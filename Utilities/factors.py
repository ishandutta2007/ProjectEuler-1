# factors.py

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

    if len(test_list) == 1:
        return test_list[0]

    
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
