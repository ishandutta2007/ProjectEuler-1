# concealed_square.py
# Find number whose square has 19 digits, with every other digit
# the numbers 1 through 9, 0

def check_digits (num, digit_dict):

    num_str = str(num)
    for key in digit_dict:
        if digit_dict[key] != int(num_str[key]):
            return 0
    return 1


digit_dict = {}
num_check_digits = 10
for i in range (1,num_check_digits+1):
    digit_dict[(2*i)-2] = (i % 10)

num_digits = 19
import sys

test = 1000000030
diff = 40
first_digit = 1
while test * test < (first_digit+1) * (10 ** (num_digits-1)):
    if check_digits (test * test, digit_dict) == 1:
        print test
        break
    test += diff
    diff = 100 - diff
#    print test, "progress"

