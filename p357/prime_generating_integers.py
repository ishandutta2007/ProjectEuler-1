# prime_generating_integers.py
# Find all numbers n such that n/d, for all divisors d of n, is prime
# n < 100 MM

import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")

from factors import gen_prime_list, is_prime

# Assuming num 
def find_square_factor (num):

    if num <= 3:
        return 0
    i = 3
    while i * i <= num:
        if num % (i * i) == 0:
            return 1
        if num % i == 0:
            return find_square_factor (num / i)
        i += 2
        
    return 0


def prime_divisor_sum (num, prime_list):
    # Find all pairs whose product is num
    # check if their sum is prime

    i = 3
    while i * i < num:
        if num % i == 0:
            if is_prime(i + num/i) == 0:
                prime_list.append (i + num/i)
                return 0
        i += 1
    return 1
    

max_num = 100000000
prime_list = []

# Number must be of form 4n + 2
# Further (n+1) must be prime
index = 0
sum_target = 0
prime_list = []
i = 2
diff = 4
while i < max_num:
    
    if find_square_factor(i) == 0:
        if is_prime(i+1) == 1:
            if is_prime ((i/2 + 2)) == 1:
                if prime_divisor_sum (i, prime_list) == 1:
                    index += 1
                    sum_target += i
                    # print i
    i += diff

    
print index, sum_target
