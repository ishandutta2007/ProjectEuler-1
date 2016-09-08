# square_root_digital_expansion.py
# Find the sum of the first 100 digits after the decimal point
# for all irrational square roots up to 100
import time

def square_list (num):
    tgt_list = []
    i = 1
    while i * i <= num:
        tgt_list.append (i*i)
        i += 1
    return tgt_list

# Gets the first target_len decimal digits of the square root of the inputted number
# Does this by multiplying the number by 10**2, and finding the next digit of that
# square root

def sq_root_decimal_sum (num, target_len):

    digit_len = 0
    int_root = int (num ** 0.5)
    new_num = num
    curr_num = int_root

    digit_sum = 0
    for dig in str(int_root):
        digit_sum += int(dig)
        digit_len += 1
    
    while digit_len < target_len:
        new_num *= 100
        curr_num *= 10
        for i in range(10):
            if i == 9:
                next_num = 9
                break
            if (curr_num + i) ** 2 < new_num and (curr_num + i + 1) ** 2 > new_num:
                next_num = i
                break
        curr_num += i
        digit_len += 1
        digit_sum += i
    return digit_sum
start_time = time.time()
target_len = 100
target_num = 100
sq_set = set(square_list (target_num))
dig_sum_total = 0

for i in range (1, target_num + 1):
    if i in sq_set:
        continue
    dig_sum_total += sq_root_decimal_sum (i, target_len)

print dig_sum_total
print time.time() - start_time
