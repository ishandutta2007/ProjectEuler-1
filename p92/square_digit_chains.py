# square_digit_chains.py
# calculate sum of digit squares recursively until loop
# Find how many numbers loop at 89 under 10000

def calc_sum_digit_square (num):
    sum_sq = 0
    for dig in str(num):
        sum_sq += int(dig)*int(dig)
    return sum_sq

def calc_num_chain (num):
    num_list = []
    next_num = num
    while next_num != 89 and next_num != 1:
        num_list.append (next_num)
        next_num = calc_sum_digit_square (next_num)
    if next_num == 89:
        return 1
    return 0

max_num = 10000000
chain_count = 0
for i in xrange (1, max_num):
    if calc_num_chain (i) == 1:
        chain_count += 1
        print i, chain_count

