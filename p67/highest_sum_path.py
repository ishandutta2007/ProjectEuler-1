# highest_sum_path.py

# get the list data from file
def get_triangle_data_list (filename, data_list):
    with open (filename, 'r') as f:
        for line in f:
            x1 = line.split()
            line_list = []
            for str_num in x1:
                line_list.append (int(str_num))
            data_list.append (line_list)

filename = "triangle.txt"
data_list = []
get_triangle_data_list (filename, data_list)

 # Working from bottom of triangle up, flipping the data makes this easier
rev_data_list = list(reversed (data_list))

for i in range(1, len (rev_data_list)):
    for j in range(len(rev_data_list[i])):
        rev_data_list[i][j] += max (rev_data_list[i-1][j], rev_data_list[i-1][j+1])

print rev_data_list[-1]
