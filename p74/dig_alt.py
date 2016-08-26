# digit_alt.py
# Digit factorial sums produce repeating chains of numbers
# Longest chain below 1 MM has 60 elements, count how many numbers
# yield chains of that length

# Faster version of digit_factorial_sums.py
# If we find a number, we count all valid permutations of that number
# If the factorial sum of a number is less than that number, we return 0
# immediately

from math import factorial
from itertools import permutations

# for any number, outputs a list of its digits
def digit_list (num):
    test_list = list(str(num))
    num_list = []
    for ch in test_list:
        num_list.append(int(ch))
    return num_list

def check_digits_increasing (num):
    num_list = digit_list(num)
    if len(num_list) == 1:
        return 1
    
    if num_list[1] != 0:
        for i in range(len(num_list)-1):
            if num_list[i] > num_list[i+1]:
                return 0
    else:
        for i in range(2, len(num_list)-1):
            if num_list[i] > num_list[i+1]:
                return 0
    return 1
        

# For any list, outputs the sum of the factorials of each number in the list
def sum_factorials_nums (num_list):
    total = 0
    for num in num_list:
        total += factorial(num)
    return total

# Calculates the chain length until a number repeats
def calc_chain_length (num, chain_dict):
    chain_len = 1
    chain_list = []
    chain_list.append(num)
    next_num = sum_factorials_nums (digit_list (num))

    
    while next_num not in set(chain_list):
        if next_num in chain_dict:
            chain_len += chain_dict[next_num]

            return chain_len
        chain_len += 1
        chain_list.append (next_num)
        num = next_num
        next_num = sum_factorials_nums (digit_list (num))


    return chain_len

def gen_permutation_list (num):
    num_str = str(num)
    perm_list = permutations (num_str)
    final_list = list(int(''.join(num_perm)) for num_perm in perm_list)
    index = 0
    final_list.sort()
    # checks for zero as starting digit - want to eliminate these
    for num_test in final_list:
        if len(str(num_test)) < len(num_str):
            index += 1
        else:
            break
    return list(set(final_list[index:]))
        
max_num = 10 ** 6
max_chain = 60
max_chain_count = 0
chain_dict = {}


for i in xrange (1, max_num):
    if i in chain_dict:
        continue
    if check_digits_increasing(i) == 0:
        continue
    
    if calc_chain_length (i, chain_dict) == max_chain:
        perm_list = gen_permutation_list (i)
        for perm in perm_list:
            max_chain_count += 1
            chain_dict[perm] = 60

print max_chain_count
