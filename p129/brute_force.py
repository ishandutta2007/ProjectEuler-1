# brute_force.py

def repunit (n, mod_class):
    total = 0
    base = 10
    for i in range(n):
        total += (base**i % mod_class)
        total %= mod_class
    return total

def main():

    i = 3
    while i < 1050:
        j = 3
        while repunit(j, i)  != 0:
            j += 1
        print i, j
        i += 2
        if i % 5 == 0:
            i += 2
main()
