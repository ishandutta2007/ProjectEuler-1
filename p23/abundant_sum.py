# abundant_sum.py
# Sum all numbers that cannot be expressed as the sum of
# 2 abundant numbers

import sys
sys.path.insert(0, '/home/osboxes/ProjEuler/Utilities')
from factors import sum_all_proper_divisors

def gen_abundant_sums (n, abundant_list, abundant_sum_list, max_num):

    for num in abundant_list:
        if (n+num) <= max_num:
            abundant_sum_list.append (n + num)

max_num = 28123
abundant_list = []
abundant_sum_list = []

for i in range(1, max_num):
    if sum_all_proper_divisors(i) > i: # abundant criterion

        abundant_list.append(i)
        gen_abundant_sums (i, abundant_list, abundant_sum_list, max_num)
        abundant_sum_set = set (abundant_sum_list)
        abundant_sum_list = list (abundant_sum_set)

        
print sum(range(max_num+1)) - sum (abundant_sum_list)

non_sum_list = []
for i in range(1, max_num+1):
    if i not in abundant_sum_list:
        # print i
        non_sum_list.append(i)
print non_sum_list[20:40]

