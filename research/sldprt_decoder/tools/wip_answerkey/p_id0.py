from common import *
import collections
hitp=collections.Counter(); hits=collections.Counter(); NP=NS=0
dist=collections.Counter()
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        recs={}
        for m in MARK.finditer(d,s,e):
            o=m.start()-8; R=m.end()+47
            recs.setdefault((u16(d,R)==0x1e, i32(d,o+4)),o)
        for (a,b) in f.pts:
            o=recs.get((True,b))
            if o is None: continue
            NP+=1; dist['p',a-b]+=1
            for k in range(-16,200,2):
                if u16(d,o+k)==a: hitp[k]+=1
        for sg in f.segs:
            a,b=sg['id']; o=recs.get((False,b))
            if o is None: continue
            NS+=1; dist['s',a-b]+=1
            for k in range(-16,200,2):
                if u16(d,o+k)==a: hits[k]+=1
print(NP,hitp.most_common(6)); print(NS,hits.most_common(6)); print(dist.most_common(12))
