# goldbach_oth_conj.py
# Find the first odd composite that cannot be
# expressed as the sum of a prime and twice a square

home_path = "/home/osboxes/ProjEuler/"
import sys
sys.path.insert (0, home_path + "Utilities/")

from factors import is_prime

# Can num be expressed as prime and twice a square
def check_sum_exists (num, prime_list):
    prime_set = set(prime_list)
    
    for i in range (1, (int) (num ** 0.5) + 1):
        if num - 2 * i * i in prime_set:
            return 1
    return 0
    
fail_test = 0
test_int = 3
prime_list = [2]

while fail_test == 0:
    if is_prime (test_int) == 0:  # composite
        if check_sum_exists (test_int, prime_list) == 0:
            print test_int
            fail_test = 1
    else:
        prime_list.append (test_int)
    test_int += 2
    
