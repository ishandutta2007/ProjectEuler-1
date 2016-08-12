# coded_triangle_numbers.py
# Count all words in inputted file whose value
# corresponds to a triangle number

input_file = "words.txt"

# Triangle numbers can be shown to be equivalent to
# 8n + 1 being a perfect square, so that is what we test
def test_if_triangle (num):
    square_test = 8 * num + 1
    sq_root = square_test ** 0.5
    if int(sq_root) == sq_root:
        return 1
    return 0

# calculates value of word, assuming 1 for 'a', 2 for 'b', ... and summing
def calc_word_value (word):
    border_cap_value = ord('Z')
    capital_base = ord('A')
    lowercase_base = ord('a')
    
    word_sum = 0
    for ch in word:
        if ord(ch) <= border_cap_value: # uppercase
            base_val = capital_base
        else:
            base_val = lowercase_base
        word_sum += (ord(ch) - base_val + 1)
    return word_sum

triangle_count = 0

with open (input_file, 'r') as f:
    for line in f:
        x1 = line.split(',')
        for word in x1:
            if test_if_triangle (calc_word_value (word[1:-1])) == 1:
                triangle_count += 1

print triangle_count

