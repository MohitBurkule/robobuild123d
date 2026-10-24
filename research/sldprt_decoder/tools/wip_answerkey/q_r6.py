import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
n="RV26 Base Panel"; d=open('fs/'+n+'.bin','rb').read()
D=[x for nn,x,_ in parts() if nn==n][0]
dec=FS.decode(d,set()); S=[f for f in D.top() if f.name=='Sketch1'][0]
sk=dec.sketches[S.id]['sketch']
cc=FS.computed_contours(sk)
for c in cc: print(c.serials,c.closed)
bs=sk.by_serial()
for x in (14,36,15,16,18,20,44): g=bs[x]; print(x,g.kind,g.real,FS._seg_polyline(sk,g)[::12])
