# brute_force.py
import sys, time


# Find x,y such that sum = a^2, diff = b^2 
def solve_xy (a, b):
    y = (a ** 2 - b ** 2) / 2
    x = a ** 2 - y

    return (x,y)

def find_possible_z (x,y, square_list):
    possible_z1 = set([(s-x) for s in square_list if s > x and s < 2*x])
    possible_z2 = set([(s - y) for s in square_list if s > y and s < 2*y]) 
    possible_z3 = set([(x - s) for s in square_list if x > s])
    possible_z4 = set([(y - s) for s in square_list if y > s]) 

    possible_z = possible_z1.intersection (possible_z2)
    if len(possible_z) > 0:
        possible_z = possible_z.intersection (possible_z3)
        if len(possible_z) > 0:
            possible_z = possible_z.intersection (possible_z4)
            if len(possible_z) > 0:

                return x + y + min(possible_z)
    return 0

def sum_squares (num):
    square_list = [x * x for x in range(1, int(num ** 0.5) + 1)]

    diff_list = [num - s for s in square_list]

    print set(square_list).intersection(set(diff_list))

def main():
    start_time = time.time()
    x_max = 1000
    square_list = [x * x for x in range(1, x_max+1)]

    for a in xrange(x_max, 4, -1):
        if a % 50 == 0:
            print a
        for b in xrange(a - 2, 2, -2):
            # Assume x + y = a^2
            # We will then assume x - y = b^2
            # Solve for x,y
            # Find suitable z's for the problem

            x,y = solve_xy (a,b)
            if x < y or y < 0:
                break

            test_xyz = find_possible_z (x,y, square_list)
            if test_xyz > 0:
                print a, b, test_xyz
    print time.time() - start_time 
main()
