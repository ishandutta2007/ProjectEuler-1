# permuted_multiples.py
# Find smallest number such that x, 2x, ... , 6x all have same digits



def multiples_same_digits (num):
    num_str = str(num)
    num_list = list(num_str)

    max_multiple = 6
    if len(set(list(num_str))) < max_multiple:
        return 0
    
    num_list.sort()

    for i in range(2, max_multiple + 1):
        check_list = list (str (i * num))
        check_list.sort()
        if check_list == num_list:
            continue
        else:
            return 0
    return 1

i = 100001
test = 0
max_multiple = 6

while test == 0:

    if multiples_same_digits (i) == 1:
        print i
        break

    if len(str(i)) != len(str(max_multiple * i)):
        new_len =  (len(str(i)) + 1) + 1
        i = 10 ** new_len
    else:
        i += 1
