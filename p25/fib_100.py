# fib_100.py

f1 = 1
f2 = 1
index = 2
target_num = 10**999
while (f2 < target_num):
    f1, f2 = f2, f1+f2
    index += 1
print index
