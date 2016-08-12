# distinct_powers.py

max_base = 100
max_exp = 100
num_list = []

for a in range(2, max_base+1):
    for b in range (2, max_exp + 1):
        num_list.append (a ** b)

num_set = set(num_list)
print len(num_set), len (num_list)
