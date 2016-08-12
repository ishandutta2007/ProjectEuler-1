# digit_factorials.py
# find all numbers such that the sum of their digit factorials
# equals the original number

import math

def calc_digit_factorial (num):
    num_str = str(num)
    sum = 0
    for ch in num_str:
        sum += math.factorial(int(ch))
    return sum

def count_ones_zeroes (num):
    count = 0
    for ch in str(num):
        if ch == '0' or ch == '1':
            count+=1
    if count % 2 == 0:
        return 0
    return 1

max_digit = 9
max_num = 7 * math.factorial(max_digit)
min_num = 10

i = min_num
sum_dig_fact = 0
while i < max_num:
    if count_ones_zeroes (i) != (i % 2):
        i += 1
        continue
    if i == calc_digit_factorial (i):
        sum_dig_fact += i
        print i
    i += 1

print sum_dig_fact
