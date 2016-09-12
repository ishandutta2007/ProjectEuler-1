# magic_5_gon.py

from itertools import permutations
import time

# Function is given a range of 5 numbers, and the remaining 5 numbers
# out of the range 1-10
# The curr_nums form the inner circle of the n-gon
# This will search all permutations of the curr_nums, to see which can form
# a valid n-gon
def find_valid_gons (curr_nums):
    
    max_num = 10
    remaining_nums = range (1,max_num+1)
    for num in curr_nums:
        remaining_nums.remove(num)
    

    ngon_list = []
    
    possible_inner_circles = permutations (curr_nums)

    gon_size = len (curr_nums)
    print curr_nums
    for curr_sets in possible_inner_circles:
        
        line_list = [] # First, we'll create a list for each of the 5 lines of the n-gon
        sum_list = [] # sum of each line created
       
        index = 0
        for num in curr_sets:
            test_list = []
            test_list.append(curr_sets[index])
            if index == len(curr_sets) - 1:
                test_list.append (curr_sets[0])
            else:
                test_list.append (curr_sets[index+1])
            line_list.append (test_list)
            sum_list.append (sum(test_list))
            index += 1
            
        sort_sum_list = sorted(sum_list)
        sort_rem_list = sorted(remaining_nums)
        diff_list = [x-y for x,y in zip (sort_sum_list, sort_rem_list)]
        
        if len (set(diff_list)) == 1:  # all the same value, means valid ngon
            item_index = 0
            for total in sort_sum_list:
                test_index = sum_list.index (total)
                line_list[test_index] = [sort_rem_list[gon_size-1-item_index]] + line_list[test_index]
                item_index += 1
            
            # Finally, determine the number corresponding to the magic n-gon
            # test_index corresponds to the minimum value for the outer spoke of the n-gon

            n_gon_str = []
            for i in range (gon_size):
                for num in line_list[(test_index + i) % gon_size]:
                    n_gon_str.append (str(num))
            ngon_list.append(int(''.join(n_gon_str)))
            
    return ngon_list
            
def choose_inner_ring (curr_nums, remaining_nums, max_num, n_gon_size):

    max_gon = 0
    
    if len (curr_nums) == 0:

        remaining_nums = range (1, max_num+1)

    new_curr_nums = curr_nums[:]
    new_remaining_nums = remaining_nums[:]
    
    # base case
    if len (new_curr_nums) == n_gon_size - 1:

        remainder = 5 - sum(new_curr_nums) % n_gon_size
        post_remainder = remainder + n_gon_size

        if remainder not in set(new_remaining_nums) and post_remainder not in set(new_remaining_nums):
            return []
        
        final_list = []
        if remainder in set(remaining_nums):
            new_curr_nums.append (remainder)
            new_remaining_nums.remove (remainder)
            final_list = find_valid_gons (new_curr_nums)
            
            
        if post_remainder in set(remaining_nums):
            new_curr_nums, new_remaining_nums = curr_nums, remaining_nums
            new_curr_nums.append (post_remainder)
            new_remaining_nums.remove (post_remainder)
            final_list += find_valid_gons (new_curr_nums)
            
        return final_list
            
    final_list = []
    index_check = 0
    for j in new_remaining_nums[:-1*(n_gon_size - len(curr_nums))+1]:
       
        new_curr_nums = curr_nums[:]
        new_curr_nums.append(j)
        rem_nums = new_remaining_nums[index_check+1:]
      
        final_list += choose_inner_ring (new_curr_nums, rem_nums, max_num, n_gon_size)
        index_check += 1
        
    return final_list

def main():
    start_time = time.time()
    curr_nums = []
    remaining_nums = []
    max_num = 10
    n_gon_size = 5
    ngon_list = choose_inner_ring (curr_nums, remaining_nums, max_num, n_gon_size)

    print max (ngon_list), len (ngon_list)
    print set(ngon_list)
    print time.time() - start_time

main()
