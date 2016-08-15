# self_powers.py
# last 10 digits of large sum

import math

max_num = 1000
num_digits = 10
remainder_sum = 0
for i in range (1, max_num+1):
    
    remainder_sum += (i ** i) % (10 ** num_digits)
    remainder_sum %= (10**num_digits)
print remainder_sum
