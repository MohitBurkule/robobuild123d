from sk import *
from sldprt import item_relations as IR
st=collections.Counter(); bytype=collections.Counter(); bad=[]
for n,D,d in parts():
    tm=tag_map(d)
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        P,L,C,O=parse(d,s,e)
        arr={'sgPointHandle':P,'sgLineHandle':L,'sgArcHandle':C}
        got=[]
        for r in IR.relation_records(d,s,e):
            ents=[]
            for t,i in r['slots']:
                c=t if isinstance(t,str) else tm.get(t)
                a=arr.get(c)
                ents.append((i,a[i]['id']) if a is not None and i<len(a) else (i,-1))
            got.append((r['type_code'],tuple(sorted(ents))))
        want=[(t,tuple(sorted(es))) for t,es in f.rels]
        G=collections.Counter(got); W=collections.Counter(want)
        for k,v in W.items():
            h=min(v,G.get(k,0)); st['hit']+=h; st['miss']+=v-h; bytype[k[0],'hit']+=h; bytype[k[0],'miss']+=v-h
        st['extra']+=sum((G-W).values())
        if sum((W-G).values()) and len(bad)<6: bad.append((n,f.name,list((W-G).items())[:4],list((G-W).items())[:4]))
print(st); print(sorted(bytype.items()))
for b in bad: print(b)
