import itertools, time
start_time = time.time()
n = 12

subset_list = []
for i in range(1, n+1):
    subset_list += itertools.combinations(range(1,n+1), i)

comp_list = []
for x in subset_list:
    for y in subset_list:
        if len(set(x).intersection(set(y))) > 0:
            continue
        else:
            comp_list.append([x, y])


for i in range(len(comp_list)):
    comp = comp_list[i]
    x0, x1 = min(comp[0]), min(comp[1])
    if x1 < x0:
        comp_list[i] = [comp[1], comp[0]]

comp_set= set(map(tuple, comp_list))
new_comp_list = list(comp_set)
trimmed_comp_list = [comp for comp in new_comp_list if len(comp[0])==
                     len(comp[1]) and len(comp[0]) > 1]
total = 0
for comp in trimmed_comp_list:
    x1, x2 = (comp[0]), (comp[1])
    x_sum = sum(map(lambda x: x[0]<x[1], zip(x1, x2)))
    if x_sum == len(comp[0]) or x_sum == 0:
        continue
    else:
        total += 1
print total
print time.time() - start_time


