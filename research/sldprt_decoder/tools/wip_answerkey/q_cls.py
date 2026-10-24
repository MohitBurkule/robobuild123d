import sys,os,bisect,collections;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS, mfc
tot=collections.Counter(); allb=0; unexp=0; nparts=collections.Counter()
for n,D,d in parts():
    dec=FS.decode(d,{f.id for f in D.top() if f.extrude})
    cov=bytearray(len(d))
    for a,b in dec.spans:
        a=max(0,a); b=min(len(d),b)
        if b>a: cov[a:b]=b'\x01'*(b-a)
    cds=mfc.class_defs(d); pos=[c.offset for c in cds]; names=[c.value['name'] for c in cds]
    seen=set()
    # run-length over uncovered
    i=0; L=len(d)
    while i<L:
        if cov[i]: i+=1; continue
        j=i
        while j<L and not cov[j]: j+=1
        # split run at classdef boundaries
        k=bisect.bisect_right(pos,i)-1
        a=i
        while a<j:
            nxt=pos[k+1] if k+1<len(pos) else L
            b=min(j,nxt)
            nm=names[k] if k>=0 else '(before first ClassDef)'
            tot[nm]+=b-a; seen.add(nm); a=b; k+=1
        unexp+=j-i; i=j
    allb+=L
    for s in seen: nparts[s]+=1
print('total',allb,'unexplained',unexp,round(100*unexp/allb,1))
for nm,b in tot.most_common(40): print(f'{nm:34s} {b:9d} {100*b/unexp:5.1f} {nparts[nm]}')
