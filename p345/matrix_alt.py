# matrix_alt.py
# Given a 15x15 matrix of numbers, pick the 15 numbers (with unique row and col)
# such that their sum is maximized
# This program attempts to cut down runtime on traveling salesman
# Instead of searching all possibilities, it uses a cheap algo to find a large
# possible sum
# Then it goes through all possiblities, but cuts off the search if the numbers # are too small to eventually reach the baseline

def get_matrix_values (filename):
    matrix_data = []
    with open(filename, 'r') as f:
        for line in f:
            line_data = []
            x1 = line.split()
            for x in x1:
                line_data.append (int(x))
            matrix_data.append (line_data)
    f.close()
    return matrix_data

# Given the ith row and jth column, this will collapse the matrix inputted
# to remove that row and column
def collapse_matrix (matrix_data, i, j):
    new_matrix = matrix_data
    if i < len(matrix_data) - 1:
        new_matrix = new_matrix[0:i] + new_matrix[i+1:]
    else:
        new_matrix = new_matrix[0:i]

    if j < len(matrix_data[0])-1:
        final_matrix = [x[:j]+x[j+1:] for x in new_matrix]
    else:
        final_matrix = [x[:j] for x in new_matrix]

    return final_matrix

# Uses a cheap metric to determine a set of matrix elements which should
# yield a large sum, although likely not the largest
# This sum is then used as a baseline for speeding up future searches in the matrix
def qcalc_sum (matrix_data):
    # Base case - if 2x2 matrix, matrix sum is the maximum of the diagonal sums
    
    if len (matrix_data) == 2:

        return max(matrix_data[0][0] + matrix_data[1][1], matrix_data[0][1]+matrix_data[1][0])

    total_sum = 0
    max_gain = 0
    max_index = 0
    for i in range(0, len(matrix_data)):
        x = matrix_data[i]
        gain = x[0] - max(x[1:])
        if i == 0:
            max_gain = gain
            max_index = 0
        else:
            if gain > max_gain:
                max_gain = gain
                max_index = i
                

    total_sum += (matrix_data[max_index][0] + qcalc_sum (collapse_matrix(matrix_data, max_index, 0)))
    
    return total_sum


# Recursive function that calculates the matrix sum by taking each point,
# getting rid of its row and column, and determining the remaining
# matrix's matrix sum
def calc_matrix_sum (matrix_data, baseline, max_value, init_val=0):
    # Base case - if 2x2 matrix, matrix sum is the maximum of the diagonal sums
    
    if len (matrix_data) == 2:
        return init_val + max(matrix_data[0][0] + matrix_data[1][1], matrix_data[0][1]+matrix_data[1][0])

    new_max_value = 0
    for line in matrix_data:
        new_max_value += max(line)


    if init_val + new_max_value < baseline:
        return 0
    
    total_sum = 0
    for i in range(0, len(matrix_data)):
        x = matrix_data[0][i]
        total_sum = max(total_sum, calc_matrix_sum(collapse_matrix (matrix_data, 0, i), baseline, new_max_value, x + init_val))

        baseline = max (total_sum, baseline)
        
    return total_sum


                        

input_file = "matrix.txt"

matrix_data = get_matrix_values (input_file)

 # this is the value we'll use to test future
 # searches to see if we can commute them quickly


n = 15
test_data = matrix_data[0:n]
for i in range(n):
    test_data[i] = test_data[i][0:n]

baseline = qcalc_sum (test_data)
print baseline
print calc_matrix_sum (test_data, baseline, 0)

