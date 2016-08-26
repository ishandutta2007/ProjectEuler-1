# bouncy_numbers.py
# A number is bouncy if its digits are neither increasing nor decreasing
# Find the number at which the % of bouncy numbers of the total is exactly 99%

def check_increasing_number (num):
    num_list = list(str(num))
    for i in range (len(num_list)-1):
        if num_list[i] > num_list[i+1]:
            return 0
    return 1

def check_decreasing_number (num):
    num_list = list(str(num))
    for i in range (len(num_list)-1):
        if num_list[i] < num_list[i+1]:
            return 0
    return 1


num_bouncy = 0
i = 10
tgt_perc = 0.99

while num_bouncy / (i+0.0) < tgt_perc:
    i += 1
    if (check_increasing_number(i) == 0):
        if (check_decreasing_number(i) == 0):
            num_bouncy += 1
print i
