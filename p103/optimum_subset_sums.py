# optimal_subset_sums.py

# Set Conditions:
# 1) Any two distinct subsets have different sums across all of their elements
# 2) If set A is larger than set B, then S(A) > S(B), S = sum across elts

# We are given a set of size 7 satisfying (1) and (2) with sum equal to 255
# Problem is to find satisfying 7 element sets with lower sums than this

# When looking at possible sets, the algo will view a set as the set of
# differences between each number and the lowest value in the list
# There are fewer conditions to check with this view, and we can pick
# an appropriate starting number if the set of differences is valid

import itertools, time
from copy import copy

# Determine the next valid value for the list greater than or equal to start_num
# Curr_num_list is in the form of differences between each number and the
# first value in the list
# Checks if pairs are equal, triples are equal, ... to determine if new value
# is valid
def next_valid_value (curr_num_list, start_num, max_num):

    if len(curr_num_list) == 0:
        return start_num
    
    next_num_index = len(curr_num_list) + 1
    if next_num_index == 2:
        last_num = curr_num_list[-1]
        if start_num > last_num:
            return start_num
        else:
            return last_num + 1
        
    # Now, go through testing until finding a valid one
    test_num = start_num
    curr_num_set = set(curr_num_list)

    curr_num_set.add(0)  # Makes checking easier by including this

    # Could add testing for test_num to make sure that it's not in simple sets
    # before doing larger testing
    while test_num < max_num:
        flag_break = 0
        # Adding one to range indices below because we added zero to the set
        for set_num in range(4, next_num_index+2, 2):
            curr_num_set.add(test_num)
            comp_set_size = set_num / 2
            
            # list of sets of size comp_set_size
            set_list = list(map(set, list(itertools.combinations
                                        (curr_num_set, comp_set_size))))

            num_sets = len(set_list)
            sum_list = map(sum, set_list)

            if len(set(sum_list)) < num_sets:  # means a sum repeats
                flag_break = 1
                break
        if flag_break == 0:
            return test_num
        else:
            curr_num_set.remove(test_num)
            test_num += 1
    return 0
#------------------------------------------------------------------------------

# Given an incomplete number list, this calculates the maximum possible
# value of the next number in the list
# It does this by checking the current maximum sum for the whole list
# and ensuring that the set conditions hold
def determine_max_value (curr_num_list, curr_max_sum, total_nums,
                         min_first_val, max_first_val):
    
    curr_num_len = len(curr_num_list)
    if curr_num_len == total_nums - 1:
        print "No more numbers to add"
        return 0
    
    # Lowest possible sum is if all numbers are consecutive
    # This is not actually possible, but does leave a conservative estimate
    if curr_num_len == 0:
        max_val = (curr_max_sum - total_nums * min_first_val -
                   ((total_nums-1)*(total_nums-2))/2) / (total_nums - 1)
        return max_val
    
    curr_total = sum (curr_num_list)
    remaining_nums = total_nums - curr_num_len - 1
    
    # Assumes initial val = 10, all values going forward are consecutive
    # Calculates the maximum value that will keep the total sum less than
    # curr_max_sum
    max_val = (curr_max_sum - total_nums * min_first_val - curr_total -
                   ((remaining_nums-1)*(remaining_nums-2))/2) / remaining_nums

    # Derive potentially better estimate of max_first_val by checking total
    test_num_list = copy(curr_num_list)
    while len(test_num_list) < total_nums - 1:
        test_num_list.append(test_num_list[-1]+1)

    max_first_val = min(max_first_val, (curr_max_sum - sum(test_num_list)) /
                        total_nums)
        
    return min(max_val, max_value_conditions  (curr_num_list, curr_max_sum,
                                               total_nums, max_first_val))

def max_value_conditions (curr_num_list, curr_max_sum, total_nums,
                          max_initial_value):

    # We'll assume that all remaining numbers are consecutive
    # This is the most conservative assumption for ensuring that
    # the smallest triple is bigger than biggest pair, ...

    curr_num_len = len(curr_num_list)
    remaining_num_len = total_nums - curr_num_len - 1

    full_num_list = [linear_var(0,x) for x in curr_num_list] # real numbers
    i = 0
    while len(full_num_list) < total_nums - 1:
        full_num_list.append(linear_var(1, i)) # x + i, where x is the var
        i += 1

    # will compare the first comp_num and final comp_num elements
    # to relate x to our initial value
    comp_num = (total_nums - 1) / 2

    initial_elts_sum = sum(full_num_list[:comp_num])
    final_elts_sum = sum(full_num_list[-1*comp_num:])

    # This will be in the form ax + b, where a is positive
    # This must be smaller than the initial value of our list
    # for the sum of the first comp_num + 1 elts to be greater than the
    # last comp_num elts
    # We use the value for max_initial_value to derive a relationship
    # for x
    diff_elts = final_elts_sum - initial_elts_sum
    max_val = (max_initial_value - diff_elts.b) / diff_elts.a
    return max_val

# Linear variable, where (3,2) represents 3x + 2
# We'll use this class to solve for the maximum possible x
class linear_var:
    def  __init__ (self, a, b):
        self.a = a
        self.b = b
        self.val = (a,b)
    def __add__ (self, other):
        a_new = self.a + other.a
        b_new = self.b + other.b
        return linear_var (a_new, b_new)
    def __radd__ (self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__ (self, other):
        a_new, b_new = self.a - other.a, self.b - other.b
        return linear_var (a_new, b_new)

#------------------------------------------------------------------------------

# Recursive function that calls itself for each additional element to the
# test list
def find_optimum_set (total_nums, min_first_val, max_first_val, curr_max_sum,
                      curr_num_list, curr_best_list):
    # Base case
    if len(curr_num_list) == total_nums - 1:
        init_val = smallest_initial_val (curr_num_list)
        return [init_val] + map(lambda x: x + init_val, curr_num_list)

    if len(curr_num_list) == 0:
        init_num = 1
    else:
        init_num = curr_num_list[-1] + 1
        
    max_num = determine_max_value (curr_num_list, curr_max_sum, total_nums,
                         min_first_val, max_first_val)

    i = init_num
    new_best_list = copy (curr_best_list)
    i = next_valid_value (curr_num_list, i, max_num)
    
    while i <= max_num and i != 0:
        test_num_list = copy(curr_num_list)

        test_num_list.append(i)
        
        result = find_optimum_set (total_nums, min_first_val, max_first_val,
                                   curr_max_sum, test_num_list,
                                   new_best_list)        
        if result != 0:
            if sum(result) < curr_max_sum:
                curr_max_sum = sum(result)
                new_best_list = copy(result)
                
        i = next_valid_value (curr_num_list, i+1, max_num)
        
    return new_best_list

# Called by above function when valid set is identified. It finds the
# smallest initial value for that set to be valid
def smallest_initial_val (curr_num_list):
    comp_list = len(curr_num_list) / 2
    
    max_val = (sum(curr_num_list[-1*comp_list:]) -
               sum(curr_num_list[:comp_list]))
    return (max_val + 1)
#-----------------------------------------------------------------------------

def main():
    start_time = time.time()
    curr_best_list = [20, 31, 38, 39, 40, 42, 45] # given in question
    curr_max_sum = sum (curr_best_list)

    # Min value is to ensure that the sum of the last 3 terms is less than
    # the first four's sum.
    # Max value is determined by the curr_max_sum
    min_first_val, max_first_val = 10, 34
    total_nums = len(curr_best_list)

    print find_optimum_set (total_nums, min_first_val, max_first_val,
                            curr_max_sum, [], curr_best_list)    
    
    print time.time() - start_time
    
main()
