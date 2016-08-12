# coin_sums.py
# Calculate number of ways to generate 200 pence
# with all possible coin denominations

from fractions import gcd

# recursive algo
def partition_count (change_amount, coin_list):
    count = 0

    if len (coin_list) > 1:

        for num in range(0, (change_amount/coin_list[0])+1):
            count += partition_count (change_amount - num * coin_list[0], coin_list[1:])
        return count

    # default recursion case
    if len(coin_list) == 1:
        if change_amount % coin_list[0] == 0:
            return 1
        return 0

change_amount = 200
coin_list = [1,2,5,10,20,50,100,200]
# coin_list = [1,5]

print partition_count (change_amount, coin_list)
