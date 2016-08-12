# sum_digits.py
# Find sum of digits in 100!

import math

def digit_sum (n):
    dig_sum = 0
    for ch in str(n):
        dig_sum += int(ch)
    return dig_sum

print digit_sum(math.factorial(100))

# Calculate 100! without the end zeroes
factorial_alt = 1
for i in range(1, 101):
    if i % 10 == 0:
        if i % 100 == 0:
            factorial_alt *= (i/100)
        elif i % 50 == 0:
            factorial_alt *= (i/50)
        else:
            factorial_alt *= (i/10)
        continue

    if i % 5 == 0:
        if i % 25 == 0:
            factorial_alt *= (i/25)
        else:
            factorial_alt *= (i/5)
        continue
    
    if i == 64 or i == 32 or i == 4:
        continue
    factorial_alt *= i
    
print digit_sum (factorial_alt), len (str(factorial_alt))
