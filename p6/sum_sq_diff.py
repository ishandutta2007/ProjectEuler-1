# sum_sq_diff.py
# Diff b/w sum of squares and square of sum of first 100 naturals

min_num = 1
max_num = 100

gen = (x**2 for x in range(max_num+1))
sum_squares = sum (gen)

square_sum = sum (range(max_num+1)) ** 2

print square_sum - sum_squares
