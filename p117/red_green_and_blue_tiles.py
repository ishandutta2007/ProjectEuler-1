# red_green_and_blue_tiles.py
# A row measures 50 blocks long. Each red block is 2 blocks long, each
# green is 3, blue is 4, and black is 1.
# How many ways can the row be filled with assuming at least
# one colored block?


from collections import Counter
from math import factorial
import time

# Function will generate the partitions of n into exactly k summands
# with minimum number min_num
# The frequencies of each summand, and the occurrence of each frequency
# is what will be returned

def partition_n_k (n, k, min_num, max_num, curr_nums):
    
    if n < k * min_num or n > k * max_num:
        return []
    
    # Base case - returns the frequencies and the number of times each frequency
    # occurs
    if len(curr_nums) == k:
    
        counter = Counter(curr_nums)
        freq_table = counter.most_common()
        freq_set = set([])
        freq_list = [[i,0] for i in range(k+1)]
        for freq_pair in freq_table:
            freq = freq_pair[1]
            freq_list[freq][1] += 1
        final_freq_list = [tuple(freq) for freq in freq_list if freq[1] != 0]

        return final_freq_list

    all_freq_list = []
    
    remaining_nums = k - len(curr_nums)
    
    # Penultimate case    
    if remaining_nums == 1:
        new_nums = curr_nums[:]
        if n - sum(curr_nums) >= min_num and n - sum(curr_nums) <= max_num:
            new_nums.append (n - sum(curr_nums))
            all_freq_list.append(partition_n_k (n, k, min_num, max_num,
                                                new_nums))
    else:
        if len(curr_nums) == 0:
            min_range = max (n - (remaining_nums-1)*max_num, min_num)
            max_range = min(n / k, max_num)
        else:
            min_range = max(min_num, curr_nums[-1], n - sum(curr_nums) -
                            (remaining_nums-1)*max_num)
                            
            max_range = min(max_num, (n - sum(curr_nums)) / remaining_nums)

        for i in range(min_range, max_range+1):
            new_nums = curr_nums[:]
            new_nums.append(i)
            all_freq_list += partition_n_k (n, k, min_num, max_num, new_nums)

    return all_freq_list

# freq_list is a list of tuples listing frequency and num of occurrences of
# that frequency
def permutation_count (n, freq_list):

    numer = factorial(n)
    denom = 1
    for freq in freq_list:
        # frequency factorial to the power of num_frequency
        frequency, num_freq = freq[0], freq[1]
        denom *= (factorial(frequency) ** num_freq)
    return numer / denom

def count_block_combos (n, block_len_list):
    
    total_count = 1  # accounts for case of no red blocks

    max_num_color = n / min(block_len_list)

    # num_red is the number of red blocks
    # This will count the number of alignments for num_red red blocks
    for num_color in range (1, max_num_color + 1):
        min_black_blocks = 0
        min_color_total = num_color * min(block_len_list)
        max_color_total = num_color * max(block_len_list)

        for color_total in range(min_color_total, max_color_total + 1):
            
            free_black_blocks = n - color_total - min_black_blocks
            
            # black boxes b/w each color and on either side
            num_black_slots = num_color + 1

            # partitions of the free black blocks
            open_black_part = partition_n_k (free_black_blocks, num_black_slots,
                                             0, free_black_blocks, [])
            
            total_black_perm = sum([permutation_count(num_black_slots, part)
                                    for part in open_black_part])
            
            for color_part in partition_n_k (color_total, num_color,
                                             min(block_len_list),
                                             max(block_len_list), []):
                
                total_count += (permutation_count (num_color, color_part) *
                                total_black_perm)
                
    return total_count

def main():
    start_time = time.time()
    n = 50
    red_block_len, green_block_len, blue_block_len = 2, 3, 4

    block_len_list = [red_block_len, green_block_len, blue_block_len]
    
    print count_block_combos (n, block_len_list)
    print time.time() - start_time
    
main()
