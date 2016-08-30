# Find the smallest numbers with 2 ** 500500 divisors mod 500500507


import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")

from factors import gen_prime_list
import time
def generate_product (prime_list, target_exp, target_mod, max_num):
    prod = prime_list[0]
    divisors_exp = 1  # current number of divisors is 2^1
    multiplier_list = []
    multiplier_list.append (prime_list[0] ** 2)
    index = 1
    
    while divisors_exp < target_exp:
        multiplier_list.append (prime_list[index])
        next_multiplier = 1
        while next_multiplier != prime_list[index]:
            next_multiplier = min (multiplier_list)
            prod *= next_multiplier
            prod = (prod % target_mod)
            
            divisors_exp += 1

            if divisors_exp == target_exp:
                break
            
            multiplier_list.remove(next_multiplier)
            if next_multiplier ** 2 < max_num:
                multiplier_list.append (next_multiplier ** 2)
 
        index += 1
    return prod

start_time = time.time()            
max_num = 8000000
prime_list = []
gen_prime_list (max_num, prime_list)

print time.time() - start_time

target_exp = 500500
target_mod = 500500507

print generate_product (prime_list, target_exp, target_mod, max_num)
print time.time() - start_time
