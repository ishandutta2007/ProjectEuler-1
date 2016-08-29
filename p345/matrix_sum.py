# matrix_sum.py
# Given a 15x15 matrix of numbers, pick the 20 numbers (with unique row and col)
# such that their sum is maximized

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

# Recursive function that calculates the matrix sum by taking each point,
# getting rid of its row and column, and determining the remaining
# matrix's matrix sum
def calc_matrix_sum (matrix_data, init_val=0):
    # Base case - if 2x2 matrix, matrix sum is the maximum of the diagonal sums
    
    if len (matrix_data) == 2:
        return init_val + max(matrix_data[0][0] + matrix_data[1][1], matrix_data[0][1]+matrix_data[1][0])

    total_sum = 0
    for i in range(0, len(matrix_data)):
        x = matrix_data[i]
        total_sum = max(total_sum, calc_matrix_sum(collapse_matrix (matrix_data, i, 0), x[0] + init_val))

    return total_sum

                        

input_file = "matrix.txt"

matrix_data = get_matrix_values (input_file)


n = 11
matrix_data = matrix_data[:n]
for i in range(n):
    matrix_data[i] = matrix_data[i][:n]

print matrix_data
print calc_matrix_sum (matrix_data)

