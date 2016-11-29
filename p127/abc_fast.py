# abc_fast.py
# Find all solutions (a,b,c) for c < 120000
# a + b = c, all rel prime, and rad(abc) < c

import sys, os, inspect, time, operator
from bisect import bisect_left, bisect_right
from math import log

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_co_prime_sieve

# By checking radical, of all nums in the list, it returns the suitable
# candidates for abc hits
def calc_radical_ratios (num_list, prime_list):
    c_possible_list = []
    prime_set = set(prime_list)
    
    for i in range(2, len(num_list)):
        
        if i in prime_set:
            continue
        factor_list = num_list[i][1]
        radical = reduce (operator.mul, factor_list)
        # If c even, a and b must be odd hence 2 cannot be a prime factor
        # of either. prime_list[0] == 2 so must be excluded
        test_prime_list = []
        if i % 2 == 0:
            j = 1 # both summands must be odd so 2 cannot be one of the primes
            while len(test_prime_list) < 2:
                if prime_list[j] not in factor_list:
                    test_prime_list.append(prime_list[j])
                j += 1
                                        
                
            if i / radical >= reduce (operator.mul, test_prime_list):
                c_possible_list.append(i)
        
        else:
            j = 0  # 2 is a valid prime to check
            while len(test_prime_list) < 2:
                if prime_list[j] not in factor_list:
                    test_prime_list.append(prime_list[j])
                j += 1
            if i / radical >= reduce(operator.mul, test_prime_list):
                c_possible_list.append(i)
    return c_possible_list
#-----------------------------------------------------------------------------
# Returns a dictionary mapping any pair of distinct prime numbers to a sorted
# list of all numbers containing exactly those two primes as factors
# Primes are capped by max_prime, products are capped by max_num
def pair_prime_factor_nums (prime_list, max_prime, max_num):
    pair_prime_dict = {}
    max_index = bisect_left (prime_list, max_prime)
    for i in range(max_index):
        p_i = prime_list[i]
        for j in range(i+1, max_index):
            p_j = prime_list[j]
            prod_list = []
            for j_exp in range(1, int(log(max_num) / log(p_j)) + 1):
                max_i_exp = int(log (max_num / p_j ** j_exp) / log(p_i))
                if max_i_exp > 0:
                    test_list = [((p_i**i_exp) * (p_j ** j_exp), i_exp, j_exp)
                             for i_exp in range(1, max_i_exp + 1)]
                    prod_list += test_list
            prod_list.sort(key=operator.itemgetter(0))
            pair_prime_dict[(p_i,p_j)] = []
            pair_prime_dict[(p_i,p_j)].append([prod[0] for prod in prod_list])
            pair_prime_dict[(p_i,p_j)].append([[prod[1], prod[2]] for prod
                                               in prod_list])
        
    return pair_prime_dict
#---------------------------------------------------------------------------    

def check_possible_c (c_num, c_factors, prime_list, num_list,
                      pair_prime_dict, max_num):

    radical = reduce (operator.mul, c_factors)
    rad_ratio = c_num / (1.0*radical)
    prod, count = 1, 0
    i = 1 - (c_num % 2) # if c_num odd, 2 (prime_list[0]) will be present
                        # among a or b.
                        # Otherwise it cannot be (violates rel prime)
    
    while prod < rad_ratio:
        if prime_list[i] not in c_factors:
            prod *= prime_list[i]
            count += 1
        i += 1
    
    max_num_primes = count - 1  # max_primes across a and b in total
    min_num_primes = 1 # must be at least one prime factor in a and b

    candidate_prime_list = prime_list[:]
    for factor in c_factors:
        candidate_prime_list.remove(factor) # only checks for valid primes

    c_count = 0
    for prime_count in range(min_num_primes, max_num_primes + 1):
         prime_tuple_list = calc_possible_prime_sets (candidate_prime_list,
                                                      rad_ratio, prime_count)
         for prime_tuple in prime_tuple_list:
             exp_list = find_valid_exponents (prime_tuple, c_num,
                                              pair_prime_dict,
                                              max_num)

             num_c = check_a_b (prime_tuple, exp_list, c_num,
                                num_list, rad_ratio)
             c_count += num_c
             
    return c_count

# Lists all possible sets of primes of size prime_count that could form
# the radical for "b", the larger of a and b

