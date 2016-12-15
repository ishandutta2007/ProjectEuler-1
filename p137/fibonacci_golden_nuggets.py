# fibonacci_golden_nuggets.py
# Find the natural numbers that map the infinte polynomial
# with Fib numbers as coefficients to rational numbers
# Return the 15th natural number to do this

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
# x + 1 and 2*x. The generators for the legs via the formulae:
# (n**2 - m**2) and 2 * m * n wlog n > m

# This function looks for valid m ranges where n ** 2 - m**2 is smaller than
# 2 * m * n. Valid is checked by seeing if the ratio of the legs is greater
# than 1/2 and smaller than 1/2 + 1/n0, where n0 is the last solution found
def find_m_range1 (n, n0):

    a, b, c = n0, (n * n0 + n), (-n0*n*n)

    low_bound = quad_formula (a,b,c)[0]
    upper_bound = n * (5 ** 0.5 - 1)/2

    if int(low_bound) != int(upper_bound):
        m_range = range(int(low_bound) + 1, int(upper_bound) + 1)
        return m_range
    return []

# This function looks for valid m ranges where n ** 2 - m**2 is greater than
# 2 * m * n. Valid is checked by seeing if the ratio of the legs is greater
# than 1/2 and smaller than 1/2 + 1/n0, where n0 is the last solution found
def find_m_range2 (n, n0):
    
    a,b,c = (n0 + 1), 4 * n * n0, -1*(n*n*n0 + n * n)

    upper_bound = quad_formula (a,b,c)[0]
    lower_bound = n * (5 ** 0.5 - 2)

    if int(lower_bound) != int(upper_bound):
        m_range = range(int(lower_bound) + 1, int(upper_bound) + 1)
        return m_range
    return []
#------------------------------------------------------------------------------
# If a valid triple, function returns x. If more than one is found, it returns
# the largest
def check_possible_solution (n, m_range):
    valid_x = []
    for m in m_range:
        test1, test2 = n**2 - m**2, 2 * m * n
        leg1, leg2 = min(test1, test2), max(test1, test2)
        x = leg1 - 1
        if leg2 == 2 * x:
            valid_x.append(x)
    if len(valid_x) == 0:
        return 0
    return max(valid_x)
    
def main():
    start_time = time.time()
    n0 = 2
    n = 3
    nugget_count = 1 # n0 is the first nugget
    target_count = 15

    while nugget_count < target_count:
        
        m_range = find_m_range1 (n, n0)

        if len(m_range) > 0:
            new_n0 = check_possible_solution (n, m_range)
            if new_n0 != 0:
                n0 = new_n0
                nugget_count += 1
                if nugget_count == target_count:
                    break

        m_range = find_m_range2 (n, n0)

        if len(m_range) > 0:
            new_n0 = check_possible_solution (n, m_range)
            if new_n0 != 0:
                n0 = max(new_n0, n0)
                nugget_count += 1
        n += 1
    print n0
    print time.time() - start_time
main()
