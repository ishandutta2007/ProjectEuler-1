# Find the 30th number that is the an integral power of the sum of its digits

import math, time

#------------------------------------------------------------------------------
# Determines all the numbers that are powers of digit sums
# that have exactly num_digits digits
def digit_power_check (num_digits):

    min_num = 10 ** (num_digits - 1)
    max_num = (10 ** num_digits) - 1

    # This is derived by noting that the smallest digit sum is n
    # and the largest number must be smaller than 10 ** n
    max_exponent = int((num_digits / math.log (num_digits)) * math.log(10))

    min_exponent = ((num_digits - 1) * math.log(10)) / (math.log(9 * num_digits))
    min_exponent = max (2, int(min_exponent) + 1)

    # Make a list of all squares, cubes, ... and check if they satisfy condition
    target_list = []
    for exponent in range(min_exponent, max_exponent + 1):
        
        base_min = min_num ** (1.0/exponent)
        if int(base_min) != base_min:
            base_min = int(base_min) + 1
        base_max = max_num ** (1.0/exponent)
        if int(base_max) != base_max:
            base_max = int(base_max)
        base_min, base_max = int(base_min), int(base_max)

        for base in range (base_min, base_max + 1):
            test_power = base ** exponent
            if base == digit_sum (test_power):
                target_list.append (test_power)
                
    if len(target_list) > 1:
        return sorted(target_list)
    return target_list

# Returns sum of digits of inputted number
def digit_sum (num):
    num_str = list(str(num))
    digit_list = [int(i) for i in num_str]
    return sum(digit_list)
#------------------------------------------------------------------------------

def main():
    start_time = time.time()
    target_index = 30

    digit_num = 2
    target_list = []

    while len (target_list) < target_index:

        target_list += digit_power_check (digit_num)
        digit_num += 1
        
    print target_list[target_index - 1]
    print time.time() - start_time
    
main()
