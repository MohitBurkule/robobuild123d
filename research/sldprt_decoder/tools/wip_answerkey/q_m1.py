import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
for n,D,d in parts():
    top=D.top(); ids={x.name:x.id for x in top}; hidx=FS.header_index(d)
    for f in top:
        if f.type!='MirrorPattern': continue
        h=hidx[f.id]
        pl=[(p,ids.get(p)) for p,t in f.parents if t=='RefPlane']
        for p,pid in pl:
            hits=[j-h.offset for j in range(h.offset,h.region_end-4) if u32(d,j)==pid and d[j-2:j]==b'\x00\x00' and u32(d,j+4)>0x1000000]
            print(n[:10],f.name,p,pid,h.region_end-h.offset,hits[:6],[d[h.offset+x-8:h.offset+x+12].hex(' ') for x in hits[:2]])
