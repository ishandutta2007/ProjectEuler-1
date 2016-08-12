# pandigital_prime.py
# Find the largest n-digit prime which is pandigital
# i.e. using all digits from 1 through n

import sys
home_path = '/home/osboxes/ProjEuler/'

def check_pandigital (num):
    if '0' in str(num):
        return 0
    if len(set(str(num))) < len(str(num)): # are all digits unique
        return 0
    if len(str(num)) == 9: # 9-digit number w unique non-zero digits satisfies
        return 1
    
    for ch in str(num):
        if int(ch) > len(str(num)):
            return 0
    return 1


sys.path.insert (0, home_path + 'Utilities/')
from factors import is_prime

max_num = 7654321  # 5 digit pandigital must be div by 3, digit sum is 15
min_num = 2143
max_prime = 0
for i in range (1234567, 7654322, 2): 
    if check_pandigital (i) == 1:
        if is_prime(i) == 1:
            max_prime = i
print max_prime
