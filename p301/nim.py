# nim.py
# Find all numbers n <= 2 ** 30 such that X(n, 2n, 3n) = 0
# where X is the Nim function meaning all moves lead to loss if zero


# This will count the integers
# such that there are no consecutive ones in their binary representation
# This should correspond to the integers satisfying the problem

def num_count_condition (num_digits, prev_digits = []):
    if num_digits == 1:
        if len(prev_digits) > 0:
            if prev_digits[-1] == 1:
                curr_digit = 0 # only option
                return 1
            if sum(prev_digits) == 0:
                curr_digit = 1
                return 1
            else:
                return 2  # could be zero or one
        return 1

    total_nums = 0
    max_digit = 1
    if len(prev_digits) > 0:
        if prev_digits[-1] == 1:
            curr_digit = 0
            total_nums += num_count_condition (num_digits-1, prev_digits + [curr_digit])

    if len(prev_digits) == 0 or prev_digits[-1] == 0:
        for curr_digit in range(max_digit+1):
            total_nums += num_count_condition (num_digits-1, prev_digits + [curr_digit])            

    return total_nums

print num_count_condition (30) + 1  # adding 1 b.c 2 ** 30 will not be included
