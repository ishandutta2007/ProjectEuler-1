# mod_Fib_golden_nuggets.py
# Problem boils down to finding the first thirty x such that the
# square root of p(x) = (5x**2 + 14x + 1) is an integer
# This is a subset of solutions, via transformation, of the Pell's generalized
# equation x**2 - 5y**2 = 44

import time

# Calculates first equivalence class of solutions to
# Pell's equation x**2 - 5 y**2 = 44
def init_equivalence_class (max_y):
    
    # make set of squares to check
    square_set = set([x * x for x in
                      range(1, int((44 + 5 * max_y * max_y) ** 0.5))])
    
    y = 1
    solution_list = []
    while y < max_y:
        if 5 * y * y + 44 in square_set:
            x = int((5 * y * y + 44) ** 0.5)
            solution_list.append((x,y))
        y += 1
    return solution_list

# Uses the solution (9,4) to the Pell equation x ** 2 - 5*y**2 = 1
# to recursively derive the next set of solutions to our Pell equation
def next_equivalence_class (solution_list):
    x_sol, y_sol = 9,4
    D, n = 5, 44  # parameters of original Pell equation
    new_list = []

    for soln in solution_list:
        x,y = soln[0], soln[1]
        t,u = x_sol, y_sol
        new_x = x * t + y * u * D
        new_y = x * u + y * t
        new_list.append ((new_x, new_y))
    return new_list

#------------------------------------------------------------------------------
# Checks the relevant equation (fn below) to see which solutions lead to integer
# solutions for our equation
def find_int_solutions (solution_list):
    int_soln_list = []

    for sol in solution_list:
        y = sol[1]
        test_val = int(relevant_equation(y))
        if test_val % 10 == 4: # ensures that n is an integer
            n = (test_val - 14) / 10
            if n > 0:
                int_soln_list.append(n)

    return int_soln_list

# Setting p(x) = y**2 and solving the resulting quadratic via quadratic
# formula leads to a discrimant which is the function below
def relevant_equation (y):
    return (20 * y * y + 176) ** 0.5
#----------------------------------------------------------------------------

def main():
    start_time = time.time()
    max_equivalence_y = 37 # comes from plugging first Pell solution (7,1)
                           # into recurrence relation
    target_num = 30
    
    int_solutions = []                      
    soln_list = init_equivalence_class (max_equivalence_y)

    while len(int_solutions) < target_num:
        
        int_solutions += find_int_solutions (soln_list)
        soln_list = next_equivalence_class (soln_list)

    print sum(int_solutions[:target_num])
    print time.time() - start_time
main()
