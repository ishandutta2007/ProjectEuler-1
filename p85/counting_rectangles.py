# counting_rectangles.py
# Find the rectangular grid with the closest number of rectangles
# in the grid to 2 MM

# number of rectangles of size x by y in an n x k rectangle
import math

def num_specific_rectangles (x, y, n, k):
    if x > n:
        return 0
    if y > k:
        return 0

    return ((n-x+1)*(k-y+1))

# num of rectangles of any dimension in an n x k rectangle
def num_total_rectangles (n,k):
    total_rect = 0
    if n <= 0 or k <= 0:
        print "Dimensions less than or equal zero"
        return 0
    for i in xrange(1, n+1):
        for j in xrange (1, k+1):
            total_rect += num_specific_rectangles (i,j,n,k)

    return total_rect

# Given the sum of rectangle dimensions, returns the (x,y) pair
# closest to the target number of total rectangles
def optimal_n_k (height, target, prev_optimal_x):
    x = prev_optimal_x
    y = height - x
    new_best_distance = abs (target - num_total_rectangles (x,y))
    init_x, init_y = x,y
    best_x, best_y = x,y
    x, y = x-1, y+1
    if x < 1:
        return best_x, best_y
    attempted_distance =  abs (target - num_total_rectangles (x,y))

    #  This will lower x by 1 and raise y by 1 to find the best combo
    # with least distance to target
    while attempted_distance < new_best_distance:
        best_x, best_y = x,y
        new_best_distance = attempted_distance
        x, y = x-1, y+1
        if x < 1:
            break
        attempted_distance =  abs (target - num_total_rectangles (x,y))

    x,y = init_x+1, init_y-1
    attempted_distance =  abs (target - num_total_rectangles (x,y))

    while attempted_distance < new_best_distance:
        best_x, best_y = x,y
        new_best_distance = attempted_distance
        x, y = x+1, y-1
        if y < 1:
            break
        attempted_distance =  abs (target - num_total_rectangles (x,y))

    return best_x,best_y

        

target_num = 2 * (10 ** 6)

i = 20
total = 0
# Finds the first n x n rectangle with 2 MM rectangles
while total < target_num:
    i += 1
    total = num_total_rectangles(i,i)

height = i + i - 2  # sum of rectangle dimensions
best_x, best_y = optimal_n_k (height, target_num, height/2)
curr_best_distance = abs(num_total_rectangles(best_x, best_y) - target_num)
opt_x = best_x

i = height + 1
while num_total_rectangles (i,1) < target_num + curr_best_distance:
    opt_x, opt_y = optimal_n_k (i, target_num, opt_x)

    if abs(target_num - num_total_rectangles (opt_x, opt_y)) < curr_best_distance:
        best_x, best_y = opt_x, opt_y
        curr_best_distance =  abs(target_num - num_total_rectangles (opt_x, opt_y))
    i += 1

print best_x, best_y, best_x * best_y, num_total_rectangles (best_x, best_y)
