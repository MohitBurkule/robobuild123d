import truth, collections
from common import *
def xf2(T,p):
    R=T[:9]; t=T[9:12]; x,y,z=p
    return (x*R[0]+y*R[1]+z*R[2]+t[0], x*R[3]+y*R[4]+z*R[5]+t[1], x*R[6]+y*R[7]+z*R[8]+t[2])
for name,fn in [('row',truth.xf),('col',xf2)]:
    truth.xf=fn; st=collections.Counter()
    for n,D,d in parts():
        for f in D.by_type('Extrusion','ICE'):
            r=truth.contour_truth(D,f)
            if not r: continue
            S,res=r; st['used']+=sum(res); st['none']+= (sum(res)==0)
    print(name,st)
