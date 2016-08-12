# circular_alt.py
# Modified this program such that it does not generate
# a prime list
# Instead it runs an is_prime function, which should
# be quicker

import sys
sys.path.insert (0, '/home/osboxes/ProjEuler/Utilities/')
from factors import gen_prime_list, is_prime

def rotate_num_digits (num, num_list):
    test_num = num
    for i in range(len(str(num))):
        num_list.append (test_num)
        new_str = str(test_num)[1:] + str(test_num)[0]
        test_num = int(new_str)

def check_for_even_digits (num):
    for ch in str(num):
        if int(ch) % 2 == 0:
            return 0
    return 1

min_num = 3
max_num = 1000000
prime_list = []
gen_prime_list (max_num, prime_list)
count = 1

for i in range(min_num, max_num):
    if check_for_even_digits(i) == 0:
        continue
    if is_prime (i) == 0:
        continue
    num_list = []
    rotate_num_digits (i, num_list)
    fail_test = 1
    
    for num in num_list[1:]:
        if is_prime(num) == 0:
            fail_test = 0 
            break
        
    if fail_test == 1:
        # print i
        count += 1

print count
