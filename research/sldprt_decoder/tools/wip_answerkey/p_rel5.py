from sk import *
from sldprt import item_relations as IR
HDR=re.compile(rb'([\x01-\x7f])\x00\x00\x00\x02\x00([\x00\x01])\x00([\x00-\x03])\x00(\xfe\xff\x00\x00|\x00\x00)', re.S)
def rels(d,s,e):
    out=[]
    for m in HDR.finditer(d,s,e):
        sl,_=IR.read_slots(d,m.end())
        if sl and ((len(m.group(4))==4 and m.group(2)==b'\x00') or (len(m.group(4))==2 and m.group(2)==b'\x01')): out.append((m.start(),m.group(1)[0],False,sl))
    return out
st=collections.Counter(); bytype=collections.Counter(); bad=[]
for n,D,d in parts():
    tm=tag_map(d)
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        P,L,C,O=parse(d,s,e)
        arr={'sgPointHandle':P,'sgLineHandle':L,'sgArcHandle':C}
        got=[];seen=set()
        for pos,t,geo,sl in rels(d,s,e):
            ents=[]
            for tg,i in sl:
                c=tg if isinstance(tg,str) else tm.get(tg)
                a=arr.get(c)
                ents.append((i,a[i]['id']) if a is not None and i<len(a) else (i,-1))
            k=(t,tuple(sorted(ents)))
            if not geo:
                if k in seen: continue
                seen.add(k)
            got.append(k)
        want=[(t,tuple(sorted(es))) for t,es in f.rels]
        G=collections.Counter(got); W=collections.Counter(want)
        for k,v in W.items():
            h=min(v,G.get(k,0)); st['hit']+=h; st['miss']+=v-h; bytype[k[0],'hit']+=h; bytype[k[0],'miss']+=v-h
        st['extra']+=sum((G-W).values())
        for k,v in (G-W).items(): bytype[k[0],'extra']+=v
        if sum((W-G).values()) and len(bad)<8: bad.append((n,f.name,list((W-G).items())[:4],list((G-W).items())[:4]))
print(st); print(sorted(bytype.items()))
for b in bad: print(b)
