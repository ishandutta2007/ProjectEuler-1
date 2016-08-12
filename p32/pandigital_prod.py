# pandigital_prods.py
# Sum of all products than can be written pandigitally
# a x b = c, where a, b, and c in total represent all digits 1-9 exactly once

def check_for_all_digits (a, b, c):
    digit_list = []
    total_str = str(a) + str(b) + str(c)
    for ch in total_str:
        if int(ch) in digit_list:
            return 0
        if int(ch) == 0:
            return 0
        digit_list.append(int(ch))

    if len(digit_list) == 9:
        return 1

    return 0

def check_digits_unique (num):
    digit_list = []
    for ch in str(num):
        if ch in digit_list:
            return 0
        digit_list.append(ch)
    return 1

def check_for_zeroes (num):
    if '0' in str(num):
        return 0
    return 1

pandigit_prod_list = []

# first, check 1 digit x 4 digit numbers

for a in range(2,9):
    for b in range (1234, 10000/a):
        
        str_union = str(a) + str(b)
        if check_for_zeroes (int(str_union)) == 0:
            continue
        if check_digits_unique (int(str_union)) == 0:
            continue
        if check_for_all_digits (a, b, a * b) == 1:
            pandigit_prod_list.append(a*b)

# Check 2 digit x 3 digit numbers

for a in range(12, 98):
    if check_for_zeroes (a) == 0:
        continue
    if check_digits_unique (a) == 0:
        continue
    for b in range(123, 10000/a):

        str_union = str(a) + str(b)
        if check_for_zeroes (int(str_union)) == 0:
            continue
        if check_digits_unique (int(str_union)) == 0:
            continue
        if check_for_all_digits (a, b, a*b) == 1:
            pandigit_prod_list.append(a*b)

unique_pan_list = list(set(pandigit_prod_list))
print sum (unique_pan_list)
