# twenty_alt.py

def nCr (n, r):
    if r == 1 or r == (n-1):
        return n
    if r == 0:
        return 1
    if n == r:
        return 1
    return nCr (n-1,r-1) + nCr (n-1,r)

print nCr (40,20)
