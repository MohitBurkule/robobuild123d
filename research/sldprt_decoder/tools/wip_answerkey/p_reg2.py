from sk import *
from sldprt import item_relations as IR
RCD=b'\xff\xff\x01\x00\x10\x00moSketchRegion_c'
def region_lists(d,s,e,treg):
    """find region list headers: [listtag][N] then region objects"""
    out=[]
    starts=[m.start() for m in re.finditer(re.escape(RCD),d[s:e])]
    cands=[s+x-4 for x in starts]
    if treg:
        tb=struct.pack('<H',treg)
        cands+= [s+m.start()-4 for m in re.finditer(re.escape(tb),d[s:e])]
    for h in sorted(set(cands)):
        lt,N=u16(d,h),u16(d,h+2)
        if not (lt&0x8000 and 0<N<500): continue
        j=h+4; regs=[]
        for k in range(N):
            if d[j:j+len(RCD)]==RCD: j+=len(RCD)
            elif treg and u16(d,j)==treg: j+=2
            else: break
            if u16(d,j)!=lt: break
            n=u16(d,j+2); sl,j2=IR.read_slots(d,j+4,n)
            if len(sl)!=n: break
            regs.append(sl); j=j2
        if len(regs)==N: out.append((h,lt,regs,j))
    return out
def treg_of(d):
    p=d.find(RCD)
    if p<0: return None
    j=p+len(RCD); n=u16(d,j+2); sl,j2=IR.read_slots(d,j+4,n)
    t=u16(d,j2)
    return t if t&0x8000 and t not in (0xffff,) else None
if __name__=='__main__':
  want=sys.argv[1:]
  for n,D,d in parts():
    if want and n not in want: continue
    tm=tag_map(d); tr=treg_of(d)
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        P,L,C,O=parse(d,s,e)
        print('==',n[:12],f.name,'contours:',[c[1] for c in f.contours])
        print('   lines',[(r['idx'],r['id'],r.get('flag')) for r in L],'arcs',[(r['idx'],r['id'],r.get('flag')) for r in C])
        for h,lt,regs,j in region_lists(d,s,e,tr):
            print('   REGLIST',hex(h),[[ ((tm.get(t,hex(t)) if isinstance(t,int) else t)[2],i) for t,i in r] for r in regs])
