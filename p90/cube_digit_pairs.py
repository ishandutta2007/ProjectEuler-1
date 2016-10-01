# cube_digit_pairs.py
# Find all ways to put digits 0-9 on 2 dice such that
# all square numbers can be displayed

import time
# if either die has a 6 or 9, but not both, the other number is added to the list
def list_adjust (die_list):
    if 6 in die_list and 9 not in die_list:
        die_list.append(9)
    if 6 not in die_list and 9 in die_list:
        die_list.append(6)
    die_list.sort()
    return die_list

# Makes a list of square numbers up to 81 in string form, with zeroes before
# the single digit squares
def make_square_list ():
    num_sq_list = ['0'+str(x*x) for x in xrange(1, 4)]
    num_sq_list += [str(x*x) for x in xrange(4,10)]
    return num_sq_list

def make_all_squares (die1, die2, num_sq_list):
    for sq in num_sq_list:
        if sq[0] in set(die1) and sq[1] in set(die2):
            continue
        if sq[0] in set(die2) and sq[1] in set(die1):
            continue
        return 0
    return 1

def main():
    start_time = time.time()
    choice_range = range(10)
    num_sq_list = make_square_list()
    count = 0
    same = 0
    for a1 in xrange(7):
        for a2 in xrange(a1+1, 8):
            for a3 in xrange (a2+1, 9):
                for a4 in xrange (a3+1, 10):
                    x_die1 = [a1, a2, a3, a4]
                    for b1 in xrange (a1, 7):
                        if b1 == a1:
                            init2 = a2
                        else:
                            init2 = b1 + 1
                        for b2 in xrange (init2, 8):
                            if (a1,a2) == (b1,b2):
                                init3 = a3
                            else:
                                init3 = b2+1
                            for b3 in xrange (init3, 9):
                                if (a1,a2,a3) == (b1,b2,b3):
                                    init4 = a4
                                else:
                                    init4 = b3+1
                                    for b4 in xrange(init4, 10):
                                        x_die2 = [b1, b2, b3, b4]
                                        die1 = [x for x in choice_range if x not in set(x_die1)]
                                        die2 = [x for x in choice_range if x not in set(x_die2)]
                                        die1.sort()
                                        die2.sort()
                                        die1 = list_adjust (die1)
                                        die2 = list_adjust (die2)
                                        die1 = map (str, die1)
                                        die2 = map (str, die2)
                                        count += make_all_squares (die1, die2, num_sq_list)
    print count, time.time() - start_time

main()

