# large_non_mersenne_prime.py
# Want to solve this without calculating
# insanely large numbers

from math import log

base = 2
exp = 7830457
scale = 28433
addend = 1
num_digits = 10

# choose exponent such that 2 ** exp < 10 ** 10
min_exp = int(num_digits * log(10) / log(base)) + 1
init_base = (base ** min_exp) % (10 ** num_digits)

# Express exp / min_exp in base 2 so that we can
# square init_base appropriately to arrive at the exponent

bin_expr = bin(exp/min_exp)[2:]
remainder = exp % min_exp
running_total = 1

for i in range (len(bin_expr)):
    if bin_expr[i] == '1':
        interim_total = init_base
        # continue squaring
        for j in range(len(bin_expr)-i-1):
            interim_total = (interim_total * interim_total) % (10 ** num_digits)

        # no squaring in the last digit of the binary expansion
        if i == len(bin_expr) - 1:
            interim_total = init_base
        running_total = (running_total * interim_total) % (10 ** num_digits)

running_total = (running_total * (base ** remainder))  % (10 ** num_digits)
running_total *= scale 
running_total += addend

print (running_total % (10 ** num_digits))
