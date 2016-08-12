# 7/21/16
# lg_pal_prod.py
# largest palindrome product of two 3 digit numbers

def gen_digit_list (num, digit_list = []):
    
    if num < 0:
        print "Negative number cannot be palindromes"
        return 0
    
    num_digits = len (str(num))

    # create list of digits
    for exp in range (num_digits - 1, -1, -1):
        digit_list.append ((num / (10 ** exp)) % 10)


def check_palindrome (digit_list):

    for i in range (len (digit_list)/2):
        if (digit_list[i] != digit_list[-1-i]):
            return 0
    return 1
        
def gen_height_pairs (height, height_pairs, min_num, max_num):

    start_pair = [height/2, height- (height/2)]
    while (start_pair[0] >= min_num and start_pair[1] <= max_num):
        height_pairs.append (list(start_pair))
        start_pair[0], start_pair[1] = start_pair[0]-1, start_pair[1] + 1



digit_list = []
min_num = 100
max_num = 999

height = 2 * max_num
min_height = 2 * min_num
max_product = 0
curr_largest_pair = []

while height >= min_height:
    height_pairs = []    
    gen_height_pairs (height, height_pairs, min_num, max_num)
    for h_pair in height_pairs:
        if h_pair[0]*h_pair[1] > max_product: # this could be new highest pair
#             digit_list = []
#             gen_digit_list (h_pair[0] * h_pair[1], digit_list)

#            if check_palindrome (digit_list) == 1:
             if str(h_pair[0] * h_pair[1]) == ''.join(reversed(str(h_pair[0]*h_pair[1]))):
                curr_largest_pair = list (h_pair)
                max_product = h_pair[0] * h_pair[1]
                min_height = (max_product ** 0.5) * 2
                
    height = height - 1

print curr_largest_pair, max_product
