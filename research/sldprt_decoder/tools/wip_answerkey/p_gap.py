from common import *
from sldprt import fstream as FS, mfc
import collections
pn=sys.argv[1]
for n,D,d in parts():
    if n!=pn: continue
    ex={f.id for f in D.top() if f.extrude}
    dec=FS.decode(d,ex)
    sp=sorted((a,b) for a,b in dec.spans if b>a)
    gaps=[];last=0
    for a,b in sp:
        if a>last: gaps.append((last,a))
        last=max(last,b)
    gaps.append((last,len(d)))
    tot=sum(b-a for a,b in gaps)
    z=sum(d[a:b].count(0) for a,b in gaps)
    print('gap bytes',tot,'zeros',z, 'of',len(d))
    # owner class: last classdef name before gap start
    cds=[(r.offset,r.value['name']) for r in mfc.class_defs(d)]
    import bisect
    pos=[c[0] for c in cds]
    own=collections.Counter()
    for a,b in gaps:
        k=bisect.bisect(pos,a)-1
        own[cds[k][1] if k>=0 else '-']+=b-a
    for k,v in own.most_common(25): print(v,k)
