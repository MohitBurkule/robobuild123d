from sk import *
st=collections.Counter(); bad=[]
def close(a,b): return a is not None and b is not None and abs(a[0]-b[0])<1e-8 and abs(a[1]-b[1])<1e-8
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        P,L,C,O=parse(d,s,e)
        pxy={}
        for (a,b),xyz in f.pts.items(): pxy[a]=xyz[:2]
        for sg in f.segs:
            a,b=sg['id']; arr={0:L,1:C}.get(sg['type'])
            if arr is None: st['type_other',sg['type']]+=1; continue
            if a>=len(arr) or arr[a]['id']!=b: st['id_bad']+=1; bad.append((n,f.name,sg['id'],sg['type'],[(r['id']) for r in arr]));continue
            r=arr[a]; st['id_ok']+=1
            if 'start' not in r: st['noflds']+=1; continue
            st['type_ok',r['type']==sg['type']]+=1
            sp=P[r['start']].get('xy') if r['start']<len(P) else None
            ep=P[r['end']].get('xy') if r['end']<len(P) else None
            ok=(close(sp,sg['p0']) and close(ep,sg['p1'])) or (close(sp,sg['p1']) and close(ep,sg['p0']))
            ok2= r['start'] in pxy and r['end'] in pxy and ((close(pxy[r['start']],sg['p0']) and close(pxy[r['end']],sg['p1'])) or (close(pxy[r['start']],sg['p1']) and close(pxy[r['end']],sg['p0'])))
            st['ends_ok',ok or ok2]+=1
            st['flag',r['flag'],sg['constr']]+=1
            if sg['type']==1:
                cp=P[r['centre']].get('xy') if r['centre']<len(P) else pxy.get(r['centre'])
                st['centre_ok', close(cp or pxy.get(r['centre']),sg['c'])]+=1
print(sorted(st.items(),key=str))
for b in bad[:8]: print(b)
