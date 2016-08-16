# square_root_convergents.py
# Find continued fraction expansion convergents
# whose numerators have more digits than denominators
# for sqrt(2)'s first thousand convergents

home_path = "/home/osboxes/ProjEuler/"
import sys
sys.path.insert (0, home_path + "Utilities/")

from factors import gcd

def invert_fraction (numer, denom):
    return denom, numer

# Outputs fraction sum in reduced terms
def sum_fraction (n1, d1, n2, d2):
    numer1 = n1 * d2 + n2 * d1
    denom1 = d1 * d2

    com_factor = gcd ([numer1, denom1])
    return numer1 / com_factor, denom1/com_factor

max_num = 1000
frac_count = 0
for conv_index in xrange(1,max_num+1):
   calc_count = conv_index
   frac = [1,2]
   calc_count -= 1
   while calc_count > 0:
       num_inter, dem_inter = (sum_fraction (frac[0], frac[1], 2,1))
       frac = invert_fraction (num_inter, dem_inter)
       calc_count -= 1
   final_frac = sum_fraction (1,1, frac[0], frac[1])
   
   if len(str(final_frac[0])) > len(str(final_frac[1])):
       frac_count += 1

print frac_count
    
