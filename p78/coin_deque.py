# coin_deque.py
# Find the lowest number such that its number of partitions is
# divisible by 1 MM

import time
from collections import deque

# takes all the pairs which sum to num
# adds them appropriately to the dictionary
def calc_all_pairs (partition_list, num):
    
    for i in xrange (1, num/2 + 1):
        partition_list.append(1)
    return partition_list

# Calculates all partitions for num, divided by the lowest summand
# Function assumes that all values lower than num are already present
# Dict[num, k] is how many partitions have all summands greater than or equal k

def calc_partition_nums (partition_list, num, div_num):

  
    new_num_list = []
    
    new_num_list = calc_all_pairs (new_num_list, num)

    for i in xrange (1, num/3+1):
       
        new_num_list[i-1] += (partition_list[-i].popleft() % div_num)
        
        if len (partition_list[-i]) == 0:
            del partition_list[-i]
        
    for i in xrange (num/2 - 1, 0, -1):
        new_num_list[i-1] = (new_num_list[i-1] +
                                    new_num_list[i]) % div_num

    partition_list.append (deque (new_num_list))
            
    return partition_list
    

def main():

    start_time = time.time()
    partition_list = []

    div_num = 10 ** 6
    i = 1
    partition_list.append([])
    partition_list.append ([1])
    
    
    while (partition_list[-1][0]+1) % div_num != 0:
        i += 1
        calc_partition_nums (partition_list, i, div_num)
        
        if i  % 2500 == 0:
            print i, partition_list[-1][0]+1
        
    print i, (partition_list[-1][0]+1)

    print time.time() - start_time

main()
