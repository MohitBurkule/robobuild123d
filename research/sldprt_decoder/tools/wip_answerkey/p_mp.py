from common import *
import collections
REF=re.compile(rb'[\x00-\xff][\x80-\xff]\x00\x00[\x00-\xff][\x80-\xff][\x00-\xff]{2}(.{4})(.{4})(.{4})',re.S)
st=collections.Counter()
for n,D,d in parts():
    R=regions(D,d); ids={f.name:f.id for f in D.top()}
    for f,s,e in R:
        if f.type not in ('MirrorPattern','CirPattern','LPattern','MirrorStock'): continue
        refs=collections.Counter(u32(d,m.start(1)) for m in REF.finditer(d,s,e))
        par=[(p,t,ids.get(p)) for p,t in f.parents]
        hit=[(p,t,i in refs) for p,t,i in par]
        allids=set(ids.values())
        extra=[i for i in refs if i in allids and i not in [x[2] for x in par] and i!=f.id]
        print(n[:10],f.name,f.type,hit,'extra',extra[:5])
