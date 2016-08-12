
#p1_alt.py
max_num = 1000

gen3 = list (3*i for i in range(max_num/3 + 1))
gen5 = list (5*i for i in range(max_num/5))
gen15 = list (15*i for i in range(max_num/15 + 1))

print sum(gen3) + sum(gen5) - sum(gen15)
