# arithmetic_expressions.py
# Find all numbers that can be expressed as arithmetic expressions
# of the set of numbers [a,b,c,d] where a through d are numbers from 0
# through 9
# Expressions are arithmetic operators (+, -, x, /) and parantheses

from itertools import permutations, combinations
import time, operator
from copy import copy

# This inserts the appropriate brackets in the arithmetic expression inputted
# This will also add a '.0' to the integer before if a division symbol if present
def insert_brackets (expr_str, bracket_index):
    curr_insert = '('
    num_digits = 10
    digit_check = set(map(str, range(num_digits)))
    expr_list = list(expr_str)
    i, j = 0, 0
    digits_found = 0

    while True:        
        if expr_list[j] in digit_check and len(bracket_index) > 0:
            digits_found += 1
            if digits_found == bracket_index[i]:
                if curr_insert == '(':
                    expr_list.insert (j, curr_insert)
                    j += 1
                    curr_insert = ')'
                else:
                    j += 1
                    expr_list.insert (j, curr_insert)
                    curr_insert = '('
                i += 1
                if i == len(bracket_index):
                    bracket_index = ()
                
        elif expr_list[j] == '/':
            if expr_list[j-1] == ')':
                j = j-1
            expr_list.insert (j, '0')
            expr_list.insert (j, '.')
            j += 2
            if expr_list[j+1] == '/':
                j += 1
        j += 1
        if j == len(expr_list):
            break
    if check_div_by_zero (expr_list) == 1:
        return 0

    return eval(''.join(expr_list))

# This makes sure that the expression does not contain an implicit zero division
def check_div_by_zero (expr_list):
    expr_str = ''.join(expr_list)
    start_index = expr_str.find ('/(')

    if start_index < 0:
        return 0
    
    start_index += 1
    end_index = expr_str.find (')', start_index)
    test_eval = eval (expr_str[start_index:end_index+1])
    if test_eval == 0:
        return 1
    return 0

# This constructs the evaluated string expression from the inputted digits
# and operations. It also will run through all bracket possibilities
# and return the list of positive integers generated
def eval_all_expressions (digit_list, op_list):
    expr_str = ""
    dig_len, op_len = len(digit_list), len(op_list)
    for i in range (min(dig_len, op_len)):
        expr_str += (str(digit_list[i])+op_list[i])
    if dig_len != op_len:
        if dig_len > op_len:
            expr_str += ''.join(map(str, digit_list[min(dig_len, op_len):]))
        else:
            expr_str += op_list[min(dig_len, op_len):]

    # If all operators are '+' or '*', no need to do brackets
    if len(op_list) == 1 and op_list[0] in ['+', '*']:
    
        return [max(0, eval(expr_str))]
    
    if '*' not in op_list and '/' not in op_list:
        return [max(0,eval(expr_str))]
    
    # Now, we want to evaluate this expression, along with all bracket
    # combinations
    int_list = []
    bracket_combos = [(1,2), (2,3), (3,4), (1,3), (2,4), (1,2,3,4), ()]
    if '+' not in op_list and '-' not in op_list:
        bracket_combos = [(1,2,3,4), ()]
    for bracket in bracket_combos:
        target_num = insert_brackets (expr_str, bracket)
        if int(target_num) == target_num and target_num > 0:
            int_list.append(int(target_num))
    return int_list

# This checks how many consecutive integers 1 to n are in the inputted list
# It checks if this list has as many as the current maximum, and if not, returns zero
def check_consec_int (int_list, curr_max):
    if 0 not in int_list:
        int_list.append(0)
        
    int_list.sort()
    if curr_max >= 0:
        if len(int_list) < (curr_max + 1):
            return 0
        if int_list[curr_max] != curr_max:
            return 0
    list_len = len(int_list)
    if int_list[list_len - 1] == list_len - 1:
        return list_len - 1
    
    min_bound = curr_max
    max_bound = list_len - 1
    check_index = (min_bound + max_bound) / 2
    while True:
        if int_list[check_index] == check_index:
            min_bound = check_index
        else:
            max_bound = check_index
        if min_bound + 1 == max_bound:
            return min_bound
        check_index = (min_bound + max_bound) / 2


def main():
    start_time = time.time()
    
    op_list = ['+', '-', '*', '/']    
    num_dig = 4
    digit_gen = combinations (range(1,10), num_dig)
    curr_max = 0
    for digit_list in digit_gen:
        combo_gen = permutations (digit_list)
        target_list = []
        target_list += [sum (digit_list), reduce (operator.mul, digit_list)]
        for digit_combo in combo_gen:
            for ops in [(x,y,z) for x in op_list for y in op_list for z in op_list]:
                if ops == ('+', '+', '+') or ops == ('*', '*', '*'):
                    continue
                target_list += eval_all_expressions (digit_combo, ops)


        check_max = check_consec_int (list(set(target_list)), curr_max)
        if check_max > curr_max:
            curr_list = copy (digit_list)
            curr_max = check_max
            print check_max
            
    print curr_list, curr_max    
    print time.time() - start_time
main()
