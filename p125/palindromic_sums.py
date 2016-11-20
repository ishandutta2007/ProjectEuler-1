# palindromic_sums.py
# Find all palindromes below 10**8 that can be written as the sum of
# consecutive squares
import time
from bisect import bisect_left


# outputs list of palindromes with num_digits digits
def gen_palindromes (num_digits):
    if num_digits == 1:
        first_num, last_num = 1,9 
        return range(first_num,last_num+1) # all 1 digit numbers are palindromes


    init_num_digits = num_digits/2
    if num_digits % 2 == 1:
        init_num_digits += 1
        rev_digit_amt = init_num_digits - 1
    else:
        rev_digit_amt = init_num_digits
    init_nums = gen_all_nums (init_num_digits)
    palindrome_list = create_palindrome (init_nums, rev_digit_amt)

    return palindrome_list

# This generates a list of all possible numbers with the inputted digit length
def gen_all_nums (num_digits):
    first_num = 10 ** (num_digits - 1)
    last_num = 10 ** num_digits - 1
    return range (first_num, last_num + 1)

# Given a list of numbers, this generates the number formed by reversing the
# first rev_digit_amt digits, and adds this to the tail of the initial number,
# forming a palindrome. Returns list of palindromes
def create_palindrome (num_list, rev_digit_amt):
    pal_list = []

    for num in num_list:
        num_str = list(str(num))
        tail_num_iter = reversed (num_str[0:rev_digit_amt])
        for dig in tail_num_iter:
            num_str.append(dig)
        pal_list.append (int(''.join(num_str)))
    return pal_list
#------------------------------------------------------------------------------

# Returns the sum of first_num**2 + (first_num+1)**2 + ... last_num**2
# Uses function sum_first_n_squares to do this very quickly
def sum_consec_squares (first_num, last_num):
    return sum_first_n_squares (last_num) - sum_first_n_squares(first_num-1)

# Formula for sum of first n squares starting at 1. This will expedite checking
# sums of arbitrary lengths of consecutive squares
def sum_first_n_squares (n):
    return ((n * (n+1) * (2*n + 1)) / 6)
#-------------------------------------------------------------------------------

# This generates a list such that the nth member is the sum of 1**2 + ... + n^2
# This will give the program a max limit as to length of consecutive sums
# it must check
def first_n_square_sum (max_num):

    n = 0
    square_sum_list = []
    square_sum =  sum_first_n_squares (n)
    while square_sum < max_num:
        square_sum_list.append (square_sum)
        n += 1
        square_sum =  sum_first_n_squares (n)
    return square_sum_list
#-----------------------------------------------------------------------------

# This calculates the remainder of any i consecutive squares mod i
# where i ranges from 1 to n
# If a number is not equal to this remainder mod i, it cannot be the sum of
# i consecutive squares
def remainder_consecutive_squares (n):
    mod_list = [0,0] # this covers cases for i=0 and i=1

    for i in xrange (2, n+1):
        consec_list = range(i)
        remainder = sum ([(x**2) % i for x in consec_list])
        mod_list.append (remainder % i)
    return mod_list
#-----------------------------------------------------------------------------

# This checks each palindrome in the list if it's the sum of consecutive
# squares. It checks the mod_list to see which consecutive lengths are
# possible. Then it checks if any of those lengths works among squares
def find_square_sums (palindrome_list, square_sum_list, sq_sum_set, mod_list):
    square_list = []
    for pal in palindrome_list:
        if pal in sq_sum_set: # represented as sum of 1**2 +...+ n**2
            square_list.append (pal)
            continue

        max_possible_len = bisect_left (square_sum_list, pal)
        pal_mod_list = [0] + [pal % i for i in xrange(1, max_possible_len)]
        comp_mod_list = zip (pal_mod_list, mod_list[:len(pal_mod_list)])
        comp_index_list = [i for i in range(len(comp_mod_list))
                           if comp_mod_list[i][0] == comp_mod_list[i][1]]
        
        comp_index_list = comp_index_list[2:]  # gets rid of 0 and 1 cases

        for comp in comp_index_list:
            if is_sum_n_consec_squares (pal, comp) == 1:
                square_list.append (pal)
                break
    return square_list
# Checks if inputted num is the sum of n consecutive squares
def is_sum_n_consec_squares (num, n):
    mid_index = int((num / n) ** 0.5)
    first_index = mid_index - (n/2)
    end_index = mid_index + (n/2)
    if n % 2 == 0:
        first_index += 1

    if first_index < 1: # this is the only possibility
        first_index = 2
        end_index = n+1
        if num == sum_consec_squares (first_index, end_index):
            return 1
        return 0

    init_diff = num -  sum_consec_squares (first_index, end_index)

    while init_diff < 0:
        first_index, end_index = first_index - 1, end_index - 1
        init_diff = num -  sum_consec_squares (first_index, end_index)
        if first_index == 1:
            return 0

    if init_diff == 0:
        return 1
    return 0
    
    

def main():
    start_time = time.time()
    max_num = 10**8
    max_digit_len = len(str(max_num-1))

    square_sum_list = first_n_square_sum (max_num)
    sq_sum_set = set(square_sum_list)
    sq_sum_set.remove(1) # 1 cannot be the sum of 2 positive squares
    
    mod_list = remainder_consecutive_squares (len(square_sum_list))
    
    square_pal_list = []
    for num_digits in xrange(1, max_digit_len+1):
        palindrome_list = gen_palindromes (num_digits)
        square_pal_list += find_square_sums (palindrome_list, square_sum_list,
                          sq_sum_set, mod_list)
    print sum(square_pal_list)
    print time.time() - start_time
main()
