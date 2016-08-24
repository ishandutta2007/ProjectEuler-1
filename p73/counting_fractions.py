# counting_fractions.py
# Return # of reduced fractions between 1/3 and 1/2 with denominator
# less than or equal to 12000

import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")
from factors import gcd

def calc_numerator_list (denominator, min_frac, max_frac):
    start_int = int(min_frac * denominator) + 1
    if (max_frac * denominator) <= int(max_frac * denominator):
        end_int = int(max_frac * denominator) - 1
    else:
        end_int = int(max_frac * denominator)

    num_list = []
    interval = 1
    if denominator % 2 == 0:
        if start_int % 2 == 0:
            start_int += 1
        interval = 2
        
    for i in range (start_int, end_int+1, interval):
        if gcd ([i, denominator]) == 1:
            num_list.append(i)
    return len(num_list)


max_num = 12000
init_num = 4
num_fractions = 0
for i in xrange (init_num, max_num+1):
    num_fractions += calc_numerator_list (i, 1/3.0, 1/2.0)
print num_fractions
