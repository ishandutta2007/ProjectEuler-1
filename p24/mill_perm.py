# mill_perm.py
# Determine millionth permutation of range(10)

import math

def calc_list_index (perm_no, num_list):
    val_index = perm_no / math.factorial(len(num_list)-1)
    return val_index


init_perm_num = 1000000
num_options = range(10)
perm_answer = []
perm_num = init_perm_num - 1

for i in range(len(num_options)-1, 0, -1):
    
    val_index = calc_list_index (perm_num, num_options)
    ith_perm_digit = num_options[val_index]
    perm_answer.append (str(ith_perm_digit))
    num_options.remove(ith_perm_digit)
    perm_num -= (val_index * math.factorial(i))

perm_answer += str(num_options[0])
print perm_answer
