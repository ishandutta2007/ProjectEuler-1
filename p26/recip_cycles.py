# recip_cycles.py

def dec_rep_1_over_n (n):
    rem_dict = {}
    num = 10
    dem = n
    remainder = num % n
    index = 1
    
    while remainder not in rem_dict:
        if remainder == 0: # no repeating cycle, terminates
            return 0
        rem_dict[remainder] = index
        num = 10 * remainder
        remainder = num % n
        index += 1

    cycle_len = index - rem_dict[remainder]
    return cycle_len

max_num = 1000
max_cycle = 0, 0
for i in range(1,max_num):
    cycle =  dec_rep_1_over_n (i)
    if cycle > max_cycle[0]:
        max_cycle = cycle, i

print max_cycle
