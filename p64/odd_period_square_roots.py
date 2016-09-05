# odd_period_square_roots.py
# For continued fraction expansions of sqrt(n), count how many have
# odd periods for n <= 10000

from alg9_rational_class import Algebraic_Rational, Alg_Rational_invert, Alg_Rational_add
import time

# generates a set of perfect squares, for easy searching
def square_list (max_num):
    i = 1
    square_list = []
    while i * i <= max_num:
        square_list.append (i * i)
        i += 1
    return set(square_list)

# recursive function that generates the integers comprising the CFE
# num must be < 1, otherwise this is invalid
def calc_cfe (num, remainder_list, int_list, period = 0):
    
    if num.val >= 1:
        print "Invalid CFE"
        return 0
    
    a = int (1 / (num.val + 0.0))
    int_list.append(a)
    curr_remainder = Alg_Rational_add (Alg_Rational_invert (num),
                                       Algebraic_Rational(-1 * a, 0, 1, 0))   
    period += 1

        
    if curr_remainder in remainder_list:
        
        return period
    else:
        remainder_list.append (curr_remainder)
        
        period = calc_cfe (curr_remainder, remainder_list, int_list, period)
        
    return period

# Returns the length of the period of the CFE for sqrt(n)
def sqrt_period_len (n):

    remainder_list = []
    test_num = n ** 0.5
    a = int (test_num)
    init_num = Algebraic_Rational (-1 * a, 1, 1, n)
    remainder_list.append(init_num)
    int_list = []
    period = calc_cfe (init_num, remainder_list, int_list)
    return period

start_time = time.time()
max_num = 10000
squ_set = square_list(max_num)
count = 0
for i in xrange(2, max_num+1):
    if i in squ_set:
        continue
    if (i-1) in squ_set:
        count += 1
        continue
    if sqrt_period_len(i) % 2 == 1:
        count += 1
print count, time.time() - start_time





















