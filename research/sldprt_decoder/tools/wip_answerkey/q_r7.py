import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
import collections
st=collections.Counter()
for n,D,d in parts():
    dec=FS.decode(d,set())
    for fid,X in dec.sketches.items():
        regs=X['regions']
        for c in X['choosers']:
            for ct in c.contours:
                if ct.rid is not None: st['ok']+=1; continue
                if not regs: st['no region list']+=1; continue
                sub=[r for r in regs if set(ct.serials)<=set(r.serials)]
                sup=[r for r in regs if set(ct.serials)>=set(r.serials)]
                k='subset' if sub else 'superset' if sup else 'none'
                st[k]+=1
                if k=='none' and st[k]<6: print(n[:12],fid,ct.serials,[(r.rid,r.serials) for r in regs])
print(st)
