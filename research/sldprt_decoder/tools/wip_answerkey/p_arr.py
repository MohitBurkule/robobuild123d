from common import *
import collections
NEG=struct.pack('<d',-1.0)
def arrays(d,s,e):
    ms=[m for m in MARK.finditer(d,s,e)]
    offs=[m.start()-8 for m in ms]
    out=[];k=0
    while k<len(offs):
        o=offs[k]; N=u32(d,o-6)
        if 0<N<=len(offs)-k and N<5000:
            out.append((o,N,u16(d,o-2),offs[k:k+N])); k+=N
        else:
            out.append((o,0,None,[o])); k+=1
    return out
st=collections.Counter(); bad=[]
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        A_=arrays(d,s,e)
        sig=[]
        for (o,N,tag,recs) in A_:
            R=[x+8+17+47 for x in recs]
            kinds=collections.Counter('P' if d[r+8:r+16]!=NEG else 'S%d'%u16(d,r+16) for r in R)
            sig.append((N,tag,dict(kinds)))
        st[str([ (x[0]>0) for x in sig])]+=1
        if len(bad)<15: bad.append((n[:10],f.name,len(f.pts),collections.Counter(sg['type'] for sg in f.segs),sig))
for b in bad: print(b)
print(st.most_common(10))
