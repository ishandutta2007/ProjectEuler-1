# sub_string_div.py
# Find sum of all 10-digit pandigital numbers
# with certain conditions of divisibility of
# substrings of digits

import time

def sub_digit_cond (num):
    if len(str(num)) < 10:
        return 0
    prime_set = set([2,3,5,7,11,13,17])
    i_str = str(num)
    index = 1
    for prime in prime_set:
        if int(i_str[index:index+3]) % prime != 0:
            return 0
        index += 1
    return 1


# This recursively generates all the 10-digit pandigital numbers
# and then checks if the number satisfies the above condition
def generate_pandigital_nums (digit_list, prev_digits):

    pan_count = 0
    
    if len(digit_list) == 1:
        pandigit_test = int(prev_digits + str(digit_list[0]))
        if sub_digit_cond (pandigit_test) == 1:
            return pandigit_test
        return 0
    
    for dig in digit_list:
        test_list = list(digit_list)
        test_list.remove(dig)
        pan_count += generate_pandigital_nums (test_list, prev_digits+str(dig))
    return pan_count
t0 = time.time()

digit_list = range(10)
print generate_pandigital_nums (digit_list, "")
t1 = time.time()
print t1 - t0


