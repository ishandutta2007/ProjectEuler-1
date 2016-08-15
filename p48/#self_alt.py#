# self_alt.py
# last 10 digits of large sum

import math

orig_sum = 10405071317 # given in problem, sum of 1^1,2^2,..., 10^10
max_num = 100000
num_digits = 10
remainder_sum = 0

for i in range (11, max_num+1):
    exp = 10 / math.log10 (i)
    num_gen = (int(exp) + 1)  # exponent such that i ** i > 10 ** 10
    new_exp =  num_gen

    new_base = (i ** new_exp) % (10 ** num_digits)
    total_exp = new_exp
    if new_base != 0:
        new_exp = int(10 / math.log10 (new_base)) + 1
    
    while i / total_exp > 10 and new_base != 0:
        new_base  =  (new_base ** (new_exp)) % (10 ** num_digits)
        total_exp = total_exp * new_exp

        if new_base != 0:
            new_exp = int(10 / math.log10 (new_base)) + 1

        
    test_gen =  (new_base ** (i / total_exp)) % (10 ** num_digits)
    
    remainder_sum += test_gen  * (i ** (i % total_exp))
    remainder_sum %= (10**num_digits)
                      
print (remainder_sum + orig_sum)%(10 ** num_digits)
