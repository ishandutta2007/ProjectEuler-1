# monopoly_alt.py
# Calculate the odds of landing on any given monopoly square
# Final answer is concatenating the square numbers of the 3 most likely
# landing squares if using 2 4-sided dice

import sys

# This maps the square number (e.g. 00, 11, ...) to its square type on the board
def init_square_dict (filename):
    square_dict = {}
    
    with open (filename, 'r') as f:
        for line in f:
            x1 = (line.rstrip('\n')).split(',')
            square_dict[x1[0]] = x1[1]
    return square_dict

# This dictionary contains the squares that can cause movement to another square
# It will contain the new square and the odds of moving to that square, all
# contained in a list
def init_movement_dict (str_list, file_suffix):

    movement_dict = {}

    for sq_type in str_list:
        list1 = []
        if sq_type == "G2J":
            filename = sq_type + file_suffix
        else:
            filename = sq_type[:2] + file_suffix
            
        with open(filename, 'r') as f:
            for line in f:
                x1 = (line.rstrip()).split()
                list1.append((x1[0], float(x1[1]))) # (Square num, odds of move)
        f.close()
        
        movement_dict[sq_type] = list1
        
    return movement_dict

# Dictionary with odds of all possible dice rolls, assuming 2 dice
# with inputted number of sides dice_sides
def init_dice_odds_dict (dice_sides):
    min_roll = 2 * 1
    max_roll = 2 * dice_sides
    max_prob_roll = (min_roll + max_roll) / 2

    dice_odds_dict = {roll: (roll - 1.0) / (dice_sides ** 2)
                      for roll in range (min_roll, max_prob_roll+1)}

    for roll in range (max_prob_roll+1, max_roll+1):
        dice_odds_dict[roll] = dice_odds_dict[min_roll+max_roll - roll]
    
    return dice_odds_dict


def init_prob_doubles_dict (dice_sides):

    min_roll = 2 * 1
    max_roll = 2 * dice_sides
    prob_doubles_dict = {}
    
    for i in range (min_roll, max_roll, 2):
        if i in prob_doubles_dict:
            break
        prob_doubles_dict[i] = 1.0 / (i - 1)

        if min_roll + max_roll - i <= i:
            break
        
        prob_doubles_dict[min_roll + max_roll - i] = prob_doubles_dict[i]
    
    return prob_doubles_dict
    

def end_square (start_square, roll_num, num_total_squares):

    final_num_square = (int(start_square) + roll_num) % num_total_squares

    if final_num_square >= 10:
        return str(final_num_square)

    return ('0' + str(final_num_square))

def is_further_movement (sq_name, square_dict, inv_sq_dict, start_prob_dict,
                             movement_dict, init_prob, start_landing_dict = {},
                         start_landing  = 0, init_sq_num = 0, doubles_prob = 0):

    sq_num = inv_sq_dict[sq_name]
    
    if sq_name in movement_dict: 
        movement_list = movement_dict[sq_name]
        for action in movement_list:
            action_prob = init_prob * action[1]
            start_prob_dict[sq_num] -= action_prob # prob  of ending on sq_name
            if start_landing == 1:
                curr_prob, curr_doubles_prob = start_landing_dict[(init_sq_num, sq_num)]
                start_landing_dict[(init_sq_num, sq_num)] = (curr_prob - action_prob,
                                                             curr_doubles_prob)
            
            action_str = action[0]
            if action_str in inv_sq_dict:
                action_num = inv_sq_dict[action_str]
                start_prob_dict[action_num] += action_prob
                if start_landing == 1:
                   
                    add_elts_start_landing_dict (start_landing_dict, init_sq_num, action_num,
                                 action_prob, doubles_prob)
                
            else:   # These are all relative actions, depending on initial slot
                action_num = relative_squares (action_str, sq_num, inv_sq_dict)
                start_prob_dict[action_num] += action_prob
                if start_landing == 1:
                    add_elts_start_landing_dict (start_landing_dict, init_sq_num, action_num,
                                 action_prob, doubles_prob)
                    
                action_sq_name = square_dict[action_num]
                start_prob_dict, start_landing_dict =  is_further_movement (action_sq_name,
                                                                            square_dict,
                                                        inv_sq_dict, start_prob_dict,
                                                        movement_dict, action_prob,
                                                        start_landing_dict, start_landing,
                                                        init_sq_num, doubles_prob)
    return start_prob_dict, start_landing_dict


