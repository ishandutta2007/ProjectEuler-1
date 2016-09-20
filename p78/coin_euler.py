# coin_euler.py
# Find the lowest number such that its number of partitions is
# divisible by 1 MM

import time

def pentagonal_nums (i):
    return i * (3 * i - 1) / 2.0

def calc_partition_val (num, partition_dict, div_num):

    rad = 24 * num + 1
    beg_val, end_val = (1 - rad ** 0.5) / 6.0, (1 + rad ** 0.5) / 6.0

    sum = 0
    for k in range (int(beg_val), int(end_val)+1, 1):
        if k == 0:
            continue
        sum = (sum + partition_dict[num - pentagonal_nums (k)]
               * ((-1) ** (k-1))) % div_num

    partition_dict[num] = sum
    
    return partition_dict
    
def main():

    start_time = time.time()
    partition_dict = {}

    div_num = 10 ** 6
    
    partition_dict[0] = 1
    for i in range(1,4):
        partition_dict[i] = i
        
    i = 3
    while partition_dict[i] % div_num != 0:
        i += 1
        partition_dict = calc_partition_val (i, partition_dict, div_num)
            
    print i, partition_dict[i]
    print time.time() - start_time

main()
