# strong_repunits.py
# Find all numbers which can be represented as a list of only 1's in 2 different
# bases

from bisect import bisect_left

max_num = 10 ** 12
repunit_list = [1]
repunit_sum = 1 # 1 is a repunit which we will not check for


for i in xrange(2, int(max_num ** 0.5)+1):
    index = 2
    curr_repunit = (i**index) + i + 1

    
    while curr_repunit < max_num:

        repunit_list.append(curr_repunit)
        repunit_sum += curr_repunit


        index += 1
        curr_repunit += (i ** index)

print sum(set(repunit_list))

