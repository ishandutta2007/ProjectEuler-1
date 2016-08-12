# pyth_triplet.py
from operator import mul

def check_combo (a, b, c):
    if c**2 == (a**2 + b**2):
        return 1
    return 0


def gen_possible_ab_combos (c, total_sum):
    low_start_point = (total_sum - c) / 2
    high_start_point = total_sum - c - low_start_point
    a, b = low_start_point, high_start_point

    while a > 0 and b < c:
        if check_combo (a, b, c) == 1:
            return [a,b,c]
        a, b = a-1, b+1
    return []
        
total_sum = 1000
for c in range(334, 500):
    final_combo = gen_possible_ab_combos (c, total_sum)
    if final_combo != []:
        print final_combo, reduce (mul, final_combo)
        break
