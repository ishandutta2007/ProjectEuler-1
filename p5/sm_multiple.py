# sm_multiple.py
# Find smallest number divisible by 1-20 inclusive

# Reduce this to finding number divisible by 11-20 inclusive
# Take out the primes (11, 13, 17, 19) and multiply them back in

div_by_all = 0
start_num = 2520
check_list = [12, 14, 15, 16, 18, 20]
prime_list = [11, 13, 17, 19]

test_num = start_num
while div_by_all == 0:
    div_by_all = 1
    for check in check_list:
        if test_num % check != 0:
            div_by_all = 0
            test_num += 20
            break

prod = test_num
for prime in prime_list:
    prod = prod * prime
print prod

