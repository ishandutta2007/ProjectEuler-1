# For special subset sums of size n = 12, determine the number
# of comparisons that need to be made between subsets to check
# if the set satisfies condition that no disjoint subset yields the
# same sum. We are assuming that the set has distinct elements, and
# that given two subsets of different size, the larger set has the
# greater sum

# Constructs and evaluates comparisons between all subsets of the same size
# Size varies from 2 to n/2. If one set's members are all component-wise greater than the
# other set's members, it need not be compared
import itertools, sys, time

# For total set of size n, compares pairs of same-sized subsets, from size 2 to n/2
# If one subset's elements are all greater than its corresponding element in the other
# subset, then it need not be compared. This returns the total number of sets that
# need to be compared
def necessary_comp_sets (n):
    
    comp_size_range = range(2, n/2+1)
    possible_set_members = set(range(1, n+1))
    necessary_sum_total = 0

    for sub_size in comp_size_range:
        # Generate comparison sets such that the first set has the lowest
        # number. This avoids double counts
        for i in range(1, n - sub_size - (sub_size-1) + 1):
            remaining_nums =  set(range(i+1, n+1))
            for rem_subset in itertools.combinations (remaining_nums, sub_size-1):
                comp_set1 = [i] + list(rem_subset)

                comp2_subset_members = set(range(i+1, n+1)) - set(comp_set1)

                if len(comp2_subset_members) < sub_size:
                    continue
                for comp_set2 in itertools.combinations (comp2_subset_members, sub_size):
                    necessary_sum_total +=  compare_subsets(comp_set1, list(comp_set2))

    return necessary_sum_total

# Check if the 2 inputted subsets need to be calculated or not
# If one member's sorted elements are all greater than the others, then there is
# no need for calculation (and returns 0). Returns 1 otherwise
def compare_subsets(sub1, sub2):
    check_sum = sum(map(lambda x: (x[0]<x[1]), zip(sorted(sub1), sorted(sub2))))
    if check_sum != len(sub1) and check_sum != 0:   
        return 1
    return 0

def main():
    start_time = time.time()
    n = 12
    print necessary_comp_sets (n)
    print time.time() - start_time
main()
