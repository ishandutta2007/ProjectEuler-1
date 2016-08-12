# thirteen_alt.py
# Check for zeroes before calculating product

from operator import mul

filename = "thousand_digit_number.txt"
digit_list = []
max_size = 13
running_prod = 1
max_prod = 1

# check if actually a digit
min_char = '0'
max_char = '9'
num_zeroes = 0


with open (filename) as f:
    while True:
        c = f.read(1)
        if c >= min_char and c <= max_char:
            
            digit_list.append(int(c))
            if digit_list[-1] == 0:
                num_zeroes += 1
            if len (digit_list) > max_size:
                if digit_list[0] == 0:
                    num_zeroes = num_zeroes - 1
                digit_list.pop(0)
                if num_zeroes == 0:
                    
                    running_prod = reduce (mul, digit_list)
                    max_prod = max(running_prod, max_prod)

            if len (digit_list) < max_size:
                running_prod *= digit_list[-1]        
            if len (digit_list) == max_size:
                if num_zeroes == 0:
                    running_prod = reduce (mul, digit_list)
                    max_prod = max(running_prod, max_prod)
        if not c:
            break

print max_prod
