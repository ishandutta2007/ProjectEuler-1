# single_integer_rt_triangles.py

import sys, time

def generate_pyth_triples (m, n, length_dict, total_count, max_num):

    triples_list = []
    final_count = total_count

    L = 0
    k = 1
    while L <= max_num:

        triple = (k * (m ** 2 - n ** 2), k*2*m*n, k * (m ** 2 + n ** 2))
        L = sum (triple)

        if L <= max_num:
            if L not in length_dict:
                length_dict[L] = triple
                final_count += 1

            else:
                if length_dict[L] != 0:
                    final_count -= 1
                    length_dict[L] = 0
        k += 1
        
    return final_count, length_dict

def gen_co_prime_sieve (max_num):
    prime_list = []
    nums = [0] * (max_num+1)
    for i in range (2, max_num+1):
        if nums[i] == 0:
            prime_list.append (i)
            for j in range (2*i, max_num+1, i):
                if nums[j] == 0:
                    nums[j] = 1, [i]
                else:
                    nums[j][1].append(i)
                    
    return prime_list, nums
                

def check_coprime (m, n, sieve_list, prime_list):
    if n == 1:
        return 1
    
    if m in set(prime_list):
        return 1
    
    if m % n == 0:
        return 0
    
    if n in set(prime_list):
        return 1

    if len (set(sieve_list[m][1]).intersection (set(sieve_list[n][1]))) == 0:
        return 1
    return 0
    

def main():
    start_time = time.time()
    max_num = 1500000
        
    final_count, length_dict = 0, {}
    
    prime_max = int ((max_num / 2) ** 0.5)
    prime_list, sieve_list = gen_co_prime_sieve (prime_max)
    
    for n in xrange(1, prime_max): 
        for m in xrange (n+1, prime_max+1, 2):
            if check_coprime (m, n, sieve_list, prime_list) == 1:
                final_count, length_dict = generate_pyth_triples (m,n, length_dict, final_count, max_num)
         
    print final_count, time.time() - start_time
    
main()

        
