# name_product.py

def get_name_data (filename, name_list):
    with open (filename, 'r') as f:
        for line in f:
            x1 = line.split(',')
            for i in range(len(x1)):
                x1[i] = (x1[i])[1:-1]
            name_list += x1

def calc_sum_name (name):
    name_sum = 0
    for ch in name:
        name_sum += (ord(ch) - ord('A') + 1)
    return name_sum
            
filename = "names.txt"
name_list = []

get_name_data (filename, name_list)

name_list.sort()
power_sum = 0

for i in range (len(name_list)):
    power_sum += ((i+1)*calc_sum_name (name_list[i]))
print power_sum

gen = [(i+1)*calc_sum_name (name_list[i]) for i in range(len(name_list))]
print sum(gen)
