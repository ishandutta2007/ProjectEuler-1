# truncatable_primes.py
# Find the 11 primes that remain prime when digits are
# truncated on the right side and the left side

import sys
sys.path.insert (0, '/home/osboxes/ProjEuler/Utilities/')

from factors import is_prime, gen_prime_list

# outputs list of integers by truncating digits from the left for inputted num
def left_truncate_list (num, left_list):
    for i in range(len(str(num))):
        left_list.append (int(str(num)[i:]))

def right_truncate_list (num, right_list):
    for i in range(len(str(num)), 0, -1):
        right_list.append (int(str(num)[:i]))

# test if all list elements are prime
def test_all_elts_prime (test_list):
    for num in test_list:
        if is_prime(num) == 0:
            return 0

    return 1

def first_digit (num):
    return int(str(num)[0])

def last_digit (num):
    return int(str(num)[-1])

count_primes = 0
total_primes = 11
prime_sum = 0
min_num = 11
max_check = 1000000
i = min_num
single_digit_primes = set([2,3,5,7])

prime_list = []
gen_prime_list (max_check, prime_list)
del prime_list[0:4]
prime_set = set(prime_list)


while i < max_check:

    for i in prime_set:
        
        right_list = []
        right_truncate_list (i, right_list)

        if test_all_elts_prime (list(reversed(right_list))[:-1]) == 1:
            left_list = []
            left_truncate_list (i, left_list)

            if test_all_elts_prime (list(reversed(left_list))[:-1]) == 1:
                count_primes += 1
                prime_sum += i
                print i, count_primes

    i = max_check
    
print prime_sum
