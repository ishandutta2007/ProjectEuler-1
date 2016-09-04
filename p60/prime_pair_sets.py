# prime_pair_sets.py
# Find the smallest set of 5 primes such that concatenating any pair of them
# yields another prime. Smallest is defined as the sum of the set in this case

import sys, os, inspect, time

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, a)

from factors import gen_prime_list, is_prime

def concat_int (int1, int2):
    str1, str2 = str(int1), str(int2)
    return int(str1 + str2)

def check_is_prime (num, prime_list, max_num):
    if num < max_num:
        if num in prime_list:
            return 1
        return 0

    return is_prime (num)

def prime_pair_concat (prime_list):

    prime_concat_dict = {}
    max_prime = max (prime_list)
    
    for index in xrange(len(prime_list)-1):
        prime_concat_dict[prime_list[index]] = []
        for j in xrange (index+1, len(prime_list)):
            prime1 = concat_int (prime_list[index], prime_list[j])
            prime2 = concat_int (prime_list[j], prime_list[index])
            if check_is_prime (prime1, prime_list, max_prime) and check_is_prime (prime2, prime_list, max_prime):
                prime_concat_dict[prime_list[index]].append (prime_list[j])

    prime_concat_dict[max_prime] = []
    return prime_concat_dict
    

start_time = time.time()
max_num = 10000
prime_list = []
gen_prime_list (max_num, prime_list)

concat_prime_dict = prime_pair_concat (prime_list)

for prime in prime_list:
    for prime2 in concat_prime_dict[prime]:
        for prime3 in list(set(concat_prime_dict[prime]) & set(concat_prime_dict[prime2])):
            for prime4 in list(set(concat_prime_dict[prime]) & set(concat_prime_dict[prime2]) & set(concat_prime_dict[prime3])):
                for prime5 in list(set(concat_prime_dict[prime]) & set(concat_prime_dict[prime2]) & set(concat_prime_dict[prime3]) & set(concat_prime_dict[prime4])):
                    print prime, prime2, prime3, prime4, prime5
                    print sum([prime, prime2, prime3, prime4, prime5])
                    
print time.time() - start_time
