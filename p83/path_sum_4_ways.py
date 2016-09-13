# path_sum_4_ways.py
# Find the minimal path sum from upper left to bottom right corner of an
# 80 x 80 matrix, where up, right, left, right movement is permitted

def get_matrix_data (filename):
    data_matrix = []
    with open (filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            x1 = line.split(',')
            x2 = map (int, x1)
            print x2
            matrix_data.append (x2)
    return data_matrix


# This will determine the min path value for each element of the matrix
# The solution to the problem will be the minimum value of the element [0,0]
# This assumes only up, down, right movement for min val calculations
def assign_values_matrix (data_matrix):

    # make 2 column matrices
    prev_col = []
    curr_col = []
    num_rows = len (data_matrix)
    num_cols = len (data_matrix[0])

    # the min path value for every element in the
    # final column is the sum of itself and all elements below it
    for row in data_matrix:
        curr_col.append (row[num_cols-1])
        prev_col.append (row[num_cols-2])

    # Breaking point
        
    
    # Calculate the min path values in reverse order by column
    for i in xrange (num_cols-2, -1, -1):
        prev_col = calc_prev_column (curr_col, prev_col)
        curr_col = prev_col
        prev_col = []
        if i > 0:
            for row in data_matrix:
                prev_col.append (row[i-1])

    return min(curr_col)


def main():
    filename = "matrix.txt"
    get_matrix_data (filename)


    

main()
    
