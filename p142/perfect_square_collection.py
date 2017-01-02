# perfect_square_collection.py
# Find smallest x + y + z where all differences and sums b/w x,y,and z
# yield perfect squares. Assuming x > y > z

import sys, os, inspect, time
import itertools

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve
from math import log, fabs

def calc_factor_exponent (num, factor):
    if num % factor != 0 or factor == 1:
        return 0

    max_possible = int(log(num) / log(factor))
    for i in range(2, max_possible+1):
        if num % (factor ** i) != 0:
            return i - 1
    return max_possible
    

# Returns [] if number not relevant (prime, single power of 2, or
# double power of 2 with only one other prime factor)
def prime_factor_if_relevant (num, prime_set, num_list):
    if num in prime_set:
        return []
    if 2 in num_list[num][1]:
        two_exponent = calc_factor_exponent (num, 2)
        if two_exponent == 1:
            return []
            
    # If function not ended yet, calculate prime factorization
    factor_list = []
    for prime in num_list[num][1]:
        factor_list.append((prime, calc_factor_exponent (num, prime)))
    return factor_list

# Calculates the set of pairs whose product is num. It will only retain the
# pairs whose difference is even
def gen_factor_pairs (num, factor_list):
    exp_list = []
    prime_list = []
    for prime in factor_list:
        exp_list.append(prime[1])
        prime_list.append(prime[0])

    full_exp_list = [tuple(range(n+1)) for n in exp_list]

    divisor_list = []
    for test_exp in itertools.product (*full_exp_list):
        prod = 1
        for i in range(len(prime_list)):
            prod *= (prime_list[i] ** test_exp[i])
        divisor_list.append(prod)
        
    divisor_list.sort()
    pair_list = []
    for i in range(len(divisor_list)/2):
        if (divisor_list[i] - divisor_list[-1*(i+1)]) % 2 == 0:
            pair_list.append ((divisor_list[i], divisor_list[-1*(i+1)]))
    if len(pair_list) > 1:
        return pair_list
    else:
        return []

# Given two pairs of numbers, where the sum of each pair's squares are equal,
# calculate the implied x,y, and z values
# Check if x - y is a square. If so, return x + y + z. Otherwise return 0
def check_all_squares (pair1, pair2):
    a1, b1 = min(pair1), max(pair1)
    a2, b2 = min(pair2), max(pair2)
    min_xyz = 0
    
    square_list = [((b1 ** 2 - a1 ** 2)) ** 2, (2 * b1 * a1) ** 2,
                   ((b2 ** 2 - a2 ** 2)) ** 2, (2 * b2 * a2) ** 2]
    square_list.sort() # largest is x+z, smallest is y - z

    
    # Both terms must be even, can end function if not
    new_square_list = []
    if (square_list[0] - square_list[1]) % 2 != 0:
        for i in range(len(square_list)):
            new_square_list.append(4 * square_list[i])
    else:
        new_square_list = square_list[:]

    z = (new_square_list[1] - new_square_list[0]) / 2
    y = new_square_list[1] - z
    x = new_square_list[3] - z

    if check_square (x-y) == 1 and y > z and x > y:
        print x, y, z, x + y + z, pair1, pair2 
        min_xyz = (x + y + z)

    square_list[1], square_list[2] = square_list[2], square_list[1]

    new_square_list = []

    if (square_list[0] - square_list[1]) % 2 != 0:
        for i in range(len(square_list)):
            new_square_list.append(4 * square_list[i])
    else:
        new_square_list = square_list[:]

    z = (new_square_list[1] - new_square_list[0]) / 2
    y = new_square_list[1] - z
    x = new_square_list[3] - z

    if check_square (x-y) == 1 and y > z and x > y:
        print x, y, z, x + y + z, pair1, pair2
        if min_xyz == 0:
            min_xyz = (x + y + z)
        else:
            min_xyz = min(min_xyz, x + y + z)
        
    return min_xyz

def check_pair_list (pair_list):
    # Take the list of pairs, and determine all pairs of pairs
    min_xyz = 0
    for x in itertools.combinations (pair_list, 2):

        a1, a2 = x[0]
        inter_pair1 = ((a1 + a2)/2, int(fabs(a1 - a2)/2))
        a1, a2 = x[1]
        inter_pair2 = ((a1 + a2)/2, int(fabs(a1 - a2)/2))

        final_pair1 = (inter_pair1[0], inter_pair2[1])
        final_pair2 = (inter_pair2[0], inter_pair1[1])
        test = check_all_squares (final_pair1, final_pair2)
        if test != 0:
           
            if min_xyz == 0:
                min_xyz = test
            else:
                min_xyz = min(test, min_xyz)
    return min_xyz

    
def check_square (num):
    test = int (num ** 0.5)
    if test * test == num:
        return 1
    return 0

def main():
    max_num = 1000
    prime_list, num_list = gen_co_prime_sieve (max_num)
    prime_set = set(prime_list)

    min_xyz = 0

    for num in xrange(2, max_num+1):

        factor_list = prime_factor_if_relevant (num, prime_set, num_list)

        pair_list = gen_factor_pairs (num, factor_list)
        test_xyz = check_pair_list (pair_list)
        if test_xyz != 0:
            print num, test_xyz
            if min_xyz == 0:
                min_xyz = test_xyz
            else:
                min_xyz = min(min_xyz, test_xyz)
    print min_xyz
main()
