# amicable_num.py
# Find all amicable numbers below 10000

def sum_all_proper_divisors (n):
    divisor_sum = 1

    if n == 2:
        return divisor_sum
    
    if n % 2 != 0: # don't have to check odd divisors
        incr = 1
    else:
        incr = 1

        divisor_sum += 2
        if (n/2) != 2:
            divisor_sum += (n/2)
        
    for div in range (3, int(n**0.5)+1, incr):
        if n % div == 0:
            divisor_sum += div
            if (n/div) != div:
                divisor_sum += (n/div)
                
    return divisor_sum

# print sum_all_proper_divisors ()

max_num = 10000
sum_factor_dict = {}
sum_factor_dict[1] = 1
amicable_list = []


for i in range (2, max_num):
    sum_factor_dict[i] = sum_all_proper_divisors(i)
    sum_factors = sum_factor_dict[i]
    if sum_factors < i:
        if sum_factor_dict[sum_factors] == i: # amicable
            amicable_list += [i, sum_factors]
            print i, sum_factors

print sum(amicable_list)
