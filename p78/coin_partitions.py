# coin_partitions.py
# Find the lowest number such that its number of partitions is
# divisible by 1 MM

import time

# takes all the pairs which sum to num
# adds them appropriately to the dictionary
def calc_all_pairs (partition_dict, num):

    for i in xrange (1, num/2 + 1):
        partition_dict[num, i] = 1
    return partition_dict

# Calculates all partitions for num, divided by the lowest summand
# Function assumes that all values lower than num are already present
# Dict[num, k] is how many partitions have all summands greater than or equal k

def calc_partition_nums (partition_dict, num, div_num):

    partition_dict[num, 0] = 1  # can partition into one pile of num

    partition_dict = calc_all_pairs (partition_dict, num)

    for i in xrange (1, num/3+1):
        partition_dict[num, i] += (partition_dict[num-i, i] % div_num)

    for i in xrange (num/2, 0, -1):
        partition_dict[num, i-1] += (partition_dict[num, i] % div_num)

    return partition_dict
    

def free_memory_dict (partition_dict, curr_index):

    curr_key_list = partition_dict.keys()

    new_dict = {k: partition_dict[k]
                for k in curr_key_list if k[0] >= (2.0 *curr_index/3) and 
                k[1] >= curr_index - k[0]}

    return new_dict


def main():

    start_time = time.time()
    partition_dict = {}

    div_num = 10 ** 5
    i = 1
    partition_dict[i,0] = 1
    
    while partition_dict[i, 0] % div_num != 0:
        i += 1
        calc_partition_nums (partition_dict, i, div_num)
        
        if i % 1000 == 0:
            print i
            new_dict = free_memory_dict (partition_dict, i)
            partition_dict = new_dict.copy()
            del new_dict
            print len (partition_dict.keys())
            
    print i, partition_dict[i,0]

    print time.time() - start_time

main()
