# torricelli_point.py
# Find all integer sided triangles whose Fermat-Torricelli points yield
# segments which are all integral

import sys, os, inspect, time, itertools, operator

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve
from algx_rational_class import Algebraic_Rational, Alg_Rational_multiply, Alg_Rational_exponent


#------------------------------------------------------------------------------
# Prime factorization of num
# Num_list[num][1] contains a list of factors (without exponents) for num
# if not a prime
def calc_prime_factorization (num, num_list, prime_set):
    if num in prime_set:
        return [(num,1)]
    factor_list = []
   
    for prime in num_list[num][1]:
        factor_list.append((prime, calc_factor_exponent(num,prime)))
    return factor_list

# Calculate max exponent such that factor ** exp | num
def calc_factor_exponent (num, factor):
    exp = 1
    while (num % (factor ** exp) == 0):
       exp += 1
    return (exp - 1)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Gets the initial equivalence class of solutions for the Pell's equation
# x**2 - D*y**2 = N, where N is a perfect square
def init_equivalence_class (D, N, max_x):
    num_solns = 0
    solution_list = []
    for x in xrange(int(N**0.5)+1, max_x+1):
        if (x*x - N) % D == 0:
            if check_square((x*x - N)/D):
                solution_list.append((x, int(((x*x - N)/D)**0.5)))
                num_solns += 1
    return solution_list

# Uses the initial solution to the appropriate Pell equation x ** 2 - D*y**2 = 1
# to recursively derive the next set of solutions to our Pell equation,
# x**2 - D*y**2 = N
def next_equivalence_class (solution_list, D, n, init_solution):
    x_sol, y_sol = init_solution
    new_list = []

    for soln in solution_list:
        x,y = soln[0], soln[1]
        t,u = x_sol, y_sol
        new_x = x * t + y * u * D
        new_y = x * u + y * t
        new_list.append ((new_x, new_y))
    return new_list

def check_square (num):
    test = int(num ** 0.5)
    if test*test == num:
        return 1
    return 0
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# This will derive solutions for x^2 - Dy^2 = n*n
def LMM_algorithm (D,n, prime_set, num_list, square_root_dict):
    # Find all factors f such that f**2 | n**2, which is equivalent
    # to finding all factors f of n
    if n == 1:
        return []
    
    N = n*n
    prime_factor_list = calc_prime_factorization(n, num_list, prime_set)

    full_factor_list =  calc_factors_below_root (prime_factor_list)

    addl_factors = [n/x for x in full_factor_list] # add factors above root n
    full_factor_list += addl_factors
    if check_square(n):
        full_factor_list.append (int(n**0.5)) # add root n if an integer

    solution_list = []
    for f in full_factor_list:
        m = N / (f*f)
        if m == 1:
            continue
        # Finds all the square roots of D in mod class m
        # Will write a faster algo to handle this later
        root_list =  calc_roots_modulo_m (D, m, prime_set,
                                          num_list, square_root_dict)

        if len(root_list) == 0:
            continue

        for z in root_list:        
            r,s = PQa_algorithm (z, m, D)
            if r < 0:
                r,s = -1*r, -1*s

            # print r*r - D*s*s, m, z, f
            if r*r - D*s*s == m:
                solution_list.append ((f*r,f*s))

    return solution_list

# Find the continued fraction expansiono of (P0 + sqrt(D))/Q0, stopping
# at a coefficient of 1 or -1. This is a condition of the LMM
# algorithm, whose function will call this one
def PQa_algorithm (P0, Q0, D):
    P, Q = [P0], [Q0]
    
    A = [0,1]
    B = [1,0]
    G = [-1*P0, Q0]

    large_list = [A, B, G]
    
    a = [int((P[-1] + (D ** 0.5))/Q[-1])]

    large_list = PQa_recursion (large_list, a[-1])

    P.append(a[-1]*Q[-1] - P[-1])
    Q.append((D - P[-1]*P[-1])/Q[-1])
    
    while Q[-1]*Q[-1] != 1:
        a.append(int((P[-1] + (D ** 0.5))/Q[-1]))
        large_list = PQa_recursion (large_list, a[-1])

        P.append(a[-1]*Q[-1] - P[-1])
        Q.append((D - P[-1]*P[-1])/Q[-1])

    A,B,G = tuple(large_list)
    r, s = G[-1], B[-1]
    return (r,s)
    
        
# Specific recursion function for the function PQa_algorithm        
def PQa_recursion (large_list, a):
    for A in large_list:
        A.append(a*A[-1] + A[-2])
    return large_list

