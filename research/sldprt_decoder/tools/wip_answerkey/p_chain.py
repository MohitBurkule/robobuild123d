from sk import *
CH=b'\xff\xff\x01\x00\x0f\x00moSketchChain_c'
def chains_at(d,j,tch):
    """parse chain list starting at object j (after the 8-byte count header)."""
    pass
st=collections.Counter(); ex=[]
for n,D,d in parts():
    p=d.find(CH)
    if p<0: continue
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        P,L,C,O=parse(d,s,e)
        amap={}
        for r in L: amap[('L',r['a'])]=(0,r['idx'],r['id'])
        for r in C: amap[('C',r['a'])]=(1,r['idx'],r['id'])
        bya=collections.defaultdict(list)
        for r in L+C: bya[r['a']].append((r['idx'],r['id']))
        # find "N 00 00 00 N 00 00 00" followed by classdef or a 2-byte tag
        want=[frozenset(c[1]) for c in f.contours]
        found=[]
        for m in re.finditer(rb'([\x01-\x7f])\x00\x00\x00\1\x00\x00\x00',d[s:e]):
            j=s+m.end(); NN=m.group(1)[0]
            if d[j:j+len(CH)]==CH: k=j+len(CH)
            else: k=j+2
            nn=u16(d,k)
            if not 0<nn<400: continue
            ents=[u32(d,k+2+4*i) for i in range(nn)]
            found.append((hex(j),NN,ents))
        st['sk']+=1
        if found:
            ents=found[0][2]
            st['have']+=1
        if len(ex)<12 and len(f.contours)>0: ex.append((n[:10],f.name,[c[1] for c in f.contours],[(r['idx'],r['id'],r['a']) for r in L],[(r['idx'],r['id'],r['a']) for r in C],found[:2]))
print(st)
for x in ex: print(x)
