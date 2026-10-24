from common import *
from sldprt import fstream as FS
import collections
st=collections.Counter(); ex=[]
for n,D,d in parts():
    hidx=FS.header_index(d)
    for f in D.top():
        h=hidx.get(f.id)
        if not h: continue
        dims=FS.feature_dims(d,h.offset,h.region_end)
        mine={a:b for a,b,_,_ in dims}
        allv=collections.defaultdict(list)
        for m in FS.DIMV.finditer(d,h.offset,h.region_end): allv[m.group(2).decode('utf-16-le')].append(struct.unpack('<d',m.group(3))[0])
        for full,v in f.dims:
            p=full.split('@')
            if p[1]!=f.name: continue
            g=mine.get(p[0])
            ok=g is not None and abs(g-v)<1e-9*max(1,abs(v))+1e-12
            st[f.type,ok]+=1
            if not ok and len(ex)<15: ex.append((n[:10],f.name,p[0],v,g,allv.get(p[0],[])[:5]))
print(st); [print(x) for x in ex]
