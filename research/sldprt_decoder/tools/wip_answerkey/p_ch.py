from common import *
from sldprt import fstream as FS, answer_key as AK
import collections
st=collections.Counter(); ex=[]
for n,D,d in parts():
    hidx=FS.header_index(d); ct=FS.chain_tag_of(d)
    for f in D.sketches():
        h=hidx[f.id]; s,e=h.offset,h.region_end
        sk=FS.parse_sketch(d,s,e); chs=FS.chains(d,s,e,ct)
        ser={}
        for x in sk.lines: ser[(0,)+x.api_id]=x.serial
        for x in sk.arcs: ser[(1,)+x.api_id]=x.serial
        cs=[sorted(c.serials) for c in chs]
        for closed,ids in f.contours:
            w=sorted(ser.get((q['type'],)+q['id'],-1) for q in AK.resolve_contour(f,ids) if q)
            ok=w in cs; st[ok]+=1
            if not ok and len(ex)<10: ex.append((n[:10],f.name,hex(ct or 0),w,cs[:6]))
print(st); [print(x) for x in ex]
st2=collections.Counter()
for n,D,d in parts():
    hidx=FS.header_index(d); ct=FS.chain_tag_of(d)
    for f in D.sketches():
        h=hidx[f.id]; chs=FS.chains(d,h.offset,h.region_end,ct)
        st2['sk_has_chains',bool(chs)]+=1
        if not chs: st2['contours_in_chainless']+=len(f.contours)
        else: st2['contours_in_chained']+=len(f.contours); st2['chains']+=len(chs)
print(st2)
st3=collections.Counter()
for n,D,d in parts():
    hidx=FS.header_index(d); ct=FS.chain_tag_of(d)
    for f in D.sketches():
        h=hidx[f.id]; s,e=h.offset,h.region_end
        chs=FS.chains(d,s,e,ct)
        if chs: continue
        sk=FS.parse_sketch(d,s,e); cc=[sorted(c.serials) for c in FS.computed_contours(sk)]
        ser={}
        for x in sk.lines: ser[(0,)+x.api_id]=x.serial
        for x in sk.arcs: ser[(1,)+x.api_id]=x.serial
        for closed,ids in f.contours:
            w=sorted(ser.get((q['type'],)+q['id'],-1) for q in AK.resolve_contour(f,ids) if q)
            st3[w in cc]+=1
print('computed',st3)
