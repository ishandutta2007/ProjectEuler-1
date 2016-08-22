# under_the_rainbow.py
# Given urn with 10 balls each for 7 different colors
# what is expected value of number of colors picked
# from 20 balls chosen at random

from math import factorial

# number of permutations of n objects chosen r ways
def n_P_r (n, r):
    return factorial(n) / factorial(n-r)

# number of combinations of n objects chosen r ways
def n_C_r (n, r):
    return factorial(n) / (factorial(r) * factorial(n-r))

def gen_total_combinations (total_colors, num_color_balls, combo_list):

    combo_colors = len(combo_list)    
    # check combo for repeats of numbers
    frequency = []
    i = 0
    j = i+1
    freq = 1
    while (i < combo_colors) and j < combo_colors:
       
        while (combo_list[i] == combo_list[j]): 
            j += 1
            freq += 1
            if j == combo_colors:
                break
        frequency.append(freq)
        i = j
        j, freq = i+1, 1

    if len(combo_list) > 1:
        if combo_list[-1] != combo_list[-2]:
            frequency.append(1)
            
    intra_color_combos = 1
    for num in combo_list:
        intra_color_combos *= n_C_r (num_color_balls, num)
        
    freq_prod = 1
    for freq in frequency:
        freq_prod *= factorial(freq)
            
    return n_P_r (total_colors, combo_colors) * intra_color_combos / freq_prod
    

def gen_all_partitions (total, num_choices, min_amt, max_amt, total_colors, num_balls_color, combo_list=[]):
    if num_choices == 1:
        if total >= min_amt and total <= max_amt:

            final_combo = combo_list + [total]

            return gen_total_combinations  (total_colors, num_balls_color, final_combo)
            
        else:
            return 0

    max_amt = min (total - (num_choices - 1), max_amt)
    total_combos = 0
    
    for i in xrange (min_amt, max_amt+1):
        test_list = combo_list + [i]
        total_combos +=  gen_all_partitions (total-i, num_choices-1,i,max_amt,total_colors, num_balls_color, test_list)

    return total_combos


num_colors = 7
num_balls_color = 10
total_balls = num_colors * num_balls_color
balls_chosen = 20
ex_num_colors = 0

for colors in range (2, num_colors+1):
    ex_num_colors += (colors * gen_all_partitions (balls_chosen, colors, 1, 10, num_colors, num_balls_color) / (n_C_r (total_balls, balls_chosen) + 0.0))

print ex_num_colors

