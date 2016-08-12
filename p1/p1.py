# Sum all multiples of 3 and 5 less than 1000
# p1.py

max_num = 1000

sum = 0
i = 1
test_num = 3*i
while test_num < 1000:
    sum += test_num
    i += 1
    test_num = 3*i


i = 1
test_num = 5*i
while test_num < 1000:
    if test_num % 15 != 0:
        sum += test_num
    i += 1
    test_num = 5*i

print sum;
