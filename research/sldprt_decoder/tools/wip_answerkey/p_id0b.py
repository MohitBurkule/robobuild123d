from common import *
import collections
st=collections.Counter(); bad=[]
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        P=[];S=[]
        for m in MARK.finditer(d,s,e):
            o=m.start()-8; R=m.end()+47
            (S if d[R+8:R+16]==struct.pack("<d",-1.0) else P).append(i32(d,o+4))
        for (a,b) in f.pts:
            ok = a<len(P) and P[a]==b; st['p',ok]+=1
        for sg in f.segs:
            a,b=sg['id']; ok= a<len(S) and S[a]==b; st['s',ok]+=1
            if not ok and len(bad)<10: bad.append((n,f.name,a,b,S[:12]))
print(st); [print(b) for b in bad]
