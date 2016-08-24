# convergents_e.py
# Return sum of the digits of the numerator
# of the 100th fractional convergent (cont fraction expansion) of e

import math

def next_convergent (term, num1, den1, num2, den2):
    num = term * num1 + num2
    den = term * den1 + den2

    return num, den

def digit_sum (num):
    num_list = list(str(num))
    dig_sum = 0
    for dig in num_list:
        dig_sum += int(dig)
    return dig_sum


max_num = 100
num, den = 3,1
prev_num, prev_den = 2,1
var_term = 2
i = 3
while i <= max_num:

    if (i%3 == 0):
        term = var_term
        var_term += 2
    else:
        term = 1

    new_num, new_den = next_convergent (term, num, den, prev_num, prev_den)
    prev_num, prev_den = num, den
    num, den = new_num, new_den

    i += 1

print digit_sum (num)
