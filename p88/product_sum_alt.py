# product_sum_alt.py
# For each number k, find the smallest set of size k such that the
# sum of the numbers equals its product
# Small is determined by the sum calculated this way
from copy import copy, deepcopy
from math import log

import sys, os, inspect, time


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve


def calc_prime_factorization (sieve_list, max_num):
    import operator
    
    prime_factor_dict = {}
    for i in xrange(2, max_num+1):
        prime_factor_dict[i] = []
        if sieve_list[i] == 0:
            prime_factor_dict[i].append((i,1))  # prime number
        else:
            factor_list = sieve_list[i][1]
            for factor in factor_list:
                j = 1
                while i % (factor ** j) == 0:
                    j += 1
                prime_factor_dict[i].append ((factor, j-1))
        prime_factor_dict[i].sort (key = operator.itemgetter(1))
        
    return prime_factor_dict


def add_val_tuple (val, tuple_list):
    from collections import deque
    
    master_list = []
    for test_tuple in tuple_list:
        new_list = deque([test_tuple[i] for i in range(len(test_tuple))])
        new_list.appendleft(val)
        master_list.append (tuple (new_list))
    return master_list


# This yields a dictionary containing all the partitions for all integers
# up to max_num
# We'll use these to determine all possible factor breakdowns for numbers N
def calc_partitions (max_num):
    part_dict = {}
    part_dict[2,1] = [(1,1)]
    part_dict[3,1] = [(1,2), (1,1,1)]

    for i in range (4, max_num+1):
        # add in the pairs
        for j in range(1, i/2+1):
            part_dict[i, j] = [(j, i-j)]
        # add in others
        for j in range(1, i/3+1):
            for k in range (j, (i-j)/2 + 1):
                part_dict[i,j] += add_val_tuple (j, part_dict[i-j,k])

    final_dict = {}
    for i in range(2, max_num+1):
        final_dict[i] = []
        for j in range (1, i/2+1):
            final_dict[i] += part_dict[i, j]
    return final_dict

# Yields all ways to allocate the factor partition into the master partition
def allocate_factors_partition (master_partition, factor_list, freq_dict, master_list,
                                latest_index = 0, prev_factor = 0):
    import operator
    from collections import Counter
    
    # Base case
    if factor_list[0] == factor_list[-1]: # fill in all remaining slots with last factor
        last_list = deepcopy (master_list)
        for i in range(len(last_list)):
            
            if len(last_list[i]) == master_partition[i]:
                continue
            else:
                rem_nums = master_partition[i] - len(last_list[i])
                last_list[i] += [factor_list[0]] * rem_nums
                
        ret_list = []
        for sample in last_list:
            ret_list.append (reduce (operator.mul, sample))
        return [ret_list]
    
    # Generally, allocate the first factor to wherever it can be allocated
    if prev_factor == factor_list[0]:
        if len(master_list[latest_index]) < master_partition[latest_index]:
            min_index = latest_index
        else:
            min_index = latest_index + 1
    else:
        min_index = 0

     # Making sure enough space remaining for all copies of this factor
     
    remaining_curr_factor = freq_dict[factor_list[0]]
                                                    
    remaining_slots = 0
    i = len(master_list) - 1
    while remaining_slots < remaining_curr_factor:
        remaining_slots += (master_partition[i] - len(master_list[i]))
        max_index = i
        i -= 1
        
    product_list = []

    for test_index in range(min_index, max_index+1):
        final_list = deepcopy(master_list)

        if len(final_list[test_index]) < master_partition[test_index]:
            if test_index > 0 and master_partition[test_index] == master_partition[test_index-1]:
                if len(final_list[test_index-1]) < master_partition[test_index-1]:
                    near_count = Counter(final_list[test_index])
                    past_count = Counter(final_list[test_index-1])
                    if near_count[factor_list[0]] >= past_count[factor_list[0]]:
                        if final_list[test_index] == final_list[test_index-1]:
                            continue

            final_list[test_index].append (factor_list[0])
            new_freq_dict = copy (freq_dict)
            new_freq_dict[factor_list[0]] -= 1

            product_list +=  allocate_factors_partition (master_partition, factor_list[1:],
                                                         new_freq_dict, final_list, test_index,
                                                         factor_list[0])

    return product_list
        
# This will calculate all the possible integer terms whose product will
# equal N
# It will calculate the k associated with that N, and add it to the
# dictionary if minimal
def calc_N_products (min_num, max_num, prime_factor_dict, partition_dict):
    
    k_dict = {i:2*i for i in range(min_num, 2 * max_num+1)}

    for N in xrange (min_num, 2 * max_num+1):

        factor_list = prime_factor_dict[N]
        long_factor_list = []
        for factor in factor_list:
            long_factor_list += [factor[0]]*factor[1]
        freq_dict = {x[0]: x[1] for x in factor_list}
        if len(factor_list) == 1 and factor_list[0][1] == 1: # prime
            continue
        num_factors = sum(map (lambda x:x[1], factor_list))
        rel_partitions = partition_dict[num_factors]
        total_list = []
        for partition in rel_partitions:
            init_list = []
            for i in range(len(partition)):
                init_list.append([])

            partition_list = allocate_factors_partition (partition, long_factor_list,
                                                      freq_dict, init_list)
            # print partition_list
            for prod in partition_list:
                k = N - sum(prod) + len(prod)
                k_dict[k] = min(k_dict[k], N)

    return k_dict
        

def main():
    start_time = time.time()
    N_list = []
    min_num = 2
    max_num = 12000
    partition_num = int(log (2 * max_num) / log(2))
    prime_list, sieve_list = gen_co_prime_sieve (2 * max_num)
    prime_factor_dict = calc_prime_factorization (sieve_list, 2 * max_num)

    partition_dict = calc_partitions (partition_num)

    k_dict = calc_N_products (min_num, max_num, prime_factor_dict, partition_dict)    
    N_list = [k_dict[i] for i in xrange(min_num, max_num+1)]
    print k_dict[max_num]
    print sum(set(N_list))
    
    print time.time() - start_time

main()
