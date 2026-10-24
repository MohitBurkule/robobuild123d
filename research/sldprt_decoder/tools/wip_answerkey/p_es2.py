from common import *
MK=re.compile(re.escape(b'\xff\xff\x00\x00\x03\xff\xff\xff\xff' + b'\x00' * 6 + b'\x80\xbf'))
CD=b'\xff\xff\x01\x00\x0b\x00moEndSpec_c'
bodies=[]
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if not f.extrude: continue
        anc=[s+m.start()+len(CD)-2 for m in re.finditer(re.escape(CD),d[s:e])]
        for m in MK.finditer(d,s,e):
            for k in (44,46):
                t=m.start()-k
                if u16(d,t)&0x8000 and d[t+2:t+4]==b'\x00\x00': anc.append(t)
        for a in sorted(set(anc)): bodies.append(d[a+2:a+200])
import collections
L=200-2
const=[]
for i in range(L):
    c=collections.Counter(b[i] for b in bodies if len(b)>i)
    v,k=c.most_common(1)[0]
    const.append((i,v,k/len(bodies)))
print(len(bodies)); print(' '.join('%d:%02x'%(i,v) if r>0.97 else '.' for i,v,r in const))