# This calculates all square roots of num modulo m, assuming m a perfect square
def calc_roots_modulo_m (num, M, prime_set, num_list, square_root_dict):
    
    if M in square_root_dict:
        return square_root_dict[M]
    m = int(M ** 0.5)

    # If m is not in the dictionary and m has only 1 factor, then
    # num is not a residue mod m
    if m in prime_set:
        return []
    if len(num_list[m][1]) == 1:
        return []

    # Last remaining case is that m is the product of multiple primes
    prime_factor_list = num_list[m][1]
    for prime in prime_factor_list:
        if prime not in square_root_dict:
            return []

    # All prime factors have m as a residue, so there are answers
    full_factor_list = calc_prime_factorization (m, num_list, prime_set)

    # Adjust full_factor_list to be M = m**2 instead of m
    true_factor_list = []
    for factor in full_factor_list:
        true_factor_list.append((factor[0], 2*factor[1]))
    full_factor_list = true_factor_list[:]
    
    congruence_list = []
    for factor in full_factor_list:
        prime, exp = factor[0], factor[1]
        congruence_list.append(square_root_dict[prime**exp])

    all_possible_congruences = itertools.product (*congruence_list)
    root_list = []
    for cong in all_possible_congruences:
        cong_mod_list = [(cong[i],
                          full_factor_list[i][0]**full_factor_list[i][1])
                         for i in range(len(cong))]
        root_list.append (chinese_remainder_calc (cong_mod_list))

    square_root_dict[M] = root_list
    
    return root_list
#-----------------------------------------------------------------------------
# Uses quadratic reciprocity to check which primes have 3 as a residue
# This plays a role in the number of Pell's solutions that will be found
def primes_3_residue (prime_list):
    residue_3_dict = {}
    for prime in prime_list:
        if prime == 2 or prime == 3:
            residue_3_dict[prime] = 0
        else:
            if prime % 4 == 1: # prime and 3 have same residue status
                if prime % 3 == 1: # residue in 3
                    residue_3_dict[prime] = 1
                else:
                    residue_3_dict[prime] = 0
            else:
                if prime % 3 == 2: # not a residue in 3
                    residue_3_dict[prime] = 1
                else:
                    residue_3_dict[prime] = 0

    return residue_3_dict
#------------------------------------------------------------------------------
# Finds the first number x such that x*x % mod_class = num
# Do this for each prime in the inputted dictionary such that D
# is a residue
# Also finds the square root of num for each power of said prime
def square_roots_modulo (num, residue_3_dict, max_num):

    square_root_dict = {}
    for prime in residue_3_dict:
        if residue_3_dict[prime] == 0:
            continue
        
        x = square_root_mod_prime (num, prime)
        square_root_dict[prime]= [x, -1*x]
        k = 2
        while (prime ** k) < max_num ** 2:
            y =  square_root_mod_prime_exponents (num, x, prime, k)
            square_root_dict[prime**k] = [y, -1*y]
            k += 1
    return square_root_dict

# This outputs x such that x^2 = num mod (prime)
def square_root_mod_prime (num, prime):
    # Find a number a such that a^2 - num is not a square modulo prime
    a = num + 1
    while 1:
        test = (a**2 - num) % prime
        if test % prime != 0:
            if large_exponent_modulo (test, (prime - 1)/2, prime) == (prime -1):
                break
        a += 1
        
        if a % prime == 0:
            a += 1
            
    x1 = Algebraic_Rational (a, 1, 1, test) # a + sqrt(test)
    x = Alg_Rational_exponent (x1, (prime + 1)/2, prime) # (a + sqrt(test))^(p+1)/2

    if (x*x % prime) != num:
        print prime, " failed to find correct root"
        
    return x

# Given that x*x = num (mod prime), returns y such that y*y = num mod (prime ** n)
def square_root_mod_prime_exponents (num, x, prime, n):
    q = prime ** n
    r = q/prime
    e = (q - 2*r + 1)/2

    y = ((large_exponent_modulo (x, r, q) *
         large_exponent_modulo (num, e, q))) % q

    return y



def check_residue_factors (factor_list, residue_3_dict):
    for factor in factor_list:
        if residue_3_dict[factor] == 1:
            return 1
    return 0
    
#-----------------------------------------------------------------------------
# Find all pairs of square numbers whose difference is exactly D * num * num
def find_squares_diff_num (num, D, num_list, prime_set):

    final_factor_list = calc_prime_fact_D_num (num, D, num_list, prime_set)

    low_factor_list = calc_factors_below_root (final_factor_list)


    # All square differences are of the form n * (2k + n)
    # factor is treated as n, if num/n can be written as 2k+n, then valid
    # square difference
    square_list = []
    final_num = num * num * D
    for n in low_factor_list:
        if (final_num / n - n) % 2 == 0:
            k = (final_num/n - n) / 2
            if k > 0:
                square_list.append((k+n, k))
    return square_list
        
    
# Find prime factorization of D*num*num
def calc_prime_fact_D_num (num, D, num_list, prime_set):

    D_factor_list = calc_prime_factorization (D, num_list, prime_set)

    if num == 1:
        return D_factor_list
    
    init_factor_list = calc_prime_factorization (num, num_list, prime_set)

    square_factor_list = []
    prime_factor_list = []
    
    for factor in init_factor_list: # prime factorization of num * num
        prime_factor_list.append(factor[0])
        square_factor_list.append ([factor[0], factor[1]*2]) 

    final_factor_list = square_factor_list[:]
    for factor in D_factor_list:
        if factor[0] in prime_factor_list:
            rel_index = prime_factor_list.index(factor[0])
            final_factor_list[rel_index][1] += factor[1]
        else:
            final_factor_list.append(factor)
    return final_factor_list

