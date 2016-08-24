# divisibility_of_factorials.py
import gc
import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")

from factors import is_prime, gen_prime_list

from bisect import bisect_left


# outputs the prime factorization of the inputted number
def prime_factorize (num, prime_list):
    if num in set(prime_list):
        return [(num,1)]
    
    if num == 1:
        return []
    pos = bisect_left (prime_list, num ** 0.5)
    test_list = prime_list[:pos+1]
    
    for prime in test_list:
        index = 1
        if num % prime == 0:
            while num % (prime ** index) == 0:
                index += 1
            exp = index - 1
            return ([(prime, index-1)] + prime_factorize (num / (prime ** exp), test_list))

    prime_list.append(num)
    return [(num,1)] # assume prime if no prime divides it

# Returns a prime factor and its exponent of the inputted number
def first_factor (num, prime_list):
    for prime in prime_list:
        if num % prime == 0:
            index = 1
            while (num % (prime ** index) == 0):
                index += 1
            return (prime, index-1)
        if prime * prime > num:
            break
        
    prime_list.append (num)
    return (num, 1)



# Calculates s(p ** n) where p is prime
# Assumes numbers are calculated in order
# so that p ** (n-1) will be known before this is called
def s_primes (p, n, s_dict):
    
    if n == 1:
        s_dict[(p,1)] = p
        s_dict[p] = p
        return p

    if (p,n) in s_dict:
        return s_dict[(p,n)]

    last_index = s_dict[(p,n-1)]
    answer = last_index + p
    index = 1
    # this fills the dictionary s_dict with appropriate answers for all
    # possible p ** k values which map s to answer
    while (answer % (p ** index) == 0):
        s_dict[(p,n+index-1)] = answer
        s_dict[p ** (n+index-1)] = answer
        index += 1
    return answer

def s_nums (num, s_dict, prime_list, store_thresh):
    prime, exp = first_factor (num, prime_list)
    factor_list = []
    factor_list.append ((prime, exp))
    prod = prime ** exp
    while (num / prod) > store_thresh:
        prime, exp = first_factor (num / prod, prime_list)
        factor_list.append ((prime, exp))
        prod *= (prime ** exp)
        
    max_s_value = s_dict[num / prod]
    
    for factor in factor_list:
        max_s_value = max (max_s_value, s_primes (factor[0], factor[1], s_dict))

    if num <= store_thresh:
        s_dict[num] = max_s_value

    return max_s_value


max_num = 10 ** 8
store_thresh = 10 ** 7
prime_list = []
# gen_prime_list (int(max_num ** 1)+1, prime_list)


s_dict = {}
s_dict[1] = 1
total_sum = 0
for i in xrange (2,max_num+1):

    total_sum += s_nums (i, s_dict, prime_list, store_thresh)

    if (i % 10 ** 7 == 0):
        print i
print total_sum
gc.collect()
