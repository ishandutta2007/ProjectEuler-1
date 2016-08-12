# max_prod.py
from operator import mul

# takes line of text, converts to list of integers
def format_line (line_in_grid, num_list):
    x = line_in_grid.split (' ')
    for num_str in x:
        if num_str[0] != '0':
            num_list.append(int (num_str))
        else:
            num_list.append(int (num_str[1]))  # 1 digit number


def max_horiz_prod (master_list, line_len):
    max_prod = 0
    for horiz_list in master_list:
        for i in range(len(horiz_list) - line_len):
            max_prod = max(max_prod, reduce (mul, horiz_list[i:i+line_len]))
    return max_prod

def max_vert_prod (master_list, line_len):
    max_prod = 0
    for i in range(len(master_list[0])):
        prod = 1
        for j in range (line_len):
            prod *= master_list[j][i]
        max_prod = max (prod, max_prod)    
    return max_prod

def max_low_diag_prod (master_list, line_len):
    max_prod = 0
    for i in range(len(master_list[0]) - line_len + 1):
        prod = 1
        for j in range (line_len - 1, -1, -1):
            prod *= master_list[j][i+line_len-1-j]
        max_prod = max (max_prod, prod)
    return max_prod

def max_hi_diag_prod (master_list, line_len):
    max_prod = 0
    for i in range(len(master_list[0]) - line_len + 1):
        prod = 1
        for j in range (line_len):
            prod *= master_list[j][i+j]
        max_prod = max (max_prod, prod)
    return max_prod

def calc_max_prod (master_list, line_len):
    return max (max_horiz_prod(master_list, line_len), max_vert_prod(master_list, line_len),
                max_low_diag_prod(master_list, line_len), max_hi_diag_prod (master_list, line_len))
            
filename = "number_grid.txt"
max_prod = 0
max_len = 4

master_list = []
with open (filename, 'r') as f:
    for line in f:
        num_list = []
        format_line (line, num_list)
        master_list.append (list(num_list))
        if len (master_list) > max_len:
            master_list.pop(0)
        if len (master_list) == max_len:
            max_prod = max (max_prod, calc_max_prod (master_list, max_len))

print max_prod
                            
