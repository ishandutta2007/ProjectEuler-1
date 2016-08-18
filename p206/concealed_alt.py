# concealed_alt.py
# Find number whose square has 19 digits, with every other digit
# the numbers 1 through 9, 0

def check_digits (num, digit_dict):

    num_str = str(num)
    for key in digit_dict:
        if digit_dict[key] != int(num_str[key]):
            return 0
    return 1

def find_possible_a_b (possible_c):
    possible_list = []
    for c in possible_c:
        for a in range(10):
            for b in range(10):
                rel_sum = c*c + 20 * b * c + 100 * b * b + 200 * a * c
                rel_str = str(rel_sum)
                if len(rel_str) >= 3:
                    if rel_str[-1] == '9' and rel_str[-3] == '8':
                        possible_list.append (1000*a+100*b+10*c)
    return possible_list


digit_dict = {}
num_check_digits = 10
for i in range (1,num_check_digits+1):
    digit_dict[(2*i)-2] = (i % 10)

num_digits = 19
import sys

possible_c = [3,7]
possible_abc = find_possible_a_b (possible_c)


base = 1000000000
first_digit = 1
test = base
while test * test < (first_digit+1) * (10 ** (num_digits-1)):
    for num in possible_abc:
        test = base + num
        if check_digits (test * test, digit_dict) == 1:
            print test
            break
    base += 10000

