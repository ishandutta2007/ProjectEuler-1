import math
from timeit import default_timer as timer
start = timer()

b=[[1,2,2],[2,1,2],[2,2,3]]
c=[[-1,2,2],[-2,1,2],[-2,2,3]]


def find_pythogorean_triplets(m,f):
    tr=[]
    if f==1:
        for i in range(0,3):
            t=m[0]*b[i][0]+m[1]*b[i][1]+m[2]*b[i][2]
            tr.append(t)
        return tr
    else:
        for i in range(0,3):
            t=m[0]*c[i][0]+m[1]*c[i][1]+m[2]*c[i][2]
            tr.append(t)
    return tr


def solve138(p1,f):
    global c1,tot_sum
    if c1<=11:
        if f==0:
            item = find_pythogorean_triplets(p1,f)
            h=item[0]
            b=item[1]*2
            l=item[2]
            if abs(h-b)==1:
                f=1
                tot_sum+=l
                print item
                c1+=1
                solve138(item,f)
        else:
            item = find_pythogorean_triplets(p1,f)
            print item, "not solution"
            f=0
            solve138(item,f)
p=[3,4,5]
c1=0
tot_sum=0
solve138(p,0)
print tot_sum


end =timer()
print "Elapsed time:", end - start
