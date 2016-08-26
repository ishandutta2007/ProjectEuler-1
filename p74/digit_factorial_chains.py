# digit_factorial_chains.py
# Digit factorial sums produce repeating chains of numbers
# Longest chain below 1 MM has 60 elements, count how many numbers
# yield chains of that length

from math import factorial
from itertools import permutations
# for any number, outputs a list of its digits
def digit_list (num):
    test_list = list(str(num))
    num_list = []
    for ch in test_list:
        num_list.append(int(ch))
    return num_list

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

max_num = 10 ** 6
max_chain = 60
max_chain_count = 0
chain_dict = {}


for i in xrange (1, max_num):
    if calc_chain_length (i, chain_dict) == max_chain:
        max_chain_count += 1
        print i
print max_chain_count
