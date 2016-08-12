# largest_prime_factor.py
# Find largest prime factor for inputted number

def generate_list_of_primes_below_target (target, prime_list = []):

    if target < 2:
        return 0
    prime_list.append(2)  # first prime
    test_num = 3

    while test_num < target:
        div_test = 0
        for prime in prime_list:
            if prime > (test_num ** 0.5):
                break
            if test_num % prime == 0:
                div_test = 1
                break
        if div_test == 0:
            prime_list.append (test_num)
        test_num += 2

def generate_prime_factors_of_num_below_target (num, target, prime_list, prime_factor_list):

    running_prod = 1
    
    for prime in prime_list:
        if prime > target:
            break
        if num % prime == 0:
            exp_no = 1
            while num % (prime ** exp_no) == 0:
                prime_factor_list.append (prime)
                running_prod *= prime
                exp_no += 1
            if (num / running_prod) in prime_list:
                prime_factor_list.append (num / running_prod)
                break
        if running_prod == num: # have found all factors
            break

def range_product (test_range):

    prod = 1
    for test in test_range:
        prod = prod * test
    return prod
                
num = 600851475143
prime_list = []

generate_list_of_primes_below_target (num ** 0.5, prime_list)

prime_factor_list = []
generate_prime_factors_of_num_below_target (num, num ** 0.5, prime_list, prime_factor_list)

if (range_product (prime_factor_list) == num):
    print prime_factor_list[-1]
else:
    print num / range_product (prime_factor_list)
