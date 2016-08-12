# integer_right_triangles.py
# Find integer perimeter p <= 1000 such that
# it has the most possible right triangles
# with integral sides

# assumes c is maximum
def check_rt_triangle (a, b, c):
    if c**2 == (a**2 + b**2):
        return 1
    return 0

# Generate possible triangles for perimeter p
def gen_possible_triangles (p):
    if p%2 == 0:
        max_side = p/2-1
    else:
        max_side = p/2

    # We will generate triangles such that c is the longest side,
    # followed by b and a
    # This will ensure unique triangle sets
    
    if p%3 == 0:
        c_min_side = p / 3
    else:
        c_min_side = p / 3 + 1
        
    triangle_list = []
    
    for c in range (c_min_side, max_side+1):
        a = (p - c) / 2
        b = p - a - c
        while a>0 and b<c:
            tri = [a,b,c]
            if a != b:
                triangle_list.append (tri)
            a, b = a-1, b+1
            
    return triangle_list


min_perim = 9
max_perim = 1000
max_count = 0
max_index = 0
for p in range (min_perim, max_perim+1):
    count = 0
    triangle_list = gen_possible_triangles (p)
    for tri in triangle_list:
        if check_rt_triangle (tri[0], tri[1], tri[2]) == 1:
            count += 1
    if max_count < count:
        max_index, max_count = p, count

print max_index, max_count