# Returns all factors of num below num ** 0.5
def calc_factors_below_root (final_factor_list):
    num_factors = 1
    exp_list = []
    for factor in final_factor_list:
        num_factors *= (factor[1]+1)
        exp_list.append(range(factor[1]+1))
        
    all_exp_list = itertools.product (*exp_list)
    low_factor_list = []
    for tup in all_exp_list:
        new_factor = reduce(operator.mul,
                            [final_factor_list[i][0] ** tup[i]
                             for i in range(len(tup))])
        low_factor_list.append(new_factor)
    low_factor_list.sort()
    return low_factor_list[:num_factors/2]
#------------------------------------------------------------------------------
    
# Calculates num ** exp mod mod_class
def large_exponent_modulo (num, exp, mod_class):
    # Get the binary representation of exp
    exp_bin = bin(exp)[2:] # string
    num_terms = len(exp_bin)

    exponent_array = []
    exponent_array.append(num % mod_class)
    for i in range (1, num_terms):
        new_num = exponent_array[-1]
        exponent_array.append ((new_num * new_num) % mod_class)

    val = 1
    exp_list = list(exp_bin)
    for i in range(num_terms):
        
        if exp_list[i] == '1':
            val = (val * exponent_array[num_terms - i - 1]) % mod_class
    return val
#------------------------------------------------------------------------------
# Returns the modular inverse of a mod m
def modinv(a, m):
    while a < 0:
        a += m

    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
# Aids in calculating modular inverse through recursive use of gcd function
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
#-------------------------------------------------------------------------------
# Chinese Remainder theorem
# Given list of modulo values, returns x that satisfies all congruences
def chinese_remainder_calc (mod_list):
    N = 1
    for mod_pair in mod_list:
        N *= mod_pair[1]

    x = 0
    for mod_pair in mod_list:
        c, n = mod_pair[0], mod_pair[1] # c mod n
        x += c * (N/n) * modinv (N/n, n)
    return (x % N)

# Take Pell's solutions, and check for possible triangles with integral
# Torricelli segments and side lengths
def check_Torricelli_triangle (xy_pair, D, num_list, prime_set, max_sum):
    x,y = xy_pair[0], xy_pair[1]

    if x <= 0 or y <= 0:
        return []
    
    if x % 2 != 0:
        return []
    b = x/2
    q = y
    if q > b:
        return []
    if (((2*b)**2 - 3*q*q)**0.5 - q) % 2 != 0:
        return []
    p =  int(((2*b)**2 - 3*q*q)**0.5 - q) / 2
    if p <= 0:
        return []

    
    # Now we check all the squares that have a difference of 3p^2, and check
    # if the larger value fits with an integral Torricelli segment

    possible_c_list = find_squares_diff_num (p, D, num_list, prime_set)

    
    torr_list = []
    for test in possible_c_list:
        if test[0] % 2 != 0:
            continue
        c = test[0] / 2
        if c < b or c < p:
            continue
        if (test[1] - p) % 2 != 0:
            continue
        r = (test[1] - p) / 2
        if r <= 0 or c < r:
            continue
        if check_square ((2*q+r)**2 + (3*r*r)):
            if (((2*q+r)**2 + (3*r*r)) ** 0.5) % 2 == 0:
                a =  int(((2*q+r)**2 + (3*r*r)) ** 0.5) / 2

                if a >= b and (p + q + r) <= max_sum:
                    if (a+b) > c and (c+b) > a:
                        torr_list.append(tuple(sorted([p,q,r])))
    return torr_list
        
def main():
    start_time = time.time()
    max_sum = 120000    
    D = 3

    prime_list, num_list = gen_co_prime_sieve (max_sum)
    prime_set = set(prime_list)
    residue_3_dict = primes_3_residue (prime_list)
    square_root_dict = square_roots_modulo (D, residue_3_dict, max_sum)
    
    init_solution = (2,1)
    torr_triangle_set = set([])
    sum_pqr_set = set([])
    sum_pqr = 0
    
    for n in xrange(1, max_sum):
        N = n*n
        if n in prime_set or n == 1:
            factor_list = [n]
        else:
            factor_list = num_list[n][1]
            
        if n == 1 or check_residue_factors (factor_list, residue_3_dict) == 0:
            solution_list = [(2*n, n)]
        else:
            solution_list = LMM_algorithm (D, n, prime_set, num_list,
                               square_root_dict)
            solution_list += [(2*n,n)]
            
        while min([solution_list[i][1]
                   for i in range(len(solution_list))]) < max_sum/3:
            
            # Feed solution_list into calculator check for potential triangles
            for xy_pair in solution_list:
                
                new_triangle_list = check_Torricelli_triangle (xy_pair, D,
                                                                 num_list,
                                                                 prime_set,
                                                               max_sum)
                for new_tri in new_triangle_list:
                    if sum(new_tri) not in sum_pqr_set:
                        sum_pqr_set.add(sum(new_tri))

            solution_list = next_equivalence_class (solution_list, D,
                                                    N, init_solution)

    print sum(sum_pqr_set), max(sum_pqr_set)
            
    print time.time() - start_time

main()


