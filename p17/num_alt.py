# num_alt.py
# Calculate the number of letters in all the numbers
# up to 1000 inclusive

# Create dictionary mapping numbers to their actual words
# When calculating two digit words, added them to dictionary and
# used this mapping to speed up three digit words

def one_digit_word (n, word_dict):
    if n > 9:
        print n, " has more than one digit"
        exit()
    if n==0:
        return ""
    return word_dict[n]

def two_digit_word (n, word_dict):
    if n > 99:
        print n, " has more than two digits"
        exit ()

    if n < 21 and n > 0:
        return word_dict[n]
    last_digit = n % 10
    tens_piece = n - last_digit

    final_str = word_dict[tens_piece] + one_digit_word (last_digit, word_dict)
    word_dict[n] = final_str
    return final_str

def three_digit_word (n, word_dict):
    if n > 999:
        print n, " has more than three digits"
        exit ()
    if n == 0:
        return ""
    
    two_digit_piece = n % 100
    hundreds_place = (n - two_digit_piece) / 100
    if hundreds_place > 0:
        first_part = one_digit_word (hundreds_place, word_dict) + "hundred"
    else:
        first_part = ""

    if two_digit_piece > 0:
        final_str =  first_part + "and" + word_dict[two_digit_piece]
    else:
        final_str = first_part

    return final_str

def four_digit_word (n, word_dict):
    if n > 9999:
        print n, " has more than four digits"
        exit ()
    three_digit_piece = n % 1000
    thousands_place = (n - three_digit_piece) / 1000
    if thousands_place > 0:
        first_part = one_digit_word (thousands_place, word_dict) + "thousand"
    else:
        first_part = ""
    
    return first_part + three_digit_word (three_digit_piece, word_dict)


def gen_dict_num_words (filename, word_dict):
    with open (filename, 'r') as f:
        for line in f:
            x1 = line.split()
            word_dict [int(x1[0])] = x1[1]

filename = "num_words.txt"
word_dict = {}

gen_dict_num_words (filename, word_dict)

sum_letters = 0
max_num = 1000
for i in range (1, max_num + 1):
    if i < 10:
        sum_letters += len(one_digit_word (i, word_dict))
    elif i < 100:
        sum_letters += len(two_digit_word (i, word_dict))
    elif i < 1000:
        sum_letters += len(three_digit_word (i, word_dict))
    else:
        sum_letters += len(four_digit_word (i, word_dict))
        
print sum_letters
