# harshad_numbers.py
# Find sum of all strong, right truncatable Harshad primes
# below 10 ** 14

import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert(0, home_path + "Utilities/")

from factors import is_prime, gen_prime_list


def calc_digit_sum (num):
    num_str = str(num)
    digit_sum = 0

    for dig in num_str:
        digit_sum += int(dig)
    return digit_sum

# if number is divisible by sum of its digits
def is_harshad (num):

    if num % calc_digit_sum(num) == 0:
        return 1
    return 0

# if number is divisible by sum of its digits
def is_strong_harshad (num):

    if is_harshad(num) == 1:
        if is_prime(num / calc_digit_sum(num)) == 1:
            return 1
    return 0

# right truncate an integer
def rt_truncate_num (num):
    num_str = str(num)
    if len(num_str) == 1:
        return num

    num_str_trunc = num_str[0:-1] 
    return int(''.join(num_str_trunc))

# if number is harshad and taking off right most digit is also
# right truncated harshad
def rt_truncate_harshad (num):
    num_str = str(num)
    if len(num_str) == 1:
        return 1

    if is_harshad(num) == 1:
        return rt_truncate_harshad (rt_truncate_num(num))
    return 0

max_exp = 14
total_sum = 0
rt_harshad_list = [] # list of tuples (harshad num, bool) where 1 indicates strong
prev_rt_harshad_list = [] # list from the previous digit length

for exp in range(max_exp):


    if exp == 0:
        i = 10 ** exp
        while i < 10 ** (exp+1):
            if rt_truncate_harshad (i) == 1:
                rt_harshad_list.append((i,is_strong_harshad(i)))
            i += 1

    if exp > 0:
        for num_pair in prev_rt_harshad_list:
            for j in range(10):
                test_num = num_pair[0] * 10 + j
                test_strong = num_pair[1]

                # look for primes if strong, will imply a strong r.t. Harshad prime
                if test_strong == 1:
                    if j%6 == 1 or j%6 == 7:
                        if is_prime(test_num) == 1:
                            total_sum += test_num


                # test for Harshad numbers, and if strong
                # No need to test for rt_truncate because number choice ensures this
                if is_harshad(test_num) == 1:
                    rt_harshad_list.append ((test_num, is_strong_harshad(test_num)))


    prev_rt_harshad_list = rt_harshad_list
    rt_harshad_list = []
print total_sum
    


