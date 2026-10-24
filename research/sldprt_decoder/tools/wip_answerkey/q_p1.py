import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS, validate as V
for n,D,d in parts():
    top=D.top(); ids={x.name:x.id for x in top}; hidx=FS.header_index(d)
    for f in top:
        if f.type not in V.PATTERN_TYPES: continue
        h=hidx.get(f.id)
        if not h: print(n[:12],f.name,'NOHDR'); continue
        refs=FS.referenced_feature_ids(d,h.offset,h.region_end,set(ids.values()))
        par=[(p,t,ids.get(p)) for p,t in f.parents]
        bad=[p for p in par if p[1]!='RefPlane' and p[2] not in refs]
        print(n[:12],f.type,f.name,f.id,h.offset,h.region_end-h.offset,'par',par,'refs',sorted(refs),'BAD' if bad else '')
