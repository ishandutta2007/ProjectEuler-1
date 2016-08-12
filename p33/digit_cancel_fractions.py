# digit_cancel_fractions.py

import sys
sys.path.insert (0, '/home/osboxes/ProjEuler/Utilities')

from factors import gcd

# fraction with the least common denominator
def lcd (numer, denom):
    common_factor = gcd([numer, denom])
    return numer / common_factor, denom / common_factor

denom_prod = 1
numer_prod = 1
min_numer = 10
max_numer = 99
for numer in range (min_numer, max_numer+1):
    numer_last_digit = numer % 10
    numer_first_digit = numer/10
    if numer_last_digit == 0:
        continue
    if numer_first_digit > numer_last_digit:
        continue
    for denom in range (10 * numer_last_digit+1, 10 * (numer_last_digit+1)):
        if numer >= denom:
            continue
        denom_last_digit = denom % 10
        denom_first_digit = denom / 10

        if numer / (denom+0.0) == (numer_first_digit / (denom_last_digit + 0.0)):
            l_numer, l_denom = lcd (numer, denom)
            denom_prod *= l_denom
            numer_prod *= l_numer


final_num, final_dem = lcd (numer_prod, denom_prod)
print final_dem
