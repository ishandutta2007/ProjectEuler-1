# distinct_primes_factors.py
# Find first occurrence of 4 consecutive integers
# such that all four have 4 distinct prime factors

# determine if exactly target number of prime factors
# if prime, add to prime list
def gen_prime_factors (num, prime_list):
    
    target_factors = 4
    factor_list = []
    factor_prod = 1

    for prime in prime_list:
        
        if num % prime == 0:
            
            index = 1
            test = num/prime
            while test % prime == 0:
                index += 1
                test = test / prime

            factor_prod *= (prime ** index)
            
            factor_list.append([prime, index])

        if factor_prod == num:
            if len (factor_list) == target_factors:
                return 1
            return 0
        
        if len (factor_list) == target_factors: # must be one more factor
            return 0

        if prime > (num ** 0.5):
            if len (factor_list) == 0: # num is prime
                prime_list.append (num)
                return 0
             # in this case, target minus one factor found,
             # must be exactly one more
            if len (factor_list) == (target_factors - 1):
                return 1
            return 0


prime_list = [2]
i = 3
consec_len = 0
consec_target = 4
while consec_len < consec_target:
    if gen_prime_factors (i, prime_list) == 1:
        consec_len += 1
    else:
        consec_len = 0
    i += 1

print i - 4
