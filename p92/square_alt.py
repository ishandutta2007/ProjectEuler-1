# square_alt.py
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

        next_num = calc_sum_digit_square (next_num)
        
    if next_num == 89:
        return 1
    return 0

max_num = 10000000
chain_count = 0
num_dict = {}


for i in xrange (1, max_num):

    if i > 601:
        if num_dict[calc_sum_digit_square(i)] == 89:
            chain_count += 1
            print i, chain_count
        continue
        
    val = calc_num_chain (i)

    if val == 1:
        num_dict[i] = 89
        chain_count += 1
        print i, chain_count
    else:
        num_dict[i] = 1
            


