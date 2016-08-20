# ordered_fractions.py
# Find largest reduced fraction, with denominator <= 1 MM which
# is less than 3/7

home_path = "/home/osboxes/ProjEuler/"
import sys
sys.path.insert (0, home_path + "Utilities/")
from factors import gcd

# Find numerator such that num/den is reduced and is between the 2 inputs
def find_numerator(denom, min_frac, max_frac):

    numerator = min_frac * denom
    numerator = int(numerator) + 1
    
    valid_solution = [0,0]
    
    while numerator / (denom + 0.0) < max_frac:
        if gcd ([numerator, denom]) == 1:
            valid_solution = [numerator, denom]
        numerator += 1

    if valid_solution != [0,0]:
        return valid_solution[0]
    return 0

min_frac = 2/5.0
max_frac = 3/7.0
max_denom = 1000000
init_denom = 9
target_numerator = 2
target_denominator = 5

for i in xrange(init_denom, max_denom+1):
    num = find_numerator (i, min_frac, max_frac)
    if num > 0:
        min_frac = num / (i+0.0)
        target_numerator = num
        target_denominator = i

print target_numerator, target_denominator
