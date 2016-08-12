# twenty_grid.py

grid_no = 20
path_count = 0
i = 1
while i < (2**(2*grid_no)):
    num_2 = bin(i)[2:]
    bit_count = 0
    nil_count = 0
    for ch in num_2:
        if ch == '1':
            bit_count += 1
        else:
            nil_count += 1
        if bit_count > grid_no or nil_count > grid_no:
            break
    if bit_count == grid_no:
        path_count += 1
    i += 1
    print i
    
print path_count
