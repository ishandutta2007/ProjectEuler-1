# path_sum_three_ways.py
# Given an 80 x 80 matrix, this finds the minimal path sum
# Valid moves are up, down, and right, all paths start in first column
# and end in last column
import time


def get_matrix_data (filename):

    data_matrix = []
    with open (filename, 'r') as f:
        for line in f:
            test_line = []
            x1 = line.split(',')
            for num in x1:
                test_line.append (int(num))
            data_matrix.append (test_line)
    return data_matrix


# Recursive function to calculate min path value for each element
# Only valid moves are down and right by construction
def calc_element_min_path (curr_col, row_num, next_col):

    # if you go right
    min_path_val = curr_col[row_num] + next_col[row_num]

    if row_num == len (curr_col) - 1: # no down option
        return min_path_val

    # In this case, there is no way going down a slot is more
    # efficient than going right
    
    if curr_col[row_num+1] > next_col[row_num]:
        return min_path_val
    
    # if you go down
    min_path_val = min (min_path_val, curr_col[row_num] + calc_element_min_path (curr_col, row_num+1, next_col))

    return min_path_val
    

# Given the nth column, this determines min path values for each element
# of the (n-1)st column
def calc_prev_column (next_col, prev_col):

    min_val_col = [0] * len (prev_col)
    
    num_rows = len(prev_col)

    for i in xrange (num_rows):
        if i == 0:
            min_val_col[i] = calc_element_min_path (prev_col, i, next_col)
        else:
            up_val = prev_col[i] + min_val_col[i-1]
            min_val_col[i] = min (up_val, calc_element_min_path (prev_col, i, next_col))
            
    return min_val_col
            
    

# This will determine the min path value for each element of the matrix
# The solution to the problem will be the minimum value of the initial column
def assign_values_matrix (data_matrix):

    # make 2 column matrices
    prev_col = []
    curr_col = []
    num_rows = len (data_matrix)
    num_cols = len (data_matrix[0])

    # the min path value for every element in the
    # final column is the element value itself
    for row in data_matrix:
        curr_col.append (row[num_cols-1])
        prev_col.append (row[num_cols-2])

    
    # Calculate the min path values in reverse order by column
    for i in xrange (num_cols-2, -1, -1):
        prev_col = calc_prev_column (curr_col, prev_col)
        curr_col = prev_col
        prev_col = []
        if i > 0:
            for row in data_matrix:
                prev_col.append (row[i-1])

    return min(curr_col)
    
start_time = time.time()
filename = "matrix.txt"
data_matrix = get_matrix_data (filename)

print assign_values_matrix (data_matrix)
print time.time() - start_time
