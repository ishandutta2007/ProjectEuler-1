# sudoku_reboot.py
# Takes a partially filled Sudoku puzzle as input, solves the puzzle,
# and outputs the first 3 digits of the first line
# Summing these outputs across all puzzles yields the final output


import sys, collections, time
from copy import copy, deepcopy
import operator


# This outputs the coordinates of the 3x3 square that is inputted.
# For example, square 0 is the 3x3 in the upper left hand corner, and the
# numbers move from left to right spanning zero to eight
def num_square_coordinates (square_num, square_len):

    row_start = (square_num / square_len) * square_len
    col_start = (square_num % square_len) * square_len
    return row_start, row_start + square_len, col_start, col_start + square_len

# This maps a coordinate to its square number
def map_elt_square (num_row, num_col, square_len):
    return (num_row/square_len)*square_len + num_col / square_len


class sudoku_class:
                    
    def __init__ (self, sudoku_list):
        
        sudoku_class.active_list = deepcopy(sudoku_list)
        sudoku_class.puzzle_len = len(sudoku_list)
        sudoku_class.square_len = int(sudoku_class.puzzle_len ** 0.5)
        sudoku_class.total_filled_elts = reduce(operator.add,
                                                [1 for i in range(sudoku_class.puzzle_len)
                                                 for j in range(sudoku_class.puzzle_len)
                                                 if sudoku_class.active_list[i][j] > 0])
        sudoku_class.possible_list = sudoku_class.gen_possible_list (self)

    # Generates a list of list that mirrors the active list
    # If element is filled in the active list, this contains an empty list
    # Otherwise, it contains a list of possible values that could fill that slot
    def gen_possible_list (self):
        active_list, puzzle_len, square_len = self.active_list, self.puzzle_len, self.square_len
        all_possibles = set(range(1, puzzle_len + 1))
        possible_list = []
        row_possible_vals, col_possible_vals, square_possible_vals = [], [], []
        for i in range(puzzle_len):
            test_row_vals = set(active_list[i])
            if 0 in test_row_vals:
                test_row_vals.remove(0)
            row_possible_vals.append(test_row_vals)
            test_col_vals = set([active_list[row_index][i] for row_index in
                             range(puzzle_len)])
            if 0 in test_col_vals:
                test_col_vals.remove(0)
            col_possible_vals.append (test_col_vals)
            row_start = (i / square_len) * square_len
            col_start = (i % square_len) * square_len
            test_square_vals = set([active_list[row_index][col_index]
                                    for row_index in range(row_start, row_start + square_len)
                                    for col_index in range(col_start, col_start + square_len)])
            if 0 in test_square_vals:
                test_square_vals.remove(0)
            square_possible_vals.append (test_square_vals)
            
        for i in range(puzzle_len):
            possible_list.append ([])
            for j in range(puzzle_len):
                if active_list[i][j] > 0:
                    possible_list[i].append([])
                else:
                    row_num, col_num, sq_num = i, j, map_elt_square(i,j,square_len)
                    possible_list[i].append(all_possibles.symmetric_difference (
                        row_possible_vals[row_num] | col_possible_vals[col_num]
                        | square_possible_vals[sq_num]))
        return possible_list
    
    # This finds all the slots in possible_list with one possible item in their lists
    # These slots can then be filled with this item
    def single_possible_slots (self):
        puzzle_len = self.puzzle_len

        fill_list = [(list(self.possible_list[i][j])[0], i, j) for i in range(puzzle_len)
                     for j in range(puzzle_len) if len(self.possible_list[i][j]) == 1]
        return fill_list

    # This finds the numbers that only appear once in the possible_list for a row, col
    # or square. It then finds the corresponding coordinates that this number must fill
    def single_appearance_fills (self):
        puzzle_len, square_len = self.puzzle_len, self.square_len
        possible_list = self.possible_list
        final_fill_list = []

        for obj_type in ["row", "col", "square"]:
            for i in range(puzzle_len):
                # Aggregates all elements that appear in the possible sets for each elt of the row
                test_range = self.calc_test_range (obj_type, i, self.possible_list)
                aggregate_possible_list = reduce (operator.add, map(list, test_range))
                counter = collections.Counter (aggregate_possible_list)
                raw_fill_list = [(num, obj_type, i) for num in range(1, puzzle_len+1)
                                 if counter[num] == 1]
                for fill_list in raw_fill_list:
                    final_fill_list += self.single_possible_num_find (fill_list[0],
                                                                 fill_list[1], fill_list[2])
        return final_fill_list
                
    # Updates filled elements into the active list and updates the possible list
    # Checks if filled value contradicts possible list, in which case function ends
    # and returns -1
    def add_filled_elts (self, fill_list):
        for fill in fill_list:
            val, i, j = fill
            if val not in self.possible_list[i][j]:
                return -1
            self.active_list[i][j] = val
            self.total_filled_elts += 1
            self.possible_list = self.gen_possible_list()
        total_empty_sets = reduce(operator.add, [1 for x in range(self.puzzle_len)
                                                 for y in range(self.puzzle_len)
                                                 if self.possible_list[x][y] == []])
        # contradiction criterion - some empty slot has no possibilities
        if total_empty_sets != self.total_filled_elts: 
            return -1
        return 1

    # If we find that there is only one slot in a row, column, or square that lists
    # num as possible, then we know it has to go there. This determines the row,col coordinates
    # of num for row, col, and square analysis
    def single_possible_num_find (self, num, obj_type, i):
        possible_list = self.possible_list
        puzzle_len, square_len = self.puzzle_len, self.square_len
        
        if obj_type == "row":
            test_range = possible_list[i]
            fill_list = [(num, i, j) for j in range(puzzle_len)
                         if num in possible_list[i][j]]
            return fill_list
        if obj_type == "col":
            fill_list = [(num, j, i) for j in range(puzzle_len)
                         if num in possible_list[j][i]]
            return fill_list
        if obj_type == "square":
            row_start, row_end, col_start, col_end = num_square_coordinates (i, square_len)
            fill_list = [(num, i, j) for i in range(row_start, row_end)
                         for j in range(col_start, col_end)
                         if num in possible_list[i][j]]
            return fill_list

        print obj_type, "Obj type invalid"
        sys.exit()

    # This outputs the implied range to check for a row, col, or square, numbered by i
    def calc_test_range (self, obj_type, i, possible_list):
        test_range = []
        puzzle_len, square_len = self.puzzle_len, self.square_len
        if obj_type == "row":
            test_range = possible_list[i]
        if obj_type == "col":
            test_range = [possible_list[j][i] for j in range(puzzle_len)]
        if obj_type == "square":
            row_start, row_end, col_start, col_end = num_square_coordinates (i, square_len)
            test_range = [possible_list[x][y] for x in range(row_start, row_end)
                          for y in range(col_start, col_end)]
            
        if test_range != []:
            return test_range
        print obj_type, "is not valid"
        sys.exit()

    # This sorts the possible list to find the slot with the fewest possibilities for
    # valid elements. It excluses the slots with zero length, as these are already filled
    def slot_fewest_possibles (self):
        possible_list = self.possible_list
        puzzle_len = self.puzzle_len
        test_list = [(len(possible_list[i][j]),i,j) for i in range(puzzle_len)
                      for j in range(puzzle_len) if len(possible_list[i][j])>0]
        test_list.sort(key=lambda x: x[0])
        if len(test_list) == 0:  # contradiction
            return -1, -1, []
        row_num, col_num = test_list[0][1], test_list[0][2]
        return row_num, col_num, possible_list[row_num][col_num]

    def print_list (self):
        puzzle_len = self.puzzle_len
        for i in range(puzzle_len):
            row_str = map(str, self.active_list[i])
            print ''.join(row_str)


