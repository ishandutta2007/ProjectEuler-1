# fibo_even.py
# Find the sum of all even Fib numbers less than 4 million

first_fib_no = 1
sec_fib_no = 2
max_num = 4000000

last_two_fib_no = []
last_two_fib_no.append (first_fib_no)
sum_even_fib_no = 0

while last_two_fib_no[-1] < max_num:
    curr_fib_no = last_two_fib_no[-1]
    
    sum_even_fib_no += (curr_fib_no % 2 == 0) * curr_fib_no # adds it if even

    if len (last_two_fib_no) == 2:    
        next_fib_no = sum (last_two_fib_no)
        last_two_fib_no.append (next_fib_no)
        last_two_fib_no.pop(0)
    else:
        last_two_fib_no.append (sec_fib_no)

print sum_even_fib_no
