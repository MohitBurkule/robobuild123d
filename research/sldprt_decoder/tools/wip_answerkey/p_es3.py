from common import *
MK=re.compile(re.escape(b'\xff\xff\x00\x00\x03\xff\xff\xff\xff' + b'\x00' * 6 + b'\x80\xbf'))
CD=b'\xff\xff\x01\x00\x0b\x00moEndSpec_c'
def es_tag(d,R):
    c=collections.Counter()
    for f,s,e in R:
        if f.type not in ('Extrusion','ICE'): continue
        for m in MK.finditer(d,s,e):
            for k in (44,46):
                t=m.start()-k
                if u16(d,t)&0x8000 and d[t+2:t+4]==b'\x00\x00' and u16(d,t)!=0xffff: c[u16(d,t)]+=1
    return c.most_common(1)[0][0] if c else None
import collections
st=collections.Counter()
for n,D,d in parts():
    R=regions(D,d); tag=es_tag(d,R)
    cd=d.find(CD)
    for f,s,e in R:
        if not f.extrude: continue
        x=f.extrude
        anc=[]
        if s<=cd<e: anc.append(cd+len(CD)-2)
        if tag:
            tb=struct.pack('<H',tag)
            anc+=[m.start() for m in re.finditer(re.escape(tb+b'\x00\x00')+b'[\x00\x01]\x00',d[s:e])]
            anc=[a if a>=cd+len(CD)-2 and a<cd+len(CD) else (a+s if a<s else a) for a in anc]
        anc=sorted(set(a for a in anc))
        codes=[(d[a+4],d[a+18]) for a in anc]
        st['n_anchor',len(anc)]+=1
        ok= len(anc)>0 and codes[0][1]==x['end1']
        st['end1_first_ok',ok]+=1
        if not ok and st['shown']<10: st['shown']+=1; print(n[:10],f.name,x,hex(tag or 0),codes)
print(st)
