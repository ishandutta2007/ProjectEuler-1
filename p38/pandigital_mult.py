# pandigital_mult.py
# find all combinations whereby some number n x (1,2,3,...k)
# generates all the digits 1-9 uniquely
# 9 x (1,2,3,4,5) is an example (9,18,27,36,45)

# digits generated from the product of 2 numbers
def digits_from_product (x,y):
    prod = x * y
    digit_list = []
    for ch in str(prod):
        digit_list.append(ch)
    return digit_list

def test_pandigital (num):
    digit_list = []
    i = 1
    while len(digit_list) < 9:
        new_dig_list =  digits_from_product (i, num)
        if '0' in new_dig_list:
            return 0
        if len(set(new_dig_list)) != len(new_dig_list): # are all unique
            return 0
        if len(set(digit_list).intersection(new_dig_list)) != 0:
            return 0
        digit_list += new_dig_list
        i += 1
    return int(''.join(digit_list))



two_dig_range = range(91,100)
three_dig_range = range(918, 988)
four_dig_range = range (9182, 9877)
max_pandigital = 0

# for i in (two_dig_range + three_dig_range + four_dig_range):
for i in range (1, 9999):
    max_pandigital = max(max_pandigital, test_pandigital(i))

print max_pandigital
