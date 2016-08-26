# dice_game.py
# P1 has 9 4-sided dice
# P2 has 6 6-sided dice
# What's the probability that P1 rolls higher than P2

import collections
from math import factorial

# Given a set of rolled dice, this gives the number
# of permutation of that roll
def calc_num_permutations (roll_list):
    num_rolls = len (roll_list)
    counter = collections.Counter (roll_list)
    freq_list = counter.most_common (num_rolls)
    div_factor = 1
    for freq in freq_list:
        div_factor *= factorial(freq[1])
    return factorial(num_rolls) / div_factor


# This calculates the number of ways to roll a single number given the
# number and type of dice being rolled
def calc_num_partitions (total, min_roll, max_roll, num_dice, prev_rolls=[]):
    if num_dice == 1:

        if len(prev_rolls) > 0:
            mod_min_roll = max(min_roll, prev_rolls[-1])
        else:
            mod_min_roll = min_roll

        
        final_roll = prev_rolls
        if mod_min_roll <= total and max_roll >= total:
            final_roll = final_roll + [total]
            return calc_num_permutations (final_roll)
        else:
            return 0
        
    total_perms = 0
    mod_max_roll = min(max_roll, total - (num_dice - 1)) # each die must be at least 1
    if len(prev_rolls) > 0:
        mod_min_roll = max(min_roll, prev_rolls[-1])
    else:
        mod_min_roll = min_roll

    for i in range (mod_min_roll, mod_max_roll+1):
        total_perms += calc_num_partitions(total-i, mod_min_roll, mod_max_roll, num_dice-1, prev_rolls + [i])

    return total_perms


# Fills 2 dictionaries: one is the probability of rolling a number given the dice setup (num of dice, and sides per die)
# The other is the cumulative probability of rolling that number or less
# given the dice setup

def fill_dice_probabilities (dice_dict, cumul_dict, num_sides, num_dice):
    
    for i in range (num_dice * 1, num_dice * num_sides+1):
        
        dice_dict[i] =  calc_num_partitions (i, 1, num_sides, num_dice) / (num_sides ** num_dice + 0.0)
        
        if (i-1) in cumul_dict:
            
            cumul_dict[i] = cumul_dict[i-1] + dice_dict[i]
        else:
            cumul_dict[i] = dice_dict[i]

    


pyramid_dice_dict = {}  # probabilities of rolls w 9 4-sided dice
cumul_pyr_dict = {}  # cumulative probabilities
cube_dice_dict = {}
cumul_cube_dict = {}

num_pyr_dice = 9
num_cube_dice = 6
num_pyr_sides = 4
num_cube_sides = 6


fill_dice_probabilities (pyramid_dice_dict, cumul_pyr_dict, num_pyr_sides, num_pyr_dice)

fill_dice_probabilities (cube_dice_dict, cumul_cube_dict, num_cube_sides, num_cube_dice)



total_winning_prob = 0
for i in range (num_pyr_dice * 1, num_pyr_dice * num_pyr_sides+1):
    total_winning_prob += pyramid_dice_dict[i] * cumul_cube_dict[i-1]
    
print total_winning_prob

