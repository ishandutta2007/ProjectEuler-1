# num_spiral_diag.py

def corner_numbers (n, num_list):
    num_list.append (n * n)
    increment = n - 1
    for i in range(1,4):
        num_list.append ((n * n) - (i * increment))
    return sum (num_list)

max_spiral = 5
corner_sum = 1 # middle
for i in range(3,max_spiral+1,2):
    num_list = []
    corner_sum += corner_numbers (i, num_list)

print corner_sum
