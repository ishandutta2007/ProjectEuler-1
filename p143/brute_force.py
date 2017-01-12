# brute_force.py
import time

def check_square (num):
    test = int(num ** 0.5)
    if test*test == num:
        return 1
    return 0

def test_function (a,b,c):
    test_prod = (a+b-c)*(a+b+c)*(a-b-c)*(a-b+c)
    if test_prod % 3 == 0:
        if check_square(test_prod/-3) == 1:
            if check_square(((-3*test_prod) ** 0.5 + a*a + b*b + c*c)/2):
                return (((-3*test_prod) ** 0.5 + a*a + b*b + c*c)/2)

    return 0

def random_check():
    b = 73*7
    for q in range(1,b):
        if check_square((2*b)**2 - 3 * q * q):
            print q, ((2*b)**2 - 3 * q * q) ** 0.5


def main():
    start_time = time.time()
    torr_set = set([])
    max_a = 20
    total_sum = 0
    for a in xrange(2, max_a+1):
        for b in xrange(int(a/(3**0.5)),a+1):
            for c in xrange(a-b+1,b):
                sum_pqr = test_function(a,b,c)
                if sum_pqr != 0:
                    print a,b,c
                    torr_set.add (int(sum_pqr ** 0.5))
#    print torr_set
    print time.time() - start_time
# main()
random_check()              
