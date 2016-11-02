# pandigital_fibonacci_ends.py
# Find the index of the first Fibonacci number such that its
# first 9 digits are pandigital and its last 9 are pandigital

import time

# Formula to calculate nth Fibonacci number and return its first
# num pandigital digits
def fib_calc_first_digits (n, num_pandigital):
    phi = (1 + 5 ** 0.5) / 2

    fib_n = (phi ** n - ((-1 * phi) ** (-1*n))) / (5 ** 0.5) 

    fib_len = len(str(int (fib_n)))  # number of digits before the decimal

    return int(fib_n) / (10 ** max(0,fib_len - num_pandigital))

# Tests if number is pandigital to the number of digits requested
def check_pandigital (test_num, num_pandigital):

    test_num_str = str(test_num)
    if len(test_num_str) != num_pandigital:
        return 0

    test_digit_list = sorted(map(int, list(test_num_str)))
    if test_digit_list == range (1, num_pandigital+1):
        return 1
    return 0

def main():
    start_time = time.time()
    num_pandigital, buffer_len = 9, 9

    f_n_1, f_n_2 = 1,1
    first_n_1, first_n_2 = 1,1
    mod_val = 10 ** num_pandigital
    index = 3

    while 1:
        f_n_last = (f_n_1 + f_n_2) % mod_val  # checks last 9 digits

        f_n_first = first_n_1 + first_n_2
        
        if (check_pandigital(f_n_last, num_pandigital)):
            f_n_first_digits = int(str(f_n_first)[:num_pandigital])
            if check_pandigital (f_n_first_digits, num_pandigital):
               
                print index, " done"
                break
        
        f_n_2 = f_n_1
        f_n_1 = f_n_last

        if (len(str(f_n_first)) > (num_pandigital + buffer_len) and
            len(str(first_n_1)) > (num_pandigital + buffer_len)):

            last_dig_1 = int(str(f_n_first)[-1])
            last_dig_2 = int(str(first_n_1)[-1])
            
            first_n_2 = first_n_1 / 10 + (last_dig_1+last_dig_2>9)
            first_n_1 = f_n_first / 10
        else:
            first_n_2 = first_n_1 
            first_n_1 = f_n_first
                    
        index += 1

        print time.time() - start_time

main()
