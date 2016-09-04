# cyclical_figurate_numbers.py
# Find 6 numbers such that one is triangular, square, pentagonal, hexagonal,
# septagonal, and octagonal
# And the last two digit of one number form the first two digits of another uniquely

import time

def tri (n):
    return (n * (n+1))/2
def squ (n):
    return n * n
def pent (n):
    return (n * (3 * n - 1)) / 2
def hexag (n):
    return n * (2 * n - 1)
def sept (n):
    return n * (5 * n - 3) / 2
def octo (n):
    return n * (3 * n - 2)

def figurate_dict_list (min_num, max_num, func):

    # triangular
    dict1 = {}
    n = 1
    while func(n) < min_num:
        n += 1
    while func(n) < max_num:
        if (func(n) / 100) not in dict1:
            dict1[func(n)/100] = [func(n) % 100]
        else:
            dict1[func(n)/100].append (func(n) % 100)
        n += 1
    return dict1

def find_figurate_list (dict_list, num_list = []):

    if len (dict_list) == 1:
        last_two_digits = num_list[-1] % 100
        if last_two_digits in dict_list[0]:
            for nums in dict_list[0][last_two_digits]:
                final_num = 100 * last_two_digits + nums
                # check if last two digits are the first two digits of the first number
                final_last_digits = final_num % 100
                if final_last_digits == (num_list[0] / 100):
                    num_list.append (final_num)
                    print sum(num_list), num_list
                    return 1
            return 0
        else:
            return 0
        
    
    if len(num_list) == 0:  # start with oct, go from there
        total_count = 0
        index = len(dict_list)
        new_dict_list = dict_list[:-1]
        
        for nums in dict_list[index-1]:
            
            end_val = dict_list[index-1][nums][0]
            dict_index = 0    
            for dict_item in new_dict_list:

                if end_val in dict_item:
                    next_dict_list = new_dict_list                        
                    next_num_list = [100 * nums + end_val]
                    total_count += find_figurate_list(next_dict_list, next_num_list)
                    
                dict_index += 1

    else:
        last_two_digits = num_list[-1] % 100
        total_count = 0
        dict_index = 0
        new_dict_list = dict_list

        for dict_item in new_dict_list:
            if last_two_digits in dict_item:
                
                if dict_index == len(new_dict_list) - 1:
                    next_dict_list = new_dict_list[:dict_index]
                else:
                    next_dict_list = new_dict_list[:dict_index] + new_dict_list[dict_index+1:]
                    
                for val in dict_item[last_two_digits]:
                    next_num_list = [100 * last_two_digits + val]
                    total_count += (find_figurate_list(next_dict_list, num_list + next_num_list))
                
            dict_index += 1


    return total_count

start_time = time.time()
func_list = [tri, squ, pent, hexag, sept, octo]
dict_list = []
for func in func_list:
    dict_list.append(figurate_dict_list (1000, 10000, func))

find_figurate_list (dict_list)
print time.time() - start_time

