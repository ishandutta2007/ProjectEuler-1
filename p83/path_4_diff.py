# path_4_diff.py
# Find the minimal path sum from upper left to bottom right corner of an
# 80 x 80 matrix, where up, right, left, right movement is permitted
# In past versions, we have tried to calculate min path values across all elements of a height
# Here, we calculate the min path values for elements near the items with the lowest min path
# values

import time, sys, operator
from math import fabs

from copy import copy

# Class which contains the row, column, and the min_path value for that row and column
# Creating this class allows for easy sorting of the elements that
# have been determined
class Coordinate_MinValue ():
    def __init__ (self, row_num, col_num, min_path_matrix):
        self.row_num = row_num
        self.col_num = col_num
        self.min_path_value = min_path_matrix[row_num][col_num]
        

def get_matrix_data (filename):
    data_matrix = []
    with open (filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            x1 = line.split(',')
            x2 = map (int, x1)
            data_matrix.append (x2)
    return data_matrix


def valid_move_check (i, j, num_rows, num_cols):
    if i < num_rows and j < num_cols:
        if i >= 0 and j >= 0:
            return 1
    return 0


# This recursive function will determine the minimum path value for the
# element of the matrix inputted. It will do this by calculating min values for all
# possible paths, with the condition that any path
# greater than already calculated paths are not optimal

def calc_min_path_value (data_matrix, min_path_matrix, curr_row, curr_col,
                         path_list, curr_min_val, min_landing_val, path_buffer,
                         curr_path_val):

    min_path_val = curr_min_val + path_buffer
    valid_move_list = [(1,0), (-1,0), (0,1), (0,-1)]
    num_rows, num_cols = len (data_matrix), len (data_matrix[0])
    if len (path_list) == 0:
        path_list.append((0,0))


    final_min_value = 0 # this is the path value plus the min path val of the
                        # final slot
    
    # base case - path has landed at an element with a previously
    # calculated min path value
    if min_path_matrix[curr_row][curr_col] > 0:
        return (curr_path_val + min_path_matrix[curr_row][curr_col]
                - data_matrix[curr_row][curr_col])

    # general case - run through valid moves
    for move in valid_move_list:
        new_path_list = copy (path_list)
        new_row, new_col = curr_row + move[0], curr_col + move[1]
                                                 
        if valid_move_check (new_row, new_col, num_rows, num_cols):
            
            new_loc = map (sum, zip (new_path_list[-1], move))
            
            if new_loc not in new_path_list: # has not traversed this path before
                new_path_val = curr_path_val + data_matrix[new_row][new_col]
                                
                if new_path_val < min_path_val:

                    new_path_list.append (new_loc)
                    final_path_val = calc_min_path_value (data_matrix,
                                                          min_path_matrix, new_row,
                                                          new_col, new_path_list,
                                                          curr_min_val,
                                                          min_landing_val,
                                                          path_buffer, new_path_val)
                    if final_min_value == 0:
                        final_min_value = final_path_val
                    else:
                        final_min_value = min (final_path_val, final_min_value)

    if final_min_value == 0: # No valid moves
        return curr_min_val + min_landing_val
                        
    return final_min_value


    
# This will determine the min path value for each element of the matrix
# The solution to the problem will be the minimum value of the element [0,0]

def assign_values_matrix (data_matrix):

    num_rows = len(data_matrix)
    num_cols = len (data_matrix[0])
    min_path_matrix = []
    gradual_data_matrix = []

    mpath_list = [] # list of objects holding coordinates whose min path has already
                    # been calculated
                    # This list will be used to determine the next element to
                    # calculate
                    # It will only hold items that are on the "front line" of
                    # calculation,
                    # meaning that any element surrounded by elements
                    # already calculated as well wlll not
                    # be in this list

    test_row = [0] * len(data_matrix[0])
    
    # Initializes the min_path matrix with zeroes
    for i in range (len (data_matrix)):
        min_path_matrix.append (copy(test_row))
        gradual_data_matrix.append (copy(test_row))

    # We know the bottom corner value is itself

    bottom_corner_val = data_matrix[num_rows-1][num_cols-1]
    
    min_path_matrix[num_rows-1][num_cols-1] = bottom_corner_val
    gradual_data_matrix[num_rows-1][num_cols-1] = data_matrix[num_rows-1][num_cols-1]
    
    # We also know the values of the elements that are one move
    # away from the bottom corner, as the min path can only be to go
    # directly to the bottom corner
                                                
    min_path_matrix[num_rows-1][num_cols-2] = (bottom_corner_val +
                                               data_matrix[num_rows-1][num_cols-2])
    gradual_data_matrix[num_rows-1][num_cols-2] = data_matrix [num_rows-1][num_cols-2]
    mpath_list.append (Coordinate_MinValue (num_rows-1, num_cols-2, min_path_matrix))

    min_path_matrix[num_rows-2][num_cols-1] = (bottom_corner_val +
                                               data_matrix[num_rows-2][num_cols-1])
    gradual_data_matrix[num_rows-2][num_cols-1] = data_matrix[num_rows-2][num_cols-1]
    mpath_list.append (Coordinate_MinValue (num_rows-1, num_cols-2, min_path_matrix))

    mpath_list.sort (key = operator.attrgetter("min_path_value"))
    
    while min_path_matrix[0][0] == 0:            

        # lowest min path element will determine the next elements to calculate
        prev_row, prev_col = mpath_list[0].row_num, mpath_list[0].col_num
        valid_list = []
        if valid_move_check (prev_row-1, prev_col, num_rows, num_cols):
            valid_list.append ((-1,0))

        if valid_move_check (prev_row, prev_col-1, num_rows, num_cols):
            valid_list.append ((0,-1))

        for move in valid_list:
            
            curr_row, curr_col = prev_row + move[0], prev_col + move[1]
            if min_path_matrix[curr_row][curr_col] > 0:
                continue
            
            min_path_val = (data_matrix[curr_row][curr_col] +
                            data_matrix[prev_row][prev_col])
            min_landing_val = (mpath_list[0].min_path_value -
                               data_matrix[prev_row][prev_col])
            path_buffer = 0

            curr_path_val = data_matrix[curr_row][curr_col]
            path_list = []
            
            min_path_matrix[curr_row][curr_col] = calc_min_path_value (data_matrix,
                                                                       min_path_matrix, curr_row, curr_col,
                                                                        path_list,
                                                                       min_path_val,
                                                                       min_landing_val, path_buffer,
                                                                       curr_path_val)
            
            gradual_data_matrix[curr_row][curr_col] = data_matrix[curr_row][curr_col]
            mpath_list.append (Coordinate_MinValue(curr_row, curr_col, min_path_matrix))

            # print curr_row, curr_col, min_path_matrix[curr_row][curr_col]
                    
        del mpath_list[0] # Now that this element has generated its possible 
                          # new elements, it can be removed from the list
        mpath_list.sort (key = operator.attrgetter("min_path_value"))

    return min_path_matrix, gradual_data_matrix        
        
def main():
    
    start_time = time.time()
    
    filename = "matrix.txt"
    data_matrix = get_matrix_data (filename)
    
    min_path_matrix, gradual_data_matrix = assign_values_matrix (data_matrix)

    print min_path_matrix[0][0]
    print time.time() - start_time


main()
    
