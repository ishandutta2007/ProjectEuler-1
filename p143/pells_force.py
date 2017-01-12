# pells_force.py
# Brute force some Pell's equation solutions for patterns

# Find solutions to x^2 - Dy^2 = N for x up to max_x
# x,y positive integers
def solve_pell (D, N, max_x):
    num_solns = 0
    for x in xrange(int(N**0.5)+1, max_x+1):
        if (x*x - N) % D == 0:
            if check_square((x*x - N)/D):
                print x, int(((x*x - N)/D)**0.5), N
                num_solns += 1
                if x == 2 * (N ** 0.5):
                    pass
    return num_solns

def find_residues (val, mod_class):
    for i in range(1, mod_class):
        if (i * i) % mod_class == val:
            print i

def check_square (num):
    test = int(num ** 0.5)
    if test*test == num:
        return 1
    return 0

def main():
    D = 3
    min_n = 4
    max_n = 4
    max_scale = 20
    
    for n in range(min_n, max_n+1):
        N = n*n
        solve_pell (D, N, max_scale*n)
# main()

find_residues (3,169)
