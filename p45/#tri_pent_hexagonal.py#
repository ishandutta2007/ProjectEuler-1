# tri_pent_hexagonal.py
# Find the second number that is triangular, pentagonal, and hexagonal

# 24n + 1 perfect square is equivalent to n a pentagon number
# as long as sqrt(24*n + 1) is 5 mod 6
def check_if_pentagon (num):
    test = (24 * num) + 1
    test_root = test ** 0.5
    if int(test_root) == test_root:
        if test_root % 6 == 5:
            return 1
    return 0
# 8k + 1 perfect square equivalent to triangular
def check_if_triangular (num):
    test = 8 * num + 1
    if (test ** 0.5) == (int) (test ** 0.5):
        return 1
    return 0

# cycle through the hexagonal numbers until finding a match
index = 144  # 143 is index of the first match
flag = 0
while flag == 0:
    hex_num = index * (2 * index - 1)
    if check_if_triangular (hex_num) == 1:
        if check_if_pentagon (hex_num) == 1:
            print hex_num, index
            flag = 1
    index += 1
    
    
