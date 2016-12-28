# square_progressive_numbers.py
# Find all square numbers n, such that there exists divisor d, where
# n = qd + r, and {r, q, and d} form a geometric sequence, not
# necessarily in that order. Sum all progressive numbers under 1 trillion

import operator

import sys, os, inspect, time
from math import factorial

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve


def check_perfect_square (n):
    test = int (n ** 0.5)
    if test * test == n:
        return 1
    return 0

# Fills the exponent_list, square_vector, and rel_prime_vectors for the find_valid_tuple
# function inputs
# Equation is r = (k_2^1)(a_5^3)(q_2^2)(a_2^5)(a_3^4)(a_4^3)
def init_vectors ():
    exponent_list = [1,3,2,5,4,3]
    square_vector = [1,1,1,0,0,0]
    rel_prime_vector = [[], [], [0], [0], [2,3], [0,2,3,4]]

    return exponent_list, square_vector, rel_prime_vector
#------------------------------------------------------------------------------
# Finds valid tuples satisfying the equation for valid remainders
# Can be shown that remainder r = a*q0^2, where q0 is the denominator
# of the ratio p/q0, common ratio of the geometric series
# This assumes that a and q0 have a common factor
def find_valid_tuples (max_product, num_vbles, curr_vector, square_vector,
                       rel_prime_vector, prime_factor_vector,
                       exponent_vector, num_list, prime_set):

    # Base case
    if len(curr_vector) == num_vbles:
        test_product = reduce(operator.mul,
                              [curr_vector[i] ** exponent_vector[i]
                               for i in range(num_vbles)])
        if test_product < max_product:
            return [tuple(curr_vector)]
        else:
            return []

    curr_index = len(curr_vector)
    is_square = square_vector[curr_index]

    if curr_index == 0:
        curr_product = 1
        invalid_factor_set = set([])
    else:
        curr_product = 1
        for i in range(curr_index):
            curr_product *= (curr_vector[i] ** exponent_vector[i])
            
        rel_prime_indices = rel_prime_vector[curr_index]
        invalid_factor_set = set([])
        for index in rel_prime_indices:
            invalid_factor_set = (invalid_factor_set |
                                  set(prime_factor_vector[index]))

    valid_tuples = []
    num = 1
    curr_exponent = exponent_vector[curr_index]
    while True:
        # if square vbles, adjust accordingly
        if is_square:
            curr_num = num * num
        else:
            curr_num = num
        
            
        if curr_product * (curr_num ** curr_exponent) >= max_product:
            break
            
        curr_factor_set = set([])
        
        if num in prime_set:
            curr_factor_set = set([num])
        elif num != 1:
            curr_factor_set = set(num_list[num][1])

        if len(curr_factor_set.intersection (invalid_factor_set)) > 0:
            num += 1
            continue
        test_curr_vector = curr_vector[:]
        test_curr_vector.append (curr_num)

        test_prime_factor_vector = prime_factor_vector[:]
        test_prime_factor_vector.append (curr_factor_set)
        
        valid_tuples += find_valid_tuples (max_product, num_vbles, test_curr_vector,
                                           square_vector, rel_prime_vector,
                                           test_prime_factor_vector, exponent_vector,
                                           num_list, prime_set)
        num += 1
    return valid_tuples 

# Takes the valid tuples, and tests them to see if they correspond to a
# square progressive number by testing the values of "p", the numerator
# of the fraction that is the common ratio of the geometric sequence
# Equation is r = (k_2^1)(a_5^3)(q_2^2)(a_2^5)(a_3^4)(a_4^3)
def test_valid_tuples (valid_tuple_list, max_num, num_list, prime_set):
    prog_list = []
    for valid_tuple in valid_tuple_list:
        (k2, a5, q2, a2, a3, a4) = valid_tuple

        q1 = q2 * a2
        k1 = k2 * a3
        a1 = a2 * a3 * a4 * a5

        q0 = q1 * a1
        a = k1 * a1

        if q0 in prime_set or q0 == 1:
            q_factors = set([q0])
        else:
            q_factors = set(num_list[q0][1])
        
        max_p = int(((max_num / (1.0 * a * q0) - q0)/(1.0*a)) ** (1/3.0))

        for p in range(q0 + 1, max_p + 1):
            if p in prime_set:
                p_factors = set([p])
            else:
                p_factors = set(num_list[p][1])

            if len(p_factors.intersection(q_factors)) > 0:
                continue
            
            test_n = (a * q0 * (a * p ** 3 + q0))
            if check_perfect_square (test_n):

                prog_list += [test_n]

    return sorted(prog_list)
#------------------------------------------------------------------------------

def check_factors (n, num_list, prime_set):
    if n == 1 or n in prime_set:
        return set([n])
    return set(num_list[n][1])

def main():
    start_time = time.time()
    max_num = 10 ** 12

    prime_list, num_list = gen_co_prime_sieve (int(max_num ** (1/3.0)))
    prime_set = set(prime_list)
    
    exponent_vector, square_vector, rel_prime_vector = init_vectors()

    valid_tuple_list = find_valid_tuples (int(max_num ** 0.5), 6, [],
                                          square_vector, rel_prime_vector,
                                          [], exponent_vector,
                                          num_list, prime_set)
    
    other_prog_set = set(test_valid_tuples (valid_tuple_list, max_num, num_list,
                                         prime_set))


    print sum(other_prog_set)
    print time.time() - start_time
main()
