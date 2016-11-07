# darts.py
# To checkout in darts is to achieve your target, ending with a double
# number of some sort
# Determine number of ways to checkout with sum under 100

# Will produce all possible checkouts, and count the ones that sum to below
# 100

import itertools, time

def produce_throw_list (min_num_throw, max_num_throw, bullseye):

    valid_num_throws = range(min_num_throw, max_num_throw+1) + [bullseye]
    end_throws = [('D', str(i)) for i in valid_num_throws]

    multiples = ['S', 'D', 'T']
    all_throws = list(itertools.product (multiples, map(str, valid_num_throws)))
    all_throws.remove(('T', '25')) # no triple bullseye
    all_throws.append(('S', '0'))         # Represents a miss (or unneeded turn)
    return all_throws, end_throws

# First, produce all valid ways (as values) first two darts can be thrown
# Then count the number of valid end throws for each of those ways
# Adding them all up will yield the answer
def produce_valid_checkouts (throw_list, end_throws, max_num,
                             max_num_throw, bullseye):

    all_pair_throws = []
    for i in range(len(throw_list)):
        for j in range(i, len(throw_list)):
            all_pair_throws.append(map_tuple_value(throw_list[i]) +
                                   map_tuple_value(throw_list[j]))

    end_throw_vals = [map_tuple_value(end_throw) for end_throw in end_throws]

    valid_checkout_count = 0
    for throw in all_pair_throws:
        if throw > max_num - 1 - 2: # no valid end throw for these
            continue
        num_possible_end_throws = (max_num - 1 - throw) / 2
        if num_possible_end_throws <= max_num_throw:
            valid_end_throws = num_possible_end_throws
        elif num_possible_end_throws < bullseye:
            valid_end_throws = max_num_throw
        else:
            valid_end_throws = max_num_throw + 1
        valid_checkout_count += valid_end_throws

    return valid_checkout_count

    
    
# This takes an input like ('D', '18') and returns 2 * 18 = 36
def map_tuple_value (board_tuple):
    multiple_dict = {}
    multiple_dict['S'], multiple_dict['D'], multiple_dict['T'] = 1,2,3 
    multiple = board_tuple[0]
    val = int(board_tuple[1])
    return multiple_dict[multiple] * val
    
    

    
def main():
    start_time = time.time()
    max_num = 100
    min_num_throw, max_num_throw, bullseye = 1, 20, 25
    throw_list, end_throws = produce_throw_list (min_num_throw,
                                                 max_num_throw, bullseye)

    print produce_valid_checkouts (throw_list, end_throws, max_num,
                             max_num_throw, bullseye)
    print time.time() - start_time
main()                  
