# square_alt.py
# Find continued fraction expansion convergents
# whose numerators have more digits than denominators
# for sqrt(2)'s first thousand convergents

max_num = 1000
frac_count = 0
frac = [3,2]
for conv_index in xrange(2,max_num+1):

    frac = 2 * frac[1] + frac[0], frac[1]+frac[0]
    
    if len(str(frac[0])) > len(str(frac[1])):
       frac_count += 1

print frac_count
    
