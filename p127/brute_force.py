# brute_force.py
# Find all solutions (a,b,c) for c < 120000
# a + b = c, all rel prime, and rad(abc) < c

import sys, os, inspect, time, operator
from bisect import bisect_left, bisect_right
from math import log

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve, gcd


def radical (num, num_list, prime_set):
    if num in prime_set:
        return num
    if num == 1:
        return 1
    factor_list = num_list[num][1]
    return reduce (operator.mul, factor_list)

def main():
    start_time = time.time()
    min_num = 15625
    max_num = 15625
    prime_list, num_list = gen_co_prime_sieve (max_num)
    prime_set = set(prime_list)
    c_count = 0
    f1 = open('brute_results.txt', 'w')
    for c_num in range(min_num, max_num+1):
        for a in range(1, c_num/2):
            if gcd([a,c_num]) != 1:
                continue
            b = c_num - a
            if (radical(a, num_list, prime_set) *
                radical(b, num_list, prime_set)
                * radical(c_num, num_list, prime_set)) < c_num:
                
                f1.write("%d\n" % (c_num))
                print c_num, a, b
                c_count += c_num
    print c_count
    f1.close()
    print time.time() - start_time
    
main()
    
