from choose2 import *
def segkey(P,r):
    def xy(i): 
        return tuple(round(v,9) for v in P[i]['xy']) if i<len(P) and 'xy' in P[i] else ('p',i)
    if 'start' not in r: return None
    a,b=xy(r['start']),xy(r['end'])
    return (r.get('type'),)+tuple(sorted([a,b],key=str))
st=collections.Counter(); ex=[]
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        cs=contour_sets(d,s,e,f.id)
        if not cs: continue
        P,L,C,O=parse(d,s,e)
        a2r={}
        for r in L: a2r[r['a']]=('L',r)
        for r in C: a2r.setdefault(r['a'],('C',r))
        # map dump seg id -> key ; key->dump seg
        idkey={}
        for r in L: idkey[(0,r['idx'],r['id'])]=segkey(P,r)
        for r in C: idkey[(1,r['idx'],r['id'])]=segkey(P,r)
        dsegs={sg['id']:sg['type'] for sg in f.segs}
        dc=[set((dsegs.get(x,-1),)+x for x in c[1]) for c in f.contours]
        key2d=collections.defaultdict(set)
        for c in dc:
            for x in c: key2d[idkey.get(x)].add(x)
        for q,edges in cs:
            ser=sorted(set(x for r in edges for x in r)-{0})
            got=set()
            for a in ser:
                if a not in a2r: got.add(('?',a)); continue
                t,r=a2r[a]; k=(0 if t=='L' else 1, r['idx'], r['id'])
                if not any(k in c for c in dc):
                    alt=key2d.get(idkey.get(k))
                    if alt: k=sorted(alt)[0]
                got.add(k)
            touched=[c for c in dc if c&got]
            U=set().union(*touched) if touched else set()
            ok = got==U and bool(U)
            st['exact' if ok else 'bad']+=1
            if not ok and len(ex)<12: ex.append((n[:10],f.name,hex(q),ser,sorted(got,key=str),[sorted(x) for x in dc]))
print(st)
for x in ex: print(x)
