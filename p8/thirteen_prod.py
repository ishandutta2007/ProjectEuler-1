# thirteen_prod.py
from operator import mul

filename = "thousand_digit_number.txt"
digit_list = []
max_size = 13
running_prod = 1
max_prod = 1

# check if actually a digit
min_char = '0'
max_char = '9'
zero_presence = [0,0]


with open (filename) as f:
    while True:
        c = f.read(1)
        if c >= min_char and c <= max_char:
            
            digit_list.append(int(c))
            if len (digit_list) > max_size:

                digit_list.pop(0)
                running_prod = reduce (mul, digit_list)
                max_prod = max(running_prod, max_prod)

            if len (digit_list) < max_size:
                running_prod *= digit_list[-1]        
            if len (digit_list) == max_size:
                running_prod = reduce (mul, digit_list)
                max_prod = max(running_prod, max_prod)
        if not c:
            break

print max_prod
