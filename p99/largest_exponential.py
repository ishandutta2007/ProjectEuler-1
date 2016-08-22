# largest_exponential.py
# Find greatest number among base raised to exponent pairs

from math import log

input_file = "base_exp.txt"
with open(input_file, 'r') as f:
    index = 1
    max_base = 1
    max_exp = 1
    tgt_index = 0
    for line in f:
        x1 = line.split(',')
        base = int(x1[0])
        exp = int(x1[1])
        if (exp * log(base)) > (max_exp * log(max_base)):
            max_base, max_exp = base, exp
            tgt_index = index
        index += 1

        
print tgt_index
