# sum_digits.py

num = 2 ** 1000
dig_sum = 0

for dig in str(num):
    dig_sum += int(dig)
print dig_sum
