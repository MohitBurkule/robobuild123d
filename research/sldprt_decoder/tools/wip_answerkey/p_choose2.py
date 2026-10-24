from choose2 import *
st=collections.Counter(); ex=[]
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        cs=contour_sets(d,s,e,f.id)
        if not cs: continue
        P,L,C,O=parse(d,s,e)
        a2seg={}
        for r in L: a2seg[r['a']]=(r['idx'],r['id'])
        for r in C: a2seg.setdefault(r['a'],(r['idx'],r['id']))
        dc=[set(c[1]) for c in f.contours]
        for q,edges in cs:
            ser=sorted(set(x for r in edges for x in r)-{0})
            segs=set(a2seg.get(a,('?',a)) for a in ser)
            sc=[len(segs&x)/max(len(segs|x),1) for x in dc]
            best=max(sc or [0])
            st['exact' if best==1 else ('partial' if best>=.5 else 'none')]+=1
            if best<1 and len(ex)<15: ex.append((n[:10],f.name,hex(q),len(edges),ser,sorted(segs,key=str),[sorted(x) for x in dc]))
print(st)
for x in ex: print(x)
