# combinatoric_alt.py
# How many values of n_C_r are > 1 MM, for n <= 100

import math

def n_choose_r (n, r):
    return math.factorial(n) / (math.factorial(r) * math.factorial(n-r))

max_num = 100
test_num = 1000000
count = 0

for i in xrange(23,max_num+1):
    for j in xrange (0,i+1):
        if n_choose_r (i,j) > test_num:
            count += (i - 2 * j + 1)
            break
print count
