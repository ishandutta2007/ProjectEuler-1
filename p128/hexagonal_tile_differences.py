# hexagonal_tile_differences.py
# Tiles are numbered from 1 in the center around a counterclockwise
# hexagonal grid
# Find all tiles such that their differences from all adjacent tiles
# contain 3 primes

import sys, os, inspect, time

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import sieve_primes

# This will check for numbers with 3 adjacent tiles with prime differences
# for tiles at the "top" of each layer of the hexagon
# E.g. layer 1 starts with 2, l-2 with 8, l-3 with 20, ...
def top_layer_calc (mod_prime_list, prime_set):
    criteria_list = [x for x in mod_prime_list if (x+2) in prime_set and
                     (2*x + 7) in prime_set]
    index_list = [(x+1)/6 for x in criteria_list]

    top_layer_list = [6*(n*(n-1))/2 + 2 for n in index_list]

    return top_layer_list

# This will check for the target tiles among the tiles that are directly
# to the right of the top tile in each layer (or the final tile in each layer)
def final_tile_calc (mod_prime_list, prime_set):

    criteria_list = [x for x in mod_prime_list if (x+6) in prime_set and
                     (2*x - 5) in prime_set]
    
    index_list = [(x+1)/6 for x in criteria_list]

    final_tile_list = [6*(n*(n+1))/2 + 1 for n in index_list]

    return final_tile_list

def main():
    start_time = time.time()
    max_num = 1000000
    target_index = 2000
    
    prime_list = sieve_primes (max_num)
    print time.time() - start_time
    prime_set = set(prime_list)
    
    mod_prime_list = [x for x in prime_list if x % 6 == 5]
    
    top_layer_list = top_layer_calc (mod_prime_list, prime_set)

    final_tile_list = final_tile_calc (mod_prime_list, prime_set)

    complete_tile_list = sorted(top_layer_list + final_tile_list)

    print complete_tile_list[target_index-1]
    print time.time() - start_time
    
main()
