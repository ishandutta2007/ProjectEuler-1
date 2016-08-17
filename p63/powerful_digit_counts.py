# powerful_digit_counts.py
# How many n-digit numbers are nth powers

# Note that the base must always be less than 10
# b/c 10 ** n is an (n+1) digit number

max_base = 10
max_exponent = 21  # Can check that 9 ** 22 is a 21 digit number
num_count = 0
for i in xrange (1, max_base):
    for exp in xrange (1, max_exponent + 1):
        if len(str(i ** exp))  == exp:
            num_count += 1
print num_count
