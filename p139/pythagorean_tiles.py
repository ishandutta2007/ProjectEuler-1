# pythagorean_tiles.py
# Find all Pythagorean triples (a,b,c) such that a - b divides c
# Count them all for triangles with perimeter less than 100 MM
# Problem boils down to Pell's equation for d = 2

import time

def Pell_recurrence (init_x, init_y, max_perimeter):
    soln_count = 0


    perimeter = calc_triangle_perimeter (init_x, init_y)
    
    # every linear multiple of this triangle is a solution
    soln_count += max_perimeter / perimeter
    
    past_x, past_y = init_x, init_y

    # Pell solution recurrence for positive/negative Pell equation, d = 2
    while perimeter < max_perimeter:
        x = 3 * past_x + 4 * past_y
        y = 2 * past_x + 3 * past_y
        perimeter = calc_triangle_perimeter (x, y)
        soln_count += max_perimeter / perimeter
        
        past_x, past_y = x,y
        
    return soln_count

# Given Pell solutions, translate this into n,m (Pythagorean triple
# generators) to yield the sides of the triangle
def calc_triangle_perimeter (x, y):

    m,n = y, x + y
    
    a = n**2 - m ** 2
    b = 2 * m * n
    c = n ** 2 + m ** 2
    return (a + b + c)

def main():
    start_time = time.time()
    max_perimeter = 100 * (10 ** 6)
    total_solns = 0
    
    init_x, init_y = 3, 2 # initial solution to Pell's equation, d = 2
    total_solns += Pell_recurrence (init_x, init_y, max_perimeter)

    init_x, init_y = 1, 1 # initial solution to negative Pell's equation, d = 2
    total_solns += Pell_recurrence (init_x, init_y, max_perimeter)
    
    print total_solns
    print time.time() - start_time
main()
