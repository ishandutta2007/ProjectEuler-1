# prime_cube_partnership.py
# Find all primes below one million such that there exists an n where
# n ** 3 + (n**2) * p is a perfect cube

import sys, os, inspect, time

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import sieve_primes

def generate_cubes (max_base):

    cube_list = [x ** 3 for x in range(1, max_base+1)]
    return cube_list

def generate_cube_differences (cube_list):
    diff_set = set([])

    for i in range(len(cube_list) - 1):
        for j in range(i+1, len(cube_list)):
            diff_set.add (cube_list[j] - cube_list[i])
    return diff_set


def main():
    start_time = time.time()
    max_prime = 10 ** 6
    max_cube_base = int (((max_prime) ** 0.5) / (3 ** 0.5))
    
    prime_list = sieve_primes (max_prime)
    prime_set = set(prime_list)
    print time.time() - start_time
    
    cube_list = generate_cubes (max_cube_base)
    cube_diff_set = generate_cube_differences (cube_list)

    print len(cube_diff_set.intersection (prime_set))
    print time.time() - start_time
    
main()
