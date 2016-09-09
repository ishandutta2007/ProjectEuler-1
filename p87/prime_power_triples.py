# prime_power_triples.py
# Find how many numbers below 50 MM can be expressed as the sum of a
# prime square, prime cubed, and a prime raised to the 4th power

import sys, os, inspect, time

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_prime_list

start_time = time.time()
max_num = 50 * (10 ** 6)
prime_list = []
gen_prime_list (int(max_num ** 0.5), prime_list)
total_sum_list = []

for prime2 in prime_list:

    for prime3 in prime_list:
        curr_sum = (prime2 ** 2)
        if prime3 > (max_num - curr_sum) ** (1.0/3):
            break
   

        for prime4 in prime_list:
            curr_sum = (prime2 ** 2 + prime3 ** 3)
            if prime4 >  (max_num - curr_sum) ** (0.25):
                break
            
            final_sum = curr_sum + (prime4 ** 4)
            total_sum_list.append (final_sum)

print len (set (total_sum_list)), len(total_sum_list)
print time.time() - start_time
