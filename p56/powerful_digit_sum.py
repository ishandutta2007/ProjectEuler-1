# powerful_digit_sum.py
# Find number a^b, a,b < 100, having largest digital sum

def calc_digital_sum (num):
    dig_sum = 0
    for dig in str(num):
        dig_sum += int(dig)
    return dig_sum

max_dig_sum = 0
max_num = 100
for a in xrange(1,max_num):
    for b in xrange (1,max_num):
        max_dig_sum = max (max_dig_sum, calc_digital_sum(a ** b))
print max_dig_sum
