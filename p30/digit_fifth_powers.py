# digit_fifth_powers.py

def get_digits (num, dig_list):
    for ch in str(num):
        dig_list.append(int(ch))

def check_condition (num, dig_list):
    dig_pow_sum = 0
    for x in dig_list:
        dig_pow_sum += (x ** 5)
    if dig_pow_sum == num:
        return 1
    return 0


max_digit = 9
max_num = (max_digit ** 5) * 6  # max number that can satisfy the condition
target_list = []

for num in range (100, max_num):
    dig_list = []
    get_digits (num, dig_list)
    if check_condition (num, dig_list) == 1:
        target_list.append (num)

print sum(target_list), len(target_list), target_list
