import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
import collections
st=collections.Counter()
for k,(n,D,d) in enumerate(parts()):
    ids={x.name:x.id for x in D.top()}
    ex={f.id:f for f in D.top() if f.extrude}
    dec=FS.decode(d,set(ex)); hidx=FS.header_index(d)
    for fid,f in ex.items():
        x=f.extrude; es=dec.endspecs.get(fid)
        if not es: continue
        upto=int(x['end1']) in (3,4,5,7)
        h=hidx[fid]
        par={ids.get(p) for p,t in f.parents if t not in ('ProfileFeature','OriginProfileFeature')}
        rs=[m for m in FS.FREF.finditer(d,es.offset,h.region_end) if u32(d,m.start(1)) in set(ids.values())]
        first=rs[0] if rs else None
        fo=u32(d,first.start(1)) if first else None
        dist=first.start()-es.offset if first else None
        st[('upto' if upto else 'other', fo in par, )]+=1
        if upto and len(sys.argv)>1: print(n[:10],f.name,int(x['end1']),'first',fo,dist,d[first.start():first.start()+8].hex(' ') if first else '', fo in par)
print(st)
