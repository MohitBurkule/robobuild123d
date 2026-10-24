from common import *
import collections
NEG=struct.pack('<d',-1.0)
def arrays(d,s,e):
    offs=[m.start()-8 for m in MARK.finditer(d,s,e)]
    out=[];k=0
    while k<len(offs):
        o=offs[k]; N=u32(d,o-6)
        if 0<N<=len(offs)-k and N<5000:
            out.append(offs[k:k+N]); k+=N
        else:
            out.append(None); k+=1
    return out
def parse(d,s,e):
    P=[];L=[];C=[];other=[]
    arrs=[a for a in arrays(d,s,e) if a]
    for ai,a in enumerate(arrs):
        R=[o+72 for o in a]
        ks=collections.Counter(u16(d,r+16) for r in R if d[r+8:r+16]==NEG)
        if ai==0: kind='P'
        elif not ks: kind='X'
        else:
            mk=ks.most_common(1)[0][0]
            kind={0:'L',1:'C',0xffff:'C'}.get(mk,'K%d'%mk)
            if kind=='L' and (ks.get(1) or ks.get(0xffff)) and not L: kind='L'
        recs=[]
        for idx,o in enumerate(a):
            r=o+72; rec={'idx':idx,'id':i32(d,o+4),'a':u32(d,o),'off':o}
            if kind=='P':
                if u16(d,r)==0x1e: rec['xy']=(f64(d,r+2),f64(d,r+10))
            elif d[r+8:r+16]==NEG:
                rec.update(start=u16(d,r),end=u16(d,r+2),flag=u16(d,r+4),type=u16(d,r+16),centre=u16(d,r+20))
            recs.append(rec)
        {'P':P,'L':L,'C':C}.get(kind,other).append(recs) if kind in 'PLC' and len(kind)==1 else other.append((kind,recs))
    return (P[0] if P else []),(L[0] if L else []),(C[0] if C else []),other

SLOT=re.compile(rb'([\x00-\xff][\x80-\xef])([\x00-\xff]{2})\xff\xff\xff\xff',re.S)
CD=re.compile(rb'\xff\xff\x01\x00([\x05-\x40])\x00([A-Za-z_][A-Za-z0-9_]+)')
SGH=('sgPointHandle','sgLineHandle','sgArcHandle','sgEntHandle','sgSplineHandle','sgEllipseHandle','sgSlotHandle','sgParabolaHandle')
def tag_map(d, rel_slots=None):
    cds=[(m.start(),m.group(2)[:m.group(1)[0]].decode()) for m in CD.finditer(d)]
    hc=[(p,c) for p,c in cds if c in SGH]
    first={}
    from sldprt import item_relations as IR
    for r in IR.relation_records(d,0,len(d)):
        for p,(t,i) in enumerate(r['slots']):
            if isinstance(t,int): first.setdefault(t,r['pos'])
    m={}; k=0
    for t in sorted(first):
        while k<len(hc) and hc[k][0]>first[t]: break
        # earliest unassigned class with pos < first use
        j=k
        if j<len(hc) and hc[j][0]<first[t]:
            m[t]=hc[j][1]; k=j+1
    return m
