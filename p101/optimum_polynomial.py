# optimum_polynomial.py
# Use polynomials to approximate function given 1 - 10 points
# Find the sums of the first wrong terms for the first 10 examples

import operator, sys, time
from copy import deepcopy

# This will do the math such that row_num = k1 * row1 + k2 * row_num
# for matrix m1
# It will return matrix m1
# If type = "col", it takes the transpose, does the same function, then
# takes the transpose again to return the matrix
def matrix_row_elim (m1, type, row_num, row_pair, k2):

    k1, row1 = row_pair[0], row_pair[1]

    if type == "col":
        test_matrix = zip (*m1) # transpose
    else:
        test_matrix = deepcopy(m1)

    interim_row1 = map (lambda x: k1 * x, test_matrix[row1])
    interim_row2 = map (lambda x: k2 * x, test_matrix[row_num])

    new_row = map (lambda (x,y):x+y, zip(interim_row1, interim_row2))

    test_matrix[row_num] = new_row
    
    if type == "col":
        return map(list, zip(*test_matrix)) # transpose

    return test_matrix

# Runs the matrix_row_elimination function simultaneously on
# 2 matrices and returns them
def pair_row_elim (m1, m2, type, row_num, row_pair, k2):

    test1 = matrix_row_elim (m1, type, row_num, row_pair, k2)
    test2 = matrix_row_elim (m2, type, row_num, row_pair, k2)

    return test1, test2

# Given matrix m1, this returns the inverse of the matrix
# We are assuming that m1 is not singular, although minor checks will be in
# place
def matrix_inversion (m1):
    matrix_len = len(m1)
    if matrix_len == 1:
        if m1[0] != 0:
            return [1.0 / m1[0]]
        else:
            print "Singular matrix"
            sys.exit()
    
    # create the appropriate identity matrix
    id_matrix =[[0] * matrix_len for i in range(matrix_len)]
    for i in range (matrix_len):
        id_matrix[i][i] = 1

    inv_matrix = deepcopy (id_matrix)

    # This will put zeroes down the first column of m1
    for i in range(1, matrix_len):
        scalar = -1 * m1[i][0] / (1.0*m1[0][0])
        m1, inv_matrix = pair_row_elim (m1, inv_matrix, "row",
                                        i, (scalar, 0), 1)

    # Fill in matrix starting in col j, filling in all the rows i
    for j in range(1, matrix_len):
        for i in range(0, matrix_len):
            if i == j:
                continue
            scalar = -1*m1[i][j] / (1.0 * m1[j][j])
            m1, inv_matrix = pair_row_elim (m1, inv_matrix, "row",
                                        i, (scalar, j), 1) 
    # Now, all the non-diagonal elts are zero
    # Scale diagonal elements to be 1
    for i in range (matrix_len):
        if m1[i][i] == 1:
            continue
        scalar = 1.0 / m1[i][i]
        m1, inv_matrix =  pair_row_elim (m1, inv_matrix, "row",
                                         i, (scalar, i), 0) 
    return inv_matrix

# Multiplies two matrices, returns the product
def matrix_multiplication (m1, m2):
    # Check constant row lengths
    if len(set(map(len, m1))) > 1:
        print "m1 not a matrix"
        sys.exit()

    if len(set(map(len, m2))) > 1:
        print "m2 not a matrix"
        sys.exit()

    num_cols_m1 = (set(map(len, m1))).pop()
    num_cols_m2 = (set(map(len, m2))).pop()
    if num_cols_m1 != len(m2):
        print "Improper dimensions for multiplication"
        sys.exit()
    prod_matrix = []
    for i in range(len(m1)):
        prod_matrix.append([])
        for j in range(num_cols_m2):
            m2_col_j = [m2[n][j] for n in range(len(m2))]
            matrix_elt = reduce(operator.add,
                                map(lambda (x,y):x*y, zip (m1[i], m2_col_j)))
            
            prod_matrix[i].append (matrix_elt)
    return prod_matrix

def generating_fn (x):

    sum = 0
    for i in range(11):
        sum += ((-1*x)**(i))
    return sum

# Calculates the first incorrect term for the fitted polynomial of degree n
# compared to the generating_fn above
# Solves a set of linear equations via matrix multiplication to determine
# the polynomial coefficients
def calc_FIT (n):

    if n == 0:
        return generating_fn(1)

    data_pt_list = []
    equation_matrix = []
    
    for i in range(1, n+2):
        data_pt_list.append(generating_fn(i))
        row_i = [i**j for j in range(n+1)]
        equation_matrix.append(row_i)
     
    data_pt_transpose =  [[data] for data in data_pt_list]

    poly_coefficients = matrix_multiplication(matrix_inversion (equation_matrix),
                                              data_pt_transpose)

    poly_coefficients = [coeff[0] for coeff in poly_coefficients] # transpose
    
    test_int = n

    # Finds the first integer such that the polynomial approximation does not
    # equal the generating_fn, within 1 to account for rounding
    while ((int(poly(test_int, poly_coefficients)) == generating_fn(test_int)) or
     (int(poly(test_int, poly_coefficients))+1 == generating_fn(test_int))):
        test_int += 1

    return poly (test_int, poly_coefficients)


def poly(x, coefficients):
    poly_sum = 0
    for i in range(len(coefficients)):
        poly_sum += coefficients[i]*(x ** i)
    return poly_sum

    
def main():
    start_time = time.time()
    max_degree = 10

    print sum([calc_FIT(i) for i in range(max_degree)])
    print time.time() - start_time

main()
