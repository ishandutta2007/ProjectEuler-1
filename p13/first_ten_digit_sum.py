# first_ten_digit_sum.py

def get_and_input_data (filename, num_list, num_needed_digits):
    with open(filename, 'r') as f:
        for line in f:
            num_list.append (int(line[:num_needed_digits]))

filename = "hundred_fifty_digit_numbers.txt"
num_list = []
num_needed_digits = 13

get_and_input_data (filename, num_list, num_needed_digits)

print (str(sum(num_list)))[0:10]
