# spiral_primes.py
# Find length of square where primes on diagonals fall below 10% of
# total numbers on the diagonal

home_path = "/home/osboxes/ProjEuler/"
import sys
sys.path.insert (0, home_path + "Utilities/")

from factors import is_prime

prime_perc = 1
perc_thresh = 0.1
index = 1
end_num = 1
side_len = 1
prime_count = 0
while prime_perc > perc_thresh:
    diag_diff = 2 * index
    side_len += 2
    index += 1
    
    for i in range(4):
        end_num += diag_diff
        if is_prime(end_num) == 1:
            prime_count += 1
            
    prime_perc = prime_count  / (side_len * 2 - 1.0)

print side_len
