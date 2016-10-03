# right_triangles.py
# Count all the right triangles with integral vertices within the
# square at points (+/-50, +/-50)

import sys, os, inspect, time
from math import factorial, fabs

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gcd

# Line equation of the form ax + by + c = 0
class line_equation ():
    
    def __init__ (self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    # Generate perpendicular line going through point x,y
    # Assumes that (x,y) satisfies line equation
    def gen_perpendicular (self, x1, x2):
        a, b, c = self.a, self.b, self.c
        
        if a * x1 + b * x2 + c != 0:
            print "Error - pt is not on line", x1, x2, a*x1 + b*x2 + c, a, b, c
            sys.exit()
        
        if a != 0:
            perp_line_slope = (b + 0.0) / a
            if b >= 0:
                return line_equation (b, -1*a, a*x2 - b*x1)
            else:
                return line_equation (-1*b, a, b*x1 - a*x2)
                
        # perpendicular line slope is undefined in this case
        return line_equation (1, 0, -1*x1)

    # Counts the lattice pts within inputted bounds on a line
    def count_lattice_pts (self, min_x, max_x, min_y, max_y):

        a, b, c = self.a, self.b, self.c
        if map(int, [a,b,c]) != [a,b,c]:
            print "Non-integral coefficients"
            sys.exit()
        if a == 0:
            if c % b == 0:
                return (max_x - min_x + 1) # every x is a lattice pt
            else:
                return 0
        if b == 0:
            if c % a == 0:
                return (max_y - min_y + 1)
            else:
                return 0
        if a % b == 0 and c % b != 0:
            return 0

        # This determines how many x values (lattice_range) will map within the y boundaries
        inv_min_y = ((b * min_y + c) / (-1.0 * a))
        inv_max_y = ((b * max_y + c) / (-1.0 * a)) 
        alt_min_x = min(inv_min_y, inv_max_y)
        alt_max_x = max(inv_min_y, inv_max_y)
        if int (alt_min_x) != alt_min_x and alt_min_x > 0:
            alt_min_x = int(alt_min_x) + 1
        else:
            alt_min_x = int(alt_min_x)

        if int(alt_max_x) != alt_max_x and alt_max_x < 0:
            alt_max_x = int(alt_max_x) - 1
        else:
            alt_max_x = int(alt_max_x)
                
        lattice_init = set(range(min_x, max_x+1))
        lattice_alt = set(range(alt_min_x, alt_max_x+1))
        lattice_range = lattice_init.intersection (lattice_alt)        
       
        if a % b == 0 and c % b == 0: # all integer x map to integer y
            return len (lattice_range)

        # Final case is when b does not divide a. This requires some
        # much tighter bookkeeping

        # There cannot be integral points in this case
        if gcd ([c,b]) % gcd([a,b]) != 0:
            return 0

        # Divide through by gcd([a,b]) such that a,b are now relatively prime
        div_factor = gcd([a,b])
        a,b,c = a / div_factor, b / div_factor, c / div_factor

        lattice_range = sorted(list(lattice_range))
        lattice_range_len = len(lattice_range)

        if lattice_range_len % b == 0: # we know there is one solution for every b numbers
            return lattice_range_len / max(-1*b, b)
        else:
            range_remainder = lattice_range_len % int(max(-1*b,b))
 
            # Will check the first range_remainder values of the range for a solution
            # This determines if there is an extra solution or not

            check_range = map (lambda x: (a * x + c) % b, lattice_range[:range_remainder])
            extra_solution = (0 in set(check_range))
            return (lattice_range_len / int(max(-1*b,b)) + extra_solution)
        
# Given 2 points, yield the line equation in the form ax + by + c = 0
def calc_line_equation (x1, y1, x2, y2):
    if (x1, y1) == (x2, y2):
        print "Not a line, same point entered"
        sys.exit()
    
    if x1 == x2:
        return line_equation (1, 0, -1*x1)
    slope = (y2 - y1) / (x2 - x1 + 0.0)
    a, b, c = slope, -1, (y1 - slope * x1)  # point slope formula set to equal zero
    line_vbles = [y2- y1, -1 * (x2 - x1), y1 * (x2 - x1) - x1 * (y2 - y1)]

    return line_equation (line_vbles[0], line_vbles[1], line_vbles[2])


        
# Counts the number of right triangles that can be created assuming point (x1,y1) is the right angle
# and origin is another vertex.
# This will calculate for x1, y1 as well as any positive scalar multiples of x1,y1
def count_P_right_angle (x1, y1, min_x, max_x, min_y, max_y):
    
    # create line equation connecting origin to x1, y1
    triangle_leg = calc_line_equation (x1, y1, 0, 0)
    perp_line = triangle_leg.gen_perpendicular (x1, y1)

    # Now, we perform the count calculation for all positive integer scalars starting with 1
    scalar = 1
    count = 0
    while (scalar * x1 in set(range(min_x, max_x+1))
           and scalar * y1 in set(range(min_y, max_y+1))):
           new_perp_line = line_equation (perp_line.a, perp_line.b, perp_line.c * scalar)
           count += (new_perp_line.count_lattice_pts (min_x, max_x, min_y, max_y) - 1)
          
           scalar += 1
    return count

# Counts the number of right triangles that can be created assuming point (x1,y1) is a vertex
# and origin is the right triangle
# This will calculate for x1, y1 as well as any positive scalar multiples of x1,y1
def count_origin_right_angle (x1, y1, min_x, max_x, min_y, max_y):
    triangle_leg = calc_line_equation (x1, y1, 0, 0)
    perp_line = triangle_leg.gen_perpendicular (0, 0)
    count =  perp_line.count_lattice_pts (min_x, max_x, min_y, max_y) - 1
    total = count
    scalar = 2
    while (scalar * x1 in set(range(min_x, max_x+1))
           and scalar * y1 in set(range(min_y, max_y+1))):
        total += count
        scalar += 1
    return total
    

    # The perpendicular line does not change when we apply scalars to the point x1, y1

def main():
    start_time = time.time()
    min_x, max_x, min_y, max_y = 0, 50, 0, 50
    total_count = 0

    # this will count all triangles w origin as rt angle
    total_count += count_origin_right_angle (0, 1, min_x, max_x, min_y, max_y) 

    # Now we address the cases where the vertex is the right angle
    total_count += count_P_right_angle (0, 1, min_x, max_x, min_y, max_y) # all y-axis pts
    total_count += count_P_right_angle (1, 0, min_x, max_x, min_y, max_y) # all x-axis pts
    total_count += count_P_right_angle (1, 1, min_x, max_x, min_y, max_y) # all y=x pts

    
    for i in range (min_x, max_x+1):
        if i == 0: # case covered above
            continue
        for j in range(min_y, max_y + 1):
            if j == 0 or i == j: # cases covered above
                continue
            if gcd ([i,j]) == 1:
                total_count += count_P_right_angle (i, j, min_x, max_x, min_y, max_y)
               
    print time.time() - start_time
    return total_count

print main()

