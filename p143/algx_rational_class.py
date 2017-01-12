# Algebraic rational class
# Represent numbers in form (a + b * sqrt(n)) / c

import sys, os, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gcd
from math import fabs


class Algebraic_Rational():

    def __init__ (self, a, b, c, n):
        if a != 0 and b != 0:
            gcd1 = gcd ([fabs(a),fabs(b),fabs(c)])
        if a == 0 and b == 0:
            gcd1 = 1
        if a == 0 and b != 0:
            gcd1 = gcd ([fabs(b),fabs(c)])
        if a != 0 and b == 0:
            gcd1 = gcd ([fabs(a),fabs(c)])
        self.a = a / gcd1
        self.b = b / gcd1
        self.c = c / gcd1
        self.n = n
        self.num = (a, b, c, n)


    def __eq__ (self, other):
        return self.num == other.num



def Alg_Rational_invert (x):

    a,b,c,n = x.a, x.b, x.c, x.n
    c_new = a * a - n * b * b
    if c_new < 0: # multiply everything by -1 as well
        c_new = -1 * c_new
        c = -1 * c
        
    inv_x = Algebraic_Rational(c * a, -1 * c * b, c_new, n)
    
    return inv_x

def Alg_Rational_add (x1, x2):

    a1, b1, c1, n1 = x1.a, x1.b, x1.c, x1.n
    a2, b2, c2, n2 = x2.a, x2.b, x2.c, x2.n

    if n1 != n2 and b1 * b2 != 0:
        print "Cannot add unlike algebraic fractions"
        sys.exit()

    x_sum = Algebraic_Rational (a1 * c2 + a2 * c1, b1 * c2 + b2 * c1, c1 * c2, n1)

    return x_sum

def Alg_Rational_multiply (x1, x2):
    a1, b1, c1, n1 = x1.a, x1.b, x1.c, x1.n
    a2, b2, c2, n2 = x2.a, x2.b, x2.c, x2.n

    if n1 != n2 and b1 * b2 != 0:
        print "Cannot add unlike algebraic fractions"
        sys.exit()    

    x_product = Algebraic_Rational (a1*a2 + n1*b1*b2, a1*b2 + a2*b1, c1*c2, n1)
    
    return x_product

# Raise x1 to the exp power, with mod_class
def Alg_Rational_exponent (x1, exp, mod_class):

    exp_bin = bin(exp)[2:]

    num_terms = len(exp_bin)

    exponent_array = []
    exponent_array.append(x1)
    for i in range (1, num_terms):
        new_num = exponent_array[-1]
        if new_num.c == 1:
            new_num.a = int(new_num.a) 
            new_num.b = int(new_num.b)

        a, b, c, n = new_num.a, new_num.b, new_num.c, new_num.n
        next_num = Algebraic_Rational(((a*a)%mod_class) + ((b*b*n)%mod_class),
                                      (2*a*b) % mod_class, c*c, n)
   
        exponent_array.append (next_num)
        old_num = exponent_array[-1]
        old_num.a, old_num.b = (int(old_num.a) % mod_class,
                                int(old_num.b) % mod_class)
        old_num.c, old_num.n = int(old_num.c), int(old_num.n)
             
    val = Algebraic_Rational (1, 0, 1, new_num.n)
    
    exp_list = list(exp_bin)
   
    for i in range(num_terms):
        if exp_list[i] == '1':
            val = Alg_Rational_multiply (val, exponent_array[num_terms - i - 1])

            val.a = int(val.a % mod_class)
            val.b = int(val.b % mod_class)
   
    if val.b != 0:
        print mod_class
    
    return val.a
