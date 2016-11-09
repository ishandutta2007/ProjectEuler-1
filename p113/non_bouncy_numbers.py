# non_bouncy_numbers.py
# Calculate the number of 100 digit numbers that are either increasing in
# digits or decreasing in digits

# Will do this recursively. A 100 digit increasing number's first n digits must
# also be increasing. Same for decreasing. Using that logic and the number of
# possibilities for the next digit is the basis of the recursion

# n is number of digits
import time

def calc_increasing_nums (n):
    num_available_digits = 9  # can't start with zero
    count = 1

    # This list tracks the count of increasing numbers ending in digit i
    end_digit_count = [1] * num_available_digits
    end_digit_count = [0] + end_digit_count
    
    count = 2
    total_sum = sum(end_digit_count)

    while count <= n:
        new_digit_count = [sum(end_digit_count[1:i]) for i in
                           range(2, num_available_digits+2)]
        new_digit_count = [0] + new_digit_count
        
        total_sum += sum(new_digit_count)
        
        end_digit_count = new_digit_count[:]
        count += 1
        
    return total_sum

def calc_decreasing_nums (n):

    num_available_digits = 10  
    count = 1

    # This list tracks the count of increasing numbers ending in digit i
    end_digit_count = [1] * (num_available_digits-1)
    end_digit_count = [0] + end_digit_count
    
    count = 2
    total_sum = sum(end_digit_count)
    while count <= n:
        new_digit_count = [sum(end_digit_count[i:num_available_digits]) for i in
                           range(0, num_available_digits)]

        total_sum += sum(new_digit_count)
        end_digit_count = new_digit_count[:]
        count += 1
        
    return total_sum

# These are the numbers that are both increasing and decreasing
# e.g. 111, 2222, .... which total 9 * n
def double_count(n):
    num_available_digits = 9
    return num_available_digits * n 

def main():
    start_time = time.time()
    n = 100
    print calc_increasing_nums (n) + calc_decreasing_nums (n) - double_count(n)
    print time.time() - start_time
main()
    
