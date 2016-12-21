# brute_force.py

def poly_fn(n):
    return 5 * n * n + 14 * n + 1

def make_square_set (max_num):

    sq_list = [x * x for x in range(1, max_num + 1)]

    return set(sq_list)

def main():
    max_num = 5000
    poly_max_num = int(max_num / (5 ** 0.5))

    square_set = make_square_set (max_num)
    poly_set = set (map(poly_fn, range(1, poly_max_num + 1)))

    soln_list =  sorted(list(square_set.intersection (poly_set)))

    print soln_list

main()
    
