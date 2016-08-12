# find_prime.py
# Find 10,001st prime

def check_prime (num, prime_list):
    for prime in prime_list:
        if num % prime == 0:
            return 0
        if prime > (num ** 0.5):
            return 1
    return 1

prime_list = [2,3]
test_num = 5
prime_list_len = 2

while prime_list_len < 10001:
    if check_prime (test_num, prime_list) == 1:
        prime_list.append (test_num)
        prime_list_len += 1
    test_num += 2

print prime_list[-1]
