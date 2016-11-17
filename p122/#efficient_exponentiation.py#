# efficient_exponentiation.py
# Find the least number of multiplications required to arrive at n ** k
# starting with n * n. Sum across k = 1 to 200

import time, math
#------------------------------------------------------------------------------
# Fills dictionary with known least numbers for powers of 2 and sums of powers
# of 2. For example, 2 ** n can be produced with n multiplications.
# 2 ** n + 2 ** i must be produced in (n+1) as it cannot be done in n, but
# can be done in n + 1
def fill_dictionary (max_num):
    min_mult_dict = {}

    n = 0
    while (2 ** n <= max_num):
        min_mult_dict[2 ** n] = n

        for i in range (n):
            min_mult_dict[2**n + 2**i] = n + 1

        n += 1
    return min_mult_dict
#-------------------------------------------------------------------------------
# Calculates the least number of multiplications needed to generate the
# given target exponent.
# Recursive function that truncates choices if they exceed max_possible and
# ends the function if min_possible is located
def calc_efficient_process (target_exp, curr_exp_list, max_possible,
                                   curr_total, min_possible, round_num):
    # Base case
    if curr_total == target_exp:
        return round_num  # number of rounds

    if curr_total < target_exp and round_num == max_possible:
        return max_possible
    
    remaining_rounds = max_possible - round_num
    if curr_total * (2 ** remaining_rounds) <= target_exp:
        return max_possible

    efficient_num = max_possible
    curr_exp_set = list(set(curr_exp_list))
    for exp in curr_exp_set:
        new_exp_list = curr_exp_list[:]
        if curr_total + exp <= target_exp:
            new_exp_list.append(curr_total + exp)
            new_total = curr_total + exp
            efficient_num = min(efficient_num,
                                calc_efficient_process (target_exp, new_exp_list,
                                                        max_possible, new_total,
                                                        min_possible, round_num+1))
            if efficient_num == min_possible:
                break
            max_possible = efficient_num
            
    return efficient_num

def max_possible_rounds (num, min_mult_dict):
    max_rounds = min_mult_dict[num-1] + 1
    if num % 2 == 0:
        possible_max_rounds = min_mult_dict[num/2] + 1
    else:
        possible_max_rounds = min_mult_dict[(num-1)/2] + 2
    return min(max_rounds, possible_max_rounds)

    
def main():
    start_time = time.time()
    min_num, max_num = 1, 200
    min_mult_dict = fill_dictionary (max_num)
    total_sum = 0
    for i in range(min_num, max_num + 1):
        if i in min_mult_dict:
            total_sum += min_mult_dict[i]
        else:
            max_possible = max_possible_rounds (i, min_mult_dict)

            # After i rounds, highest number possible is 2 ** i. So if num is
            # between 2 ** i and 2 ** (i+1) min possible is (i+1)
            min_possible = int (math.log(i) / math.log(2)) + 2

            if max_possible == min_possible:
                min_mult_dict[i] = min_possible
            else:
                min_mult_dict[i] = calc_efficient_process (i, [1,2], max_possible, 2,
                                                 min_possible, 1)
            total_sum += min_mult_dict[i]

    print total_sum
    print time.time() - start_time
    
main()
