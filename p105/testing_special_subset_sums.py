# testing_special_subset_sums.py
# Take a list of sets from file, and determine if they satisfy certain
# set criteria (i) disjoint subsets have unique sums and (ii) if a subset is
# larger than another subset, then its sum must be greater than the other's

# Our program will solve this by looking at the differences of each set elt
# from the first element
# Make sure that all subsets of the same size do not have equal sums
# Then find the minimum initial value to ensure criteria (ii), and check
# if this set's minimum is above that value

# Note that a lot of this code is taken from the p103 solution

import itertools, sys, time


# Checking all pairs, triplets, ... up to total_nums/2
# All sets of same size must have distinct sums, otherwise
# not a valid set
# Curr_num_set is a set of differences from the lowest element in the set
def disjoint_subset_sums (curr_num_list):

    curr_num_set = set(curr_num_list)    
    curr_num_set.add(0)  # Makes checking easier by including this

    total_nums = len(curr_num_set)
    
    flag_break = 0
    for set_num in range(4, total_nums+1, 2):

        comp_set_size = set_num / 2

        # list of sets of size comp_set_size
        set_list = list(map(set, list(itertools.combinations
                                    (curr_num_set, comp_set_size))))

        num_sets = len(set_list)
        sum_list = map(sum, set_list)

        if len(set(sum_list)) < num_sets:  # means a sum repeats
            flag_break = 1
            return 0
    return 1
#------------------------------------------------------------------------------

# Called by above function when valid set is identified.
# The input is the difference set, not the actual set
# It finds the smallest initial value for that set to be valid
def smallest_initial_val (curr_num_list):
    comp_list = len(curr_num_list) / 2
    
    max_val = (sum(curr_num_list[-1*comp_list:]) -
               sum(curr_num_list[:comp_list]))
    return (max_val + 1)

#------------------------------------------------------------------------------

# Takes a list of numbers, returns a sorted list of each element's difference
# from the lowest element in the list
def calc_difference_list (num_list):
    num_list = sorted(num_list)
    diff_list = [(num_list[i] - num_list[0]) for i in range(1, len(num_list))]

    return diff_list, num_list[0]
#-----------------------------------------------------------------------------

# Reads in list of numbers from the file inputted
# Outputs a list of lists of these numbers
def get_num_lists (filename):
    input_num_lists = []
    
    with open(filename, 'r') as f:
        for line in f:
            x1 = line.split(',')
            x_int = map(int, x1)
            input_num_lists.append(x_int)
    return input_num_lists
#------------------------------------------------------------------------------

def main():
    start_time = time.time()
    filename = "sets.txt"
    input_num_lists = get_num_lists (filename)
    subset_sum = 0
    for num_list in input_num_lists:
        diff_list, initial_elt = calc_difference_list (num_list)

        if disjoint_subset_sums (diff_list) == 1:
            if smallest_initial_val (diff_list) <= initial_elt:
                subset_sum += sum(num_list)
    print subset_sum
    print time.time() - start_time
main()
            
