# arranged_probability.py
# Find the first numbers > 10**12 such that m/n * (m-1)/(n-1) = 1/2
# Noticed a constant ratio between solutions, and used this to search
# for the next solution
# Turns out this was a Pell's equation variant, explaining the constant ratio
import time

def main():
    start_time = time.time()
    n = 8 * 10 ** 5
    k = 5.82840961829
    # k = 1
    max_num = 10**13
    target_num = 10 ** 12
    m_prev, n_prev = 1, 1
    while n < max_num:
        m = int(n / (2 ** 0.5)) + 1
        if n * (n - 1) == 2 * m * (m - 1):
            print m, n, (n+0.0) / n_prev
            if n > target_num:
                break
            if (n + 0.0) / n_prev < 6:
                k =  (n + 0.0) / n_prev
            m_prev, n_prev = m, n
            n = int(k * n) - 1

        n += 1
    print time.time() - start_time
main()
