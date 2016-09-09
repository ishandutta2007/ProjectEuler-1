# reversible_numbers.py
# Reversible is defined as when a number added to its palindrome has only
# odd digits
# How many reversible numbers are there below 10 ** 9

import time


def check_odd_digits (num):
    num_str = str(num)
    for ch in num_str:
        if int(ch) % 2 == 0:
            return 0
    return 1

# Recursive algo generating possible reversible numbers
# by checking the consequences of choices
def count_reversible_nums (num_digit_list, rev_digit_list, next_index, carry, last_digit):

    num_len = len (num_digit_list)
    possible_digits = 10
    
    # End case
    if num_digit_list[num_len/2] >= 0:
        num_str_list = [str(ch) for ch in num_digit_list]
        rev_str_list = [str(ch) for ch in rev_digit_list]
        
        num = int(''.join(num_str_list))
        rev_num =  int(''.join(rev_str_list))

        if check_odd_digits (num + rev_num) == 1:

            return 1
        return 0

    total_count = 0

    num_test_list = num_digit_list[:]
    rev_test_list = rev_digit_list[:]
    test_carry = carry
    
    if next_index < ((num_len-1) / 2.0):
        if next_index == 0:
            start_dig = 1
        else:
            start_dig = 0
            
        for test_dig in range (start_dig, possible_digits):
            num_test_list[next_index] = test_dig
            rev_test_list[num_len - next_index - 1] = test_dig

            total_count += count_reversible_nums (num_test_list, rev_test_list,
                                                  num_len - next_index - 1, test_carry, test_dig)

            
    elif next_index > ((num_len-1) / 2.0):
        if (test_carry + last_digit) % 2 == 1:
            if next_index == (num_len - 1):
                start_dig = 2
            else:
                start_dig = 0
        else:
            start_dig = 1

        if next_index == num_len - 2:
            end_digit = 9 - last_digit # cannot sum up to more than 10
        else:
            end_digit = 9
            
        # By definition, this digit plus its opposite digit (which is chosen)
        # plus a carry variable must end
        # in an odd number. So we can choose the range appropriately

        for test_dig in range (start_dig, end_digit+1, 2):

            num_test_list[next_index] = test_dig
            rev_test_list[num_len - next_index - 1] = test_dig
            if last_digit + test_dig + test_carry >= possible_digits:
                carry = 1
            else:
                carry = 0

            total_count +=  count_reversible_nums (num_test_list, rev_test_list,
                                                   num_len - next_index, carry, test_dig)

    elif next_index == (num_len - 1) / 2.0:
        if carry == 0:
            return 0
        for test_dig in range (0, possible_digits):
           num_test_list[next_index] = test_dig
           rev_test_list[num_len - next_index - 1] = test_dig
           carry = 0
           
           # carry and next_index are irrelevant because all digits are filled at this point
           total_count +=  count_reversible_nums (num_test_list, rev_test_list,
                                                   next_index, carry, test_dig)
    return total_count

start_time = time.time()
total_count = 0
max_digits = 9
for num_digits in range (2, max_digits+1):
    if num_digits == 5 or num_digits == 9:
        continue
    num_digit_list = [-1] * num_digits
    rev_digit_list = [-1] * num_digits
    next_index = 0
    carry = 0
    last_digit = -1
    total_count += count_reversible_nums (num_digit_list, rev_digit_list, next_index, carry, last_digit)

print total_count
print time.time() - start_time
