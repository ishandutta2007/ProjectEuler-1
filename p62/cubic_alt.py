# cubic_alt.py
# Find the smallest cube such that permuting its digits leads to
# 4 other cubes

import collections

def digit_frequency (num):
    num_list = list(str(num))
    counter = collections.Counter (num_list)
    num_possible_digits = 10
    freq_list = [0] * num_possible_digits
    for x in counter:
        freq_list[int(x)] = counter[x]
    num_rep = []
    for freq in freq_list:
        num_rep += str(freq)        
    return (''.join(num_rep))


def dictinvert(d):
    inv = {}
    for k, v in d.iteritems():
        keys = inv.setdefault(v, [])
        keys.append(k)
    return inv


def find_target_cubic (dig_freq_list, freq_dict):
    target_permutations = 5
    
    counter = collections.Counter (dig_freq_list)
    tgt_perm_list = []
    for x in counter.most_common (len (dig_freq_list) / target_permutations):
        if x[1] >= target_permutations:
            tgt_perm_list.append(x[0])
            
    min_val = 0        
    if len (tgt_perm_list) > 0:
        inv_freq_dict = dictinvert(freq_dict)
        min_val = min (inv_freq_dict[tgt_perm_list[0]])
        for dig_list in tgt_perm_list:
            min_val =  min (min_val, min(inv_freq_dict[dig_list]))
    return min_val



num_digits = 8
tens_exp = num_digits - 1

while True:
# generate all the cubes with "num_digits" digits
    freq_dict = {}
    start_i = int((10 ** tens_exp)**(1/3))+1
    i = start_i
    dig_freq_list = []
    while i ** 3 < 10 ** num_digits:

        freq_dict[i] =  digit_frequency(i ** 3)
        dig_freq_list.append (freq_dict[i])
        i += 1

    # checks if any digit representations recur 5 times or more
    min_val = find_target_cubic (dig_freq_list, freq_dict)
    if min_val > 0:
        print min_val, min_val ** 3
        break
    
    num_digits += 1
    tens_exp = num_digits - 1
