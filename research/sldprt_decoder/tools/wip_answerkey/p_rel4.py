exec(open('p_rel3.py').read().split('st=collections')[0])
fl=collections.Counter()
for n,D,d in parts():
    tm=tag_map(d)
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        P,L,C,O=parse(d,s,e)
        arr={'sgPointHandle':P,'sgLineHandle':L,'sgArcHandle':C}
        W=collections.Counter((t,tuple(sorted(es))) for t,es in f.rels)
        for m in HDR.finditer(d,s,e):
            sl,_=IR.read_slots(d,m.end())
            if not sl: continue
            ents=[]
            for tg,i in sl:
                c=tg if isinstance(tg,str) else tm.get(tg); a=arr.get(c)
                ents.append((i,a[i]['id']) if a is not None and i<len(a) else (i,-1))
            k=(m.group(1)[0],tuple(sorted(ents)))
            hit=W[k]>0
            if hit: W[k]-=1
            fl[len(m.group(4))==4, m.group(2)[0], m.group(3)[0], hit]+=1
for k,v in sorted(fl.items()): print(k,v)
