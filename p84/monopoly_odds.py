# monopoly_odds.py
# Calculate the odds of landing on any given monopoly square
# Final answer is concatenating the square numbers of the 3 most likely
# landing squares if using 2 4-sided dice


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

def end_square (start_square, roll_num, num_total_squares):

    final_num_square = (int(start_square) + roll_num) % num_total_squares

    if final_num_square > 10:
        return str(final_num_square)

    return ('0' + str(final_num_square))

def is_further_movement (sq_name, inv_sq_dict, start_prob_dict,
                             movement_dict):

    sq_num = inv_sq_dict[sq_name]
    init_prob = start_prob_dict[sq_num]
    
    if sq_name in movement_dict: 
        movement_list = movement_dict[sq_name]
        for action in movement_list:
            action_prob = init_prob * action[1]
            start_prob_dict[sq_num] -= action_prob # prob  of ending on sq_name
            
            action_str = action[0]
            if action_str in inv_sq_dict:
                action_num = inv_sq_dict[action_str]
                start_prob_dict[action_num] += action_prob
                
            else:   # These are all relative actions, depending on initial slot
                action_num = relative_squares (action_str, sq_num, inv_sq_dict)
                start_prob_dict[action_num] += action_prob

    return start_prob_dict


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
        start_prob_dict = is_further_movement (sq_name, inv_sq_dict,
                                               start_prob_dict, movement_dict)    
    return start_prob_dict

def main():
    filename = "monopoly_squares.txt"
    square_dict = init_square_dict (filename)

    str_list = ['CC1', 'CC2', 'CC3', 'CH1', 'CH2', 'CH3', 'G2J']
    
    file_suffix = '.txt'
    movement_dict = init_movement_dict (str_list, file_suffix)
    
    dice_sides = 6
    dice_odds_dict = init_dice_odds_dict (dice_sides)

    start_prob_dict = init_start_prob_dict (len(square_dict), square_dict,
                                            movement_dict)

    for i in range (len(start_prob_dict)):
        if i < 10:
            i_str = '0' + str(i)
        else:
            i_str = str(i)
        print i, start_prob_dict[i_str]
    
    
main()
