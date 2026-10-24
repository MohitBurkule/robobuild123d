from common import *
from sldprt import mfc
st=collections.Counter() if False else None
import collections
st=collections.Counter()
for n,D,d in parts():
    cs=mfc.cstrings(d)
    got={}
    for r in cs:
        e=r.end
        if r.value and d[e+16:e+19]==b'\xff\xfe\xff' and u32(d,e+8)<100000 and u32(d,e)==0:
            got.setdefault((r.value,u32(d,e+8)),r.offset)
    want={(f.name,f.id) for f in D.features+[c for f in D.features for c in f.children] if f.type not in ('AmbientLight','DirectionLight','EnvFolder')}
    st['want']+=len(want); st['hit']+=len(want&set(got)); st['extra']+=len(set(got)-want)
    if set(got)-want and st['show']<5: st['show']+=1; print(n,list(set(got)-want)[:5])
print(st)