# If the action required is relative to current position (e,g,
# back 3 spaces or Next Railroad), then this function will
# determine final landing spot
def relative_squares (action_str, curr_square_num, inv_sq_dict):

    from bisect import bisect_right
    
    num_total_squares = len (inv_sq_dict)
    
    if action_str == 'Z3': # back 3 spaces
        return end_square (curr_square_num, -3, num_total_squares)

    if action_str == 'RN': # find the next railroad
        railroad_num_list = [5, 15, 25, 35]
        pos = bisect_right (railroad_num_list, int (curr_square_num))
        if pos == len (railroad_num_list):
            pos = 0
        if pos == 0:
            action_num = '0' + str(railroad_num_list[pos])
        else:
            action_num = str(railroad_num_list[pos])
        return action_num
        
    if action_str == 'UN': # find next utility
        util_num_list = [12,28]
        if (int (curr_square_num) < util_num_list[0]) or (int(curr_square_num)
                                                           >= util_num_list[1]):
            action_num = str (util_num_list[0])
        else:
            action_num = str (util_num_list[1]) 
        return action_num

# This calculates the probability of landing on any given square
# beginning with the assumption that each square has equal
# probability of a landing, before movement actions are forced due to
# that landing (i.e. go to jail, draw a Chance card, ...)

def init_start_prob_dict (num_total_squares, square_dict, movement_dict):

    start_prob_dict = {square: 1.0 / num_total_squares for
                       square in square_dict}

    # Inverse dictionary to look up square number by square name
    inv_sq_dict = {v: k for k,v in square_dict.items()}

    for square in start_prob_dict:
        sq_name = square_dict[square]
        init_prob = start_prob_dict[square]
        start_prob_dict, sl_dict = is_further_movement (sq_name, square_dict,
                                               inv_sq_dict,
                                               start_prob_dict, movement_dict,
                                               init_prob)
    return start_prob_dict


# This takes the current square probabilities, rolls dice from each square,
# and calculates the landing probabilities for each square.
# In time, the current probabilities and these end probabilities should
# be the same, but it may require multiple iterations
def calc_end_prob (start_prob_dict, dice_odds_dict, square_dict, movement_dict,
                   prob_doubles_dict, dice_sides, include_doubles, prob_two_doubles_dict = {}):

    end_prob_dict = {k:0 for k in square_dict}
    inv_sq_dict = {v:k for k,v in square_dict.items()}
    jail_prob = start_prob_dict[inv_sq_dict['JAIL']]

    start_landing_dict = {}
    
    for square in square_dict:        
        for roll_num in dice_odds_dict:
            landing_square = end_square (square, roll_num,
                                         len(square_dict))
            landing_sq_name = square_dict[landing_square]
            
            init_prob = (start_prob_dict[square] *
                                             dice_odds_dict[roll_num])

            # check for odds of 3 doubles in a row
            if include_doubles == 1:
                if roll_num % 2 == 0:
                    trip_doubles_prob = (prob_two_doubles_dict[square] * prob_doubles_dict[roll_num])
                else:
                    trip_doubles_prob = 0
            else:
                trip_doubles_prob = 0
            
            end_prob_dict[inv_sq_dict['JAIL']] += (init_prob * trip_doubles_prob)

            init_prob = init_prob * (1 - trip_doubles_prob) # subtract jail prob
            
            end_prob_dict[landing_square] += init_prob
                                             
            end_prob_dict, sl_dict = is_further_movement (landing_sq_name, square_dict,
                                                 inv_sq_dict,
                                                 end_prob_dict, movement_dict,
                                                 init_prob)
    return end_prob_dict


def add_elts_start_landing_dict (start_landing_dict, start_num, landing_num,
                                 init_prob, doubles_prob):
    square, landing_square = start_num, landing_num
    
    if (start_num, landing_num) not in start_landing_dict:
        start_landing_dict[(square,
                    landing_square)] = (init_prob,
                                        doubles_prob)
    else:
        prev_init_prob = start_landing_dict[(square, landing_square)][0]
        prev_doubles_prob =  start_landing_dict[(square, landing_square)][1]
        curr_init_prob = init_prob
        curr_doubles_prob = doubles_prob
        if prev_init_prob + curr_init_prob > 0:
            wtd_doubles_prob = ((prev_init_prob * prev_doubles_prob
                            + curr_init_prob * curr_doubles_prob) /
                            (prev_init_prob + curr_init_prob))
        else:
            wtd_doubles_prob = 0
        start_landing_dict[(square, landing_square)] = ((prev_init_prob +
                                                         curr_init_prob),
                                                        wtd_doubles_prob)
    return start_landing_dict
    
    

