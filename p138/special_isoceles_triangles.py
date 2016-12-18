# special_isoceles_triangles.py
# Find the first 12 isoceles triangles whose heights are either one more
# or one less than its base, where all sides are integers as is the height
# Return the sum of the legs of those 12 triangles

import time

def quad_formula (a,b,c):
    rad = (b * b - 4 * a * c)
    if rad < 0:
        return []
    return [(-b + rad ** 0.5) / (2 * a),
            (-b - rad ** 0.5) / (2 * a)]

#------------------------------------------------------------------------------
# The variables n and m are generators of Pythagorean triples
# Function is looking for a triple where the legs are of the form
# x and 2*x +/- 1. 
# We know that the larger value is odd, so it must be of the form
# (n**2 - m**2).
# Will use quadratic formula to determine possible range for n

def find_n_range (m, a0):
    k = 4 - 2.0/a0
    
    a, b, c = 1, -1*k, -1
    low_bound = m * quad_formula (a,b,c)[0] # ratio for n/m

    k = 4 + 2.0/a0
    
    a, b, c = 1, -1*k, -1
    upper_bound = m * quad_formula (a,b,c)[0] # ratio for n/m
    
    return range(int(low_bound) + 1, int(upper_bound) + 1)

#------------------------------------------------------------------------------
# If a valid triple, function returns num of solutions, hypotenuse length, and
# min leg length
def check_possible_solution (m, n_range):
    valid_triple = []
    l_sum, max_a0, soln_count = 0, 0, 0
    for n in n_range:
        leg1, leg2, leg3  = 2*m*n, n**2 - m**2, n**2 + m**2
        if leg1 * 2 == leg2 - 1 or leg1 * 2 == leg2 + 1: # valid triple
            valid_triple.append((leg1, leg2, leg3))
            l_sum += leg3
            max_a0 = max(leg1, max_a0)
            soln_count += 1
            print valid_triple
    return soln_count, l_sum, max_a0
                
def main():
    start_time = time.time()
    m = 1
    a0 = 1
    target_count = 12
    curr_count = 0
    leg_sum = 0

    while curr_count < target_count:
        n_range = find_n_range (m, a0)
        num_solns, leg_len, possible_a0 = check_possible_solution (m, n_range)
        curr_count += num_solns
        leg_sum += leg_len
        a0 = max (a0, possible_a0)

        m += 1
    print leg_sum
    print time.time() - start_time
main()
