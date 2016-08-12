# collatz.py

def calc_chain_len (n, collatz_list):

    no_of_terms = 1
    curr_term = n

    while curr_term != 1:
        if curr_term % 2 == 0:
            curr_term = curr_term/2
        else:
            curr_term = 3 * curr_term + 1

        if curr_term < n:
            return collatz_list[curr_term] + no_of_terms
        
        no_of_terms += 1
        
    return no_of_terms

max_num = 1000000
max_chain_len = 0
curr_leader = 0
collatz_list = [0]
for i in range (1, max_num):
    curr_chain = calc_chain_len(i, collatz_list)
    collatz_list.append (curr_chain)
    if curr_chain > max_chain_len:
        curr_leader = i
        max_chain_len = curr_chain

print curr_leader, max_chain_len
