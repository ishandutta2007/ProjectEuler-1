# cuboid_route.py
# Find all prisms with integer sides such that the shortest path
# across the prism is also an integer. Find the height value where
# this number crosses 1 MM


import time

# Dictionary will map m,n Pythagorean triangle generators to their
# x,y values, or non-hypotenuse sides of the triangle
def create_side_dict (max_side):

    side_dict = {}
    max_height = 1 * max_side

    prime_list, sieve_list = gen_co_prime_sieve (max_height)
    for height in range (3, 4 * int(max_height**0.5), 2):
        init_m = height/2 + 1
        for m in range(init_m, height):
            n = height - m
            
            if m % 2 == n % 2: # same parity
                continue
            if check_coprime (m, n, sieve_list, prime_list) == 1:
                k = 1
                x, y = m**2 - n**2, 2*m*n
                while max (k*x, k*y) <= max_height:                 
                    side_dict[(m,n,k)] = (max(k*x,k*y), min(k*x,k*y))
                    k += 1
                    
    return side_dict
            


def gen_co_prime_sieve (max_num):
    prime_list = []
    nums = [0] * (max_num+1)
    for i in range (2, max_num+1):
        if nums[i] == 0:
            prime_list.append (i)
            for j in range (2*i, max_num+1, i):
                if nums[j] == 0:
                    nums[j] = 1, [i]
                else:
                    nums[j][1].append(i)
                    
    return prime_list, nums
                

def check_coprime (m, n, sieve_list, prime_list):
    if n == 1:
        return 1
    
    if m in set(prime_list):
        return 1
    
    if m % n == 0:
        return 0
    
    if n in set(prime_list):
        return 1

    if len (set(sieve_list[m][1]).intersection (set(sieve_list[n][1]))) == 0:
        return 1
    return 0

# Checks that the shortest path across the cuboid is actual integral
def integer_shortest_path (x,y,z):

    side_list = [x,y,z]
    side_sum = sum(side_list)
    min_diag_len = side_sum
    for side in side_list:
        diag_len = (side ** 2 + (side_sum - side) ** 2) ** 0.5
        min_diag_len = min (diag_len, min_diag_len)
    if int(min_diag_len) == min_diag_len:
        return 1
    return 0
    

# Finds all possible triples with a path connecting opposite points of length
# height, and integral sides
def compile_cuboid_list (height, x, y):
    cuboid_list = []
    
    if y == height: # if one equals height, force it to be x
       y = x
       x = height
    
    if x == height:
        for j in range (y/2, 0, -1):
            if y - j <= height:
                cuboid_test = (j, y-j, height)
                if integer_shortest_path (cuboid_test[0], cuboid_test[1],
                                          cuboid_test[2]) == 1:
                    cuboid_list.append (cuboid_test)
        return cuboid_list

    cuboid_test = ((min(x-height, y), max(x-height, y), height))
    if integer_shortest_path (cuboid_test[0], cuboid_test[1],
                              cuboid_test[2]) == 1:
        cuboid_list.append (cuboid_test)
    
    return cuboid_list


def map_height_pairs (height, side_dict):
    
    beg_list = [v for k,v in side_dict.items() if height in v
                and max(v) <= 2 * height]
    oth_list = [v for k,v in side_dict.items() if v[1] < height
                and v[0] >= height+1 and v[0] <= 2*height]

    cuboid_list = []
    for height_pair in (beg_list + oth_list):
        cuboid_list = cuboid_list + compile_cuboid_list (height,
                                                         height_pair[0],
                                                         height_pair[1])
    return len (set(cuboid_list))

def main():
    start_time = time.time()
    
    max_side = 4001
    max_cuboid_num = 1000000
    
    side_dict = create_side_dict(max_side)
    print "Dict done"
    
    cuboid_sum = 0
    for M in range(3, max_side):
        cuboid_sum += map_height_pairs (M, side_dict)
        if cuboid_sum > max_cuboid_num:
            print M, cuboid_sum
            break

    print M, cuboid_sum
    print time.time() - start_time
main()
