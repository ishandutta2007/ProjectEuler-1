# path_sum.py
# Find minimal path sum through an 80 x 80 matrix
# of numbers, moving from upper left corner to lower right
# moving either right or down


def fill_matrix_values (filename, data_matrix):
    with open(filename, 'r') as f:
        for line in f:
            line_list = []
            x1 = line.split(',')
            for x in x1:
                line_list.append(int(x))
            data_matrix.append(line_list)


def calc_path_values (data_matrix):
    path_values = data_matrix
    matrix_size = len(data_matrix)

    for height in xrange (2 * matrix_size - 2, -1, -1):
        if height >= matrix_size:
            start_row = matrix_size - 1
            start_col = height - start_row
        else:
            start_col = 0
            start_row = height - start_col

        x, y = start_row, start_col

        while x < matrix_size and y < matrix_size and x >= 0 and y >= 0:
            if x+1 < matrix_size and y+1 < matrix_size:
                path_values[x][y] +=  min(path_values[x+1][y], path_values[x][y+1])
            else:
                if y + 1 < matrix_size:
                    path_values[x][y] += path_values[x][y+1]
                else:
                    if x + 1 < matrix_size:
                        path_values[x][y] += path_values[x+1][y]
                    
            x, y = x-1, y+1
            
    return path_values[0][0]
            
input_file = "matrix.txt"
data_matrix = []

fill_matrix_values (input_file, data_matrix)

print calc_path_values (data_matrix)
