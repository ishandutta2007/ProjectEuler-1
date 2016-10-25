# arranged_probability.py
import time
start_time = time.time()
sqrt_2 = 2 ** 0.5
min_num = sqrt_2 - sqrt_2 / (10 ** 12)
max_num = sqrt_2 - 1.0 / (10 ** 12)
k = 10 ** 6
curr_min, curr_max = min_num, max_num
while k < 3 * 10**8:
    k += 1
    curr_min = min_num * k
    curr_max = max_num * k
    if int(curr_min) != int(curr_max):
        # print k, " success"
        pass
    if k % 10 ** 8 == 0:
        print k
print time.time() - start_time