def calc_start_landing_dict (start_prob_dict, dice_odds_dict, square_dict,
                             movement_dict, prob_doubles_dict, dice_sides):

    start_landing_dict = {}
    inv_sq_dict = {v:k for k,v in square_dict.items()}
    end_prob_dict = {k:0 for k in square_dict}

    
    for square in square_dict:
        for roll_num in dice_odds_dict:
            landing_square = end_square (square, roll_num,
                                         len(square_dict))
            landing_sq_name = square_dict[landing_square]
            
            init_prob = (start_prob_dict[square] * dice_odds_dict[roll_num])
            
            if roll_num in prob_doubles_dict:
                doubles_prob = prob_doubles_dict[roll_num]

            else:
                doubles_prob = 0


            
            start_landing_dict = add_elts_start_landing_dict (start_landing_dict, square,
                                                                  landing_square,
                                                                  init_prob,
                                                                  doubles_prob)
            end_prob_dict[landing_square] += init_prob


            end_prob_dict, start_landing_dict = is_further_movement (landing_sq_name, square_dict,
                                                 inv_sq_dict,
                                                 end_prob_dict, movement_dict,
                                                 init_prob, start_landing_dict,
                                                 1, square, doubles_prob)

    return end_prob_dict, start_landing_dict

def calc_odds_doubles_landing (end_landing_dict, square_dict):
    import operator
    
    sq_doubles_dict = {}
    for square in square_dict:
        sq_list = [v[0] for k,v in end_landing_dict.items() if k[1] == square]
        sq_doub_list = [(v[0]* v[1]) for k,v in end_landing_dict.items() if k[1] == square]
        check_list =  [(k[0], v[0], v[1]) for k,v in end_landing_dict.items() if k[1] == square]
            
        if sum(sq_list) > 0:
            sq_doubles_dict[square] = (sum(sq_doub_list) /
                                       sum(sq_list))
        else:
            sq_doubles_dict[square] = 0.0
            
    sq_two_doubles_dict = {}
    for square in square_dict:
        sq_mini_dict = {k[0]:v[0] for k,v in end_landing_dict.items() if k[1] == square}

        sq_comb_list = [sq_doubles_dict[k] * sq_mini_dict[k] for k in sq_mini_dict]
        if sum (sq_mini_dict.values()) > 0:
            sq_two_doubles_dict[square] = ((sum(sq_comb_list) / sum (sq_mini_dict.values()) *
                                        sq_doubles_dict[square]))
        else:
            sq_two_doubles_dict[square] = 0

    return sq_two_doubles_dict
        

            


# This calculates the maximum value difference between two dictionaries
# with the same keys
def dict_diff (dict1, dict2):
    from math import fabs

    max_diff = 0
    for k in dict1:
        if type (dict1[k]) is tuple:
            max_diff = max (fabs(dict1[k][0] - dict2[k][0]), max_diff)
        else:
            max_diff = max (fabs(dict1[k] - dict2[k]), max_diff)
    return max_diff

def main():
    filename = "monopoly_squares.txt"
    square_dict = init_square_dict (filename)

    str_list = ['CC1', 'CC2', 'CC3', 'CH1', 'CH2', 'CH3', 'G2J']
    
    file_suffix = '.txt'
    movement_dict = init_movement_dict (str_list, file_suffix)
    
    dice_sides = 4
    dice_odds_dict = init_dice_odds_dict (dice_sides)

    start_prob_dict = init_start_prob_dict (len(square_dict), square_dict,
                                            movement_dict)

    prob_doubles_dict = init_prob_doubles_dict (dice_sides)

    include_doubles = 0

    end_prob_dict =  calc_end_prob (start_prob_dict, dice_odds_dict,
                                    square_dict, movement_dict,
                                    prob_doubles_dict, dice_sides,
                                    include_doubles)
    thresh = 0.00001
    
    while dict_diff (start_prob_dict, end_prob_dict) > thresh:
        start_prob_dict = end_prob_dict
        end_prob_dict =  calc_end_prob (start_prob_dict, dice_odds_dict,
                                    square_dict, movement_dict,
                                        prob_doubles_dict, dice_sides,
                                        include_doubles)
        
    end_prob_dict, end_landing_dict = calc_start_landing_dict (start_prob_dict, dice_odds_dict,
                                                                 square_dict,
                                                                 movement_dict,prob_doubles_dict,
                                                                 dice_sides)


    sq_two_doubles_dict = calc_odds_doubles_landing (end_landing_dict, square_dict)
    
    start_prob_dict = end_prob_dict

    include_doubles = 1

    end_prob_dict =  calc_end_prob (start_prob_dict, dice_odds_dict,
                                    square_dict, movement_dict,
                                    prob_doubles_dict, dice_sides,
                                    include_doubles, sq_two_doubles_dict)
    thresh = 0.00001
    
    while dict_diff (start_prob_dict, end_prob_dict) > thresh:
        start_prob_dict = end_prob_dict
        end_prob_dict =  calc_end_prob (start_prob_dict, dice_odds_dict,
                                    square_dict, movement_dict,
                                    prob_doubles_dict, dice_sides,
                                    include_doubles, sq_two_doubles_dict)
    
                                    
    
    end_sum = 0
    for i in range(40):
        if i < 10:
            i_str = '0' + str(i)
        else:
            i_str = str(i)
        print i_str, end_prob_dict[i_str]
        end_sum += end_prob_dict[i_str]
    print end_sum

main()
