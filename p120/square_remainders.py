# square_remainders.py
# Maximize ((a-1) ** n + (a+1)) ** n % a**2 for all a from 3 to 1000 and sum

import time

#-----------------------------------------------------------------------------
# This can be derived by expanding out exponents
def remainder_formula (a, n):
    return ((2 * n * a) % (a**2))

# Based on the remainder formula, it is simple to show that one of two
# parameters for n must optimize it. Both are tried and the max is taken
def max_remainder (a):

    if a % 2 == 0:
        return max(remainder_formula (a, a/2 - 1),
                   remainder_formula (a, a - 1), 2)

    return (max(remainder_formula (a, (a-1)/2),
                remainder_formula (a, a-1), 2))
#----------------------------------------------------------------------------
def main ():
    start_time = time.time()
    min_range, max_range = 3, 1000

    total_sum = 0

    for a in range(min_range, max_range+1):
        total_sum += max_remainder (a)
    print total_sum
    print time.time() - start_time

main()
