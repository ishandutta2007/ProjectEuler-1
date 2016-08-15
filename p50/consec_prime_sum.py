# consec_prime_sum.py
# Find the prime less than 1 MM which can be represented
# as the sum of the most consecutive primes

from bisect import bisect_left
import sys
home_path = "/home/osboxes/ProjEuler/"
sys.path.insert (0, home_path + "Utilities/")

from factors import gen_prime_list

# Make a list which is the running sum of the prime list
def running_sum_list (prime_list):

    i = 1
    running_sum = 0
    running_list = []
    running_list.append(prime_list[0])
    
    while i < len(prime_list):
        
        running_list.append(prime_list[i] + running_list[i-1])
        i += 1
    return running_list

# find longest list of consecutive numbers that equals num
# Running sum of list is passed to the function
def find_longest_consec (num, running_list, min_list_len):

    # Find the index from the beginning of list which equals num

    longest_list_len = bisect_left (running_list, num)
    if num in set(running_list):
        return num, longest_list_len + 1

    buffer = 5
    for i in range (longest_list_len, min_list_len, -1):
        # Find approx start point
        approx_start_index = bisect_left (running_list, num / i) - i/2
        start_index = max (approx_start_index - buffer, 0)
        consec_sum = 0
        while consec_sum < num:
            consec_sum = running_list[start_index+i] - running_list[start_index]
            if consec_sum == num:

                return num, i
            start_index += 1
    return num, 0
# Won't need more consecutive primes than this 
# as we know the list is more than 20

max_num = 1000000
min_num = 1000
prime_list = []
gen_prime_list (max_num, prime_list)

end_pos = bisect_left (prime_list, max_num/10) 
running_sum_iter = running_sum_list (prime_list[:end_pos])

prime_index = bisect_left (prime_list, min_num)
prime_list = prime_list[prime_index-1:]
min_list_len = 21  # given in problem
max_consec_len = [0,min_list_len]
for prime in prime_list:
    test_prime, consec_len = find_longest_consec (prime, running_sum_iter, max_consec_len[1])
    if consec_len > max_consec_len[1]:
        max_consec_len = test_prime, consec_len
print max_consec_len