# Function takes a sudoku class object with an incomplete active_list and attempts to solve it    
def solve_sudoku (sudoku_item):

    while sudoku_item.total_filled_elts < sudoku_item.puzzle_len ** 2:
        past_filled_elts = sudoku_item.total_filled_elts
        fill_list = sudoku_item.single_possible_slots()
        flag = sudoku_item.add_filled_elts (fill_list)
        if flag == -1: # contradiction
            return -1, []
        
        if sudoku_item.total_filled_elts == past_filled_elts:
            fill_list = list(set(sudoku_item.single_appearance_fills ()))
            flag = sudoku_item.add_filled_elts (fill_list)
            if flag == -1:
                return -1, []
        if sudoku_item.total_filled_elts == past_filled_elts:
            break
            
    if sudoku_item.total_filled_elts == sudoku_item.puzzle_len ** 2:
        # sudoku_item.print_list()
        return 1, int(''.join(map(str, sudoku_item.active_list[0][:sudoku_item.square_len])))
    else:
        row_num, col_num, possible_set = sudoku_item.slot_fewest_possibles()

        if possible_set == []: # contradiction
            return -1, []
        new_list = deepcopy (sudoku_item.active_list)
        for test_element in list(possible_set):

            new_list[row_num][col_num] = test_element
            flag, output = solve_sudoku (sudoku_class (new_list))
            if flag == 1:
                return flag, output
        return -1, []
        sys.exit()            
                    
def gen_sudoku_list (filename, square_len):
    sudoku_list = []
    with open (filename, 'r') as f:
        index = 0
        solve_count = 0
        for line in f:
            if index == 0:
                sudoku_list = []
            else:
                test_line = [int(line[i]) for i in range(square_len)]
                sudoku_list.append (test_line)
                if len(sudoku_list) == square_len: # sudoku list complete
                    sudoku_item = sudoku_class (sudoku_list)
                    flag, output = solve_sudoku (sudoku_item)
                    solve_count += output
                   
                    
            index = (index + 1) % (square_len + 1)
        return solve_count
def main():
    start_time = time.time()
    filename = "sudoku.txt"
    square_len = 9
    print gen_sudoku_list (filename, square_len)
    print time.time() - start_time
main()
    
    
    
