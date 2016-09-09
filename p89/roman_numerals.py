# roman_numerals.py
# Take Roman numerals from input file, calculate their minimal Roman numeral
# representation and determine how many characters are saved
# Sum up the character savings


import time

# opens inputted file, puts the roman numerals into an outputted list
def get_roman_list (filename):
    roman_list = []
    
    with open (filename, 'r') as f:
        for line in f:
            roman_list.append(line.rstrip())
    return roman_list

def roman_english_dict (map_file_name):
    roman_dict = {}
    with open (map_file_name, 'r') as f:
        for line in f:
            x1 = (line.rstrip()).split('\t')
            if len(x1) > 1:
                roman_num, english_num = x1[0], int(x1[1])
                roman_dict[roman_num] = english_num
    
    return roman_dict

def convert_roman_english (roman_list, roman_dict):
    num_list = []
    for roman_nums in roman_list:
        index = 0
        num_total = 0
        while index < len (roman_nums):
            if index == len (roman_nums) - 1:
                num_total += roman_dict[roman_nums[index]]
                index += 1
            else:
                test_str = roman_nums[index:index+2]
                if test_str in roman_dict:
                    num_total += roman_dict[test_str]
                    index += 2
                else:
                    test_str = roman_nums[index]
                    num_total += roman_dict[test_str]
                    index += 1
        num_list.append ((num_total, len (roman_nums)))
                         
    return num_list

# Converts numbers into most efficient Roman form
# Takes the difference in string length between this and
# original Roman form (which is in the inputted list)

def convert_english_roman (num_list, inv_dict):
    final_list = []
    for nums in num_list:
        roman_str = []
        num_str = str(nums[0])
        num_len = len (num_str)
        index = 0
        for dig in reversed (num_str):
            val = int(dig) * (10 ** index)
            if val == 0:
                index += 1
                continue
            if val in inv_dict:
                roman_str = list(inv_dict[val]) + roman_str
            else:
                if index == 3:  # thousands digit
                    roman_str = (['M'] * int(dig)) + roman_str
                else:
                    if int(dig) > 5:
                        rem_digits = int(dig) - 5
                        roman_str = ([inv_dict[1 * (10 ** index)]] * rem_digits) + roman_str
                        roman_str = list(inv_dict[5 * (10 ** index)]) + roman_str
                    else:
                        rem_digits = int(dig)
                        roman_str = ([inv_dict[1 * (10 ** index)]] * rem_digits) + roman_str
                        
            index += 1
        final_list.append (nums[1] - len(roman_str))

    return final_list
        
start_time = time.time()                       
filename = "roman.txt"
roman_list = get_roman_list (filename)

map_file_name = "roman_mapping.txt"
roman_dict = roman_english_dict (map_file_name)
inv_dict = {v:k for k,v in roman_dict.iteritems()}

num_list = convert_roman_english (roman_list, roman_dict)

print sum(convert_english_roman (num_list, inv_dict))
print time.time() - start_time
