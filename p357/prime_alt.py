# prime_alt.py
# Find all numbers n such that n/d, for all divisors d of n, is prime
# n < 100 MM

import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")

from factors import gen_prime_list, is_prime



def prime_divisor_sum (num, prime_list):
    # Find all pairs whose product is num
    # check if their sum is prime

    i = 3
    while i * i <= num:
        if num % i == 0:
            if (i + num/i) not in set(prime_list):
                return 0
        i += 1
    return 1
    

max_num = 100000

# Number must be of form 4n + 2
# Further (n+1) must be prime
target_sum = 1
index = 0
i = 3
prime_list = [2]
test_list = [1]
diff = 2
while i < max_num:
    
    if is_prime(i, prime_list) == 1:
        prime_list.append(i)

        new_list = [i*a for a in test_list if a < max_num/(2*i+0.0)]        
        test_list += new_list
        print i, len(test_list)    
    i += diff
    
print index, target_sum