def calc_possible_prime_sets (candidate_prime_list, rad_ratio,
                              prime_count, curr_list = [], last_index = 0):

    max_product = rad_ratio / candidate_prime_list[0]
    
    # Base case
    if len(curr_list) == prime_count:
        if reduce(operator.mul, curr_list) < max_product:

            return [tuple(curr_list)]
        else:
            return ()

    remaining_nums = prime_count - len(curr_list)
    if len(curr_list) == 0:
        min_index = 0
        max_index = bisect_left (candidate_prime_list,
                                 max_product ** (1.0 / prime_count))
    else:
        min_index = last_index + 1
        curr_prod = reduce (operator.mul, curr_list)
        max_prime_est = ((max_product / (1.0*curr_prod)) **
                         (1.0 / remaining_nums))
        max_index = bisect_left (candidate_prime_list,
                                 max_prime_est)
    prime_tuple_list = []
    for i in range(min_index, max_index):
        new_list = curr_list[:]
        new_list.append(candidate_prime_list[i])
        prime_tuple_list +=  calc_possible_prime_sets (candidate_prime_list,
                                                       rad_ratio,
                                                       prime_count, new_list,
                                                       i)
    return prime_tuple_list

# Find exponents applied to each prime in the tuple such that the product
# of the tuple is greater than c/2 and less than c
def find_valid_exponents (prime_tuple, c_num, pair_prime_dict, max_num):
    # Base case - tuple length is 1 or 2

    if len(prime_tuple) == 1:
        prime_num = prime_tuple[0]
        if int(log(c_num)/log(prime_num)) == int((log(c_num/2.0)/log(prime_num))):
            return []
        else:
            return [[int(log(c_num)/log(prime_num))]]
    if len(prime_tuple) == 2:
        prime1, prime2 = prime_tuple[0], prime_tuple[1]
        if prime2 < max_num ** 0.5: # both primes in pair_dict
            prod_list = pair_prime_dict[(prime1, prime2)][0]
            exp_list = pair_prime_dict[(prime1, prime2)][1]
            low_index = bisect_left (prod_list, c_num/2.0)
            high_index =  bisect_left (prod_list, c_num)
            if low_index == high_index:
                return []
            else:
                return exp_list[low_index:high_index]
        else: # prime2 > sqrt(max_num) means its exponent must be one
            part_list = find_valid_exponents ([(prime1)], c_num / (1.0*prime2),
                                              pair_prime_dict, max_num)
            if part_list == []:
                return []
            else:
                two_exp_list = []
                for part in part_list:
                    two_exp_list.append (part + [1])
                return two_exp_list
            
    # If tuple is larger than two elements, use recursion
    # to ultimately reduce to two element case
    # Work backward from largest primes to smallest
    full_exp_list = []
    min_exp = 1
    max_exp = int(log(c_num / (1.0*reduce(operator.mul, list(prime_tuple)[:-1]))))

    for exp_n in range(min_exp, max_exp + 1):
        part_list = find_valid_exponents (list(prime_tuple)[:-1],
                                          (1.0*c_num) / (prime_tuple[-1] ** exp_n), 
                                          pair_prime_dict, max_num)
        if part_list != []:
            for part in part_list:
                full_exp_list.append(part + [exp_n])
            
    return full_exp_list

# Given exponents that will make the product of the prime tuple greater than
# c_num / 2, program checks if a, c_num - b, has suitable factors such that
# rad(a) * rad(b) < rad_ratio
def check_a_b (prime_tuple, exp_list, c_num, num_list, rad_ratio):
    c_count = 0
    for exp_poss in exp_list:
        b = reduce (operator.mul, [prime_tuple[i] ** exp_poss[i] for
                                   i in range(len(prime_tuple))])
        radical_b = reduce (operator.mul, prime_tuple)

        a = c_num - b
        if a == 1:
            continue
        if num_list[a] == 0: # prime
            radical_a = a
        else:
            radical_a = reduce (operator.mul, num_list[a][1])
        if radical_a * radical_b < rad_ratio:
            c_count += 1
    return c_count
#----------------------------------------------------------------------------------

def radical (num, factor_list):
    return reduce (operator.mul, factor_list)

def main():
    start_time = time.time()
    max_num = 120000
    prime_list, num_list = gen_co_prime_sieve (max_num)
    prime_set = set(prime_list)
    
    pair_prime_dict = pair_prime_factor_nums (prime_list, max_num ** 0.5,
                                              max_num)
    c_possible_list = calc_radical_ratios (num_list, prime_list)
    c_count = 0

    for c_num in range(2, max_num):
        # test b = c_num - 1
        b = c_num - 1
        if b in prime_set or c_num in prime_set:
            continue
        else:
            b_factor = num_list[b][1]
            
        c_factor = num_list[c_num][1]
        if radical (b, b_factor) * radical(c_num, c_factor) < c_num:
            c_count += c_num
    
    for c_num in c_possible_list:
        c_factor = num_list[c_num][1]
        c_count +=  (c_num * check_possible_c (c_num, c_factor, prime_list,
                                               num_list, pair_prime_dict,
                                               max_num))
    print c_count
    print time.time() - start_time
    
main()
    
