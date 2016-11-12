# counting_block_combinations.py
# A row measures 50 blocks long. Each red block is 2 blocks long,
# green is 3, and blue is 4. No black boxes (1) needed between blocks.
# Assuming access to only one color, how many ways are there to
# fill the row, with the condition that at least one colored block
# must be used


from collections import Counter
from math import factorial
import time

# Function will generate the partitions of n into exactly k summands
# with minimum number min_num
# The frequencies of each summand, and the occurrence of each frequency
# is what will be returned

def partition_n_k (n, k, min_num, curr_nums):
    if n < k * min_num:
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
        new_nums.append (n - sum(curr_nums))
        all_freq_list.append(partition_n_k (n, k, min_num, new_nums))
    else:
        if len(curr_nums) == 0:
            min_range = min_num
            max_range = n / k
        else:
            min_range = max(min_num, curr_nums[-1])
            max_range = (n - sum(curr_nums)) / remaining_nums

        for i in range(min_range, max_range+1):
            new_nums = curr_nums[:]
            new_nums.append(i)
            all_freq_list += partition_n_k (n, k, min_num, new_nums)

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

def count_block_combos (n, block_len):
    
    total_count = 0  # accounts for case of no red blocks

    max_num_color = n / block_len

    # num_color is the number of colored blocks
    # This will count the number of alignments for num_color colored blocks
    for num_color in range (1, max_num_color + 1):
        min_black_blocks = 0
        color_total = block_len * num_color

        free_black_blocks = n - color_total - min_black_blocks

        # black boxes b/w each color and on either side
        num_black_slots = num_color + 1

        # partitions of the free black blocks
        open_black_part = partition_n_k (free_black_blocks, num_black_slots,
                                         0, [])

        total_black_perm = sum([permutation_count(num_black_slots, part)
                                for part in open_black_part])
        total_count += total_black_perm

    return total_count

def main():
    start_time = time.time()
    n = 50
    red_block_len, green_block_len, blue_block_len = 2,3,4
    block_len_list = [red_block_len, green_block_len, blue_block_len]
    
    print sum([count_block_combos (n, block_len) for block_len in
               block_len_list])
    
    print time.time() - start_time
    
main()
