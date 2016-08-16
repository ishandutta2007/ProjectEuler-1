# lychrel_numbers.py
# How many lychrel numbers below 10000
# Lychrel = numbers where you add the reverse of the number,
# and never end up with a palindrome

def gen_reverse_num (num):
    rev_str = list(reversed (str(num)))
    return int("".join(rev_str))

def is_palindrome (num):
    if num == gen_reverse_num(num):
        return 1
    return 0

max_num = 10000
lychrel_count = 0
max_palindrome_iter = 50

for i in xrange(1, max_num):
    iter_count = 0
    num = i
    while iter_count < max_palindrome_iter and is_palindrome (num + gen_reverse_num(num)) == 0:
        num += gen_reverse_num(num)
        iter_count += 1
    if iter_count == max_palindrome_iter:
        lychrel_count += 1
print lychrel_count
        

