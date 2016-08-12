# double_base_palindromes.py

def check_palindrome (test_str):

    if list(test_str) == list(reversed(test_str)):
        return 1
    return 0

pal_sum = 0
min_num = 1
max_num = 1000000

for i in range(min_num, max_num, 2): # number has to be odd for pal in binary
    if str(i)[0] != str(i)[-1]:
        continue
    if check_palindrome (str(i)) == 1:
        if check_palindrome (str(bin(i)[2:])) == 1:
            # print i
            pal_sum += i

print pal_sum

