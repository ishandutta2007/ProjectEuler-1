# counting_fractions.py
# for n <= 10 ** 6, how many proper reduced fractions are there
# This boils down to summing Euler's totient function from 1 to n

import sys, os, inspect, time
from math import factorial

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
a = cmd_folder.split(os.path.sep)
a = a[:-1]                         
a.append ("Utilities")
sys.path.insert (0, (os.path.sep).join(a))

from factors import gen_totient_list

max_num = 10 ** 6
print sum(gen_totient_list(max_num))



