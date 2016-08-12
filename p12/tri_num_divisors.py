# tri_num_divisors.py
# Find first triangle number with more than 500 divisors

def calc_num_divisors (n, prime_list):
    count = 0

    for i in range(1, n/3):
        if n % i == 0:
            count += 1
    if n % 2 == 0:
        return (count + 2) # adds back n/2 and n
    
    return (count + 1) # adds back n

# This will actually return the (n-1)th triangle number
def num_divisors_nminus1th_triangle_num (n, num_divisors):
    if n % 2 == 0:
        return num_divisors[n/2]*num_divisors[n-1]
    else:
        return num_divisors[n]*num_divisors[(n-1)/2]

num_divisors = [1, 1, 2] # corresponds to 0, 1, and 2
total_tri_num_divisors = 1
n = 3
while True:
    num_divisors.append(calc_num_divisors(n))
    total_tri_num_divisors = num_divisors_nminus1th_triangle_num (n, num_divisors)
    if total_tri_num_divisors > 500:
        break
    n += 1
    
print n-1, ((n-1)*(n))/2

