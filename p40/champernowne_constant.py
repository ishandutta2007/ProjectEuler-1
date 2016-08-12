# champernowne_constant.py
# find specific digits of irrational 0.12345678910111213...
from operator import mul

i = 1
dig_index = 1 # tracks the digit number
curr_target = 1
max_index = 1000000
digit_list = []

while curr_target <= max_index:
    if dig_index >= curr_target:
        offset = dig_index - curr_target
        digit_list.append (int(str(i)[-1-offset]))
        curr_target *= 10
        
    i += 1
    dig_index += len(str(i))

print digit_list
print reduce (mul, digit_list)
