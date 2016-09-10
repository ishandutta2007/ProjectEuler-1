# digital_root_clocks.py
# Two digital clocks calculate the digital root of a number step by step
# On clock 1, each intermediate number is displayed digitally with no
# regard to the number preceding it, wasting transitions
# On clock 2, each intermediate number is displayed using what was displayed
# before so as to use the minimum number of transitions
# How many steps are saved if both clocks are given all primes between
# 10 ** 7 and 2 * 10 ** 7

import sys, os, inspect, time
import collections
from bisect import bisect_left

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import sieve_primes

# This function maps each digit to a binary string, corresponding to which
# lights are on for its display. The first 4 digits correspond to the vertical
# lights going clockwise from the 1st quadrant
# The last 3 digits correspond to the horizontal lights, going from upper to lower
# The number 1 corresponds to 1001000 (upper vertical, lower vertical).
# Number 8 is 1111111, as all lights are on
# num_lights_dict counts the number of '1's in each digit

def digit_map_lights ():

    num_digits = 10
    light_dict = {}
    num_lights_dict = {}
    
    light_dict[0] = '1111101'
    light_dict[1] = '1001000'
    light_dict[2] = '1010111'
    light_dict[3] = '1001111'
    light_dict[4] = '1101010'
    light_dict[5] = '0101111'
    light_dict[6] = '0111111'
    light_dict[7] = '1101100'
    light_dict[8] = '1111111'
    light_dict[9] = '1101111'

    for i in range (num_digits):
        num_lights_dict[i] = (collections.Counter (light_dict[i]))['1']
        light_dict[i] = (light_dict[i], int(light_dict[i], 2))

        
    return light_dict, num_lights_dict

# This outputs a dictionary that gives the number of transitions needed
# to go from displaying one digit to another
# It uses the XoR function to determine this value

def transitions_between_digits (light_dict):
    num_digits = 10
    transition_dict = {}
    
    for i in xrange (num_digits):
        for j in xrange (num_digits):
            base10_xor = light_dict[i][1] ^ light_dict[j][1] 
            base2_xor = bin(base10_xor)[2:]
            str_count = collections.Counter (base2_xor)
            transition_dict[i,j] = str_count ['1']

    return transition_dict

# Returns the total number of lights displayed for all digits of a number
def total_lights (num, num_lights_dict):
    total_sum = 0
    num_str = str(num)
    for dig in num_str:
        total_sum += num_lights_dict[int(dig)]
    return total_sum

# Sums digits of a number
def sum_digits (num):
    dig_sum = 0
    num_str = str(num)
    for dig in num_str:
        dig_sum += int(dig)
    return dig_sum

# This calculates the number of lights transitioned between displaying
# prev_num and curr_num
# We know that prev_num <= curr_num
def transitions_between_numbers (curr_num, prev_num,
                                 transition_dict, num_lights_dict):

    num_transitions = 0
    curr_str, prev_str = str(curr_num), str(prev_num)
    num_leading_digits = len (prev_str) - len (curr_str)

    # First we deal with leading digits. They must be turned entirely off
    for i in range(num_leading_digits):
        num_transitions += num_lights_dict[int(prev_str[i])]

    # Now, we deal with the part of the previous number with the same
    # number of digits as the current number
    prev_str = prev_str[num_leading_digits:]

    for i in range (len(prev_str)):
        num_transitions += transition_dict[int(prev_str[i]), int(curr_str[i])]

    return num_transitions
    

def main():

    start_time = time.time()
    max_num = 2 * (10 ** 7)
    start_num = 10 ** 7
    prime_list = sieve_primes (max_num)
    light_dict, num_lights_dict = digit_map_lights()

    trans_dict = transitions_between_digits (light_dict)

    pos = bisect_left (prime_list, start_num)

    diff_count = 0
        
    for i in range(pos, len(prime_list)):

        sam_trans_count = 0
        max_trans_count = 0

        display_num = prime_list[i]

        # Turn on display num
        sam_trans_count += 1 * total_lights (display_num, num_lights_dict)
        max_trans_count += 1 * total_lights (display_num, num_lights_dict)
        
        while display_num > 9:
            prev_display_num = display_num
            display_num = sum_digits (display_num)

            # Sam turns off all lights from prev_display_num
            # and turns on all lights from display_num
            sam_trans_count += 1 * total_lights (prev_display_num, num_lights_dict)
            sam_trans_count += 1 * total_lights (display_num, num_lights_dict)

            # Max transitions from prev_display_num to display_num
            max_trans_count += 1 * transitions_between_numbers (display_num, prev_display_num,
                                                                trans_dict, num_lights_dict)
        # Sam and Max turn off the lights from final display num    
        sam_trans_count += 1 * total_lights (display_num, num_lights_dict)
        max_trans_count += 1 * total_lights (display_num, num_lights_dict)

        diff_count += (sam_trans_count - max_trans_count)
            
    print diff_count, time.time() - start_time

main()
