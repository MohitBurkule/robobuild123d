from choose2 import *
def edge_refs(d,a,b,sid):
    return [u32(d,m.start(3)) for m in REF.finditer(d,a,b) if u32(d,m.start(1))==sid]
def scan(d,s,e,sid):
    """-> regions [{'rid','edges'}], choosers [[edges...]]"""
    items=[m.start() for m in SIG.finditer(d,s,e)]
    heads=[]
    for k,q in enumerate(items):
        cdE=d.rfind(b'\xff\xff\x01\x00\x0b\x00moEdgeRef_c',max(s,q-20),q)
        p=cdE if cdE>=0 else q-2
        if cdE<0 and not (u16(d,p)&0x8000): continue
        nE=u16(d,p-2); h=p-2
        cdO=d.rfind(b'\xff\xff\x01\x00\x0e\x00moOneContour_c',max(s,h-22),h)
        if cdO>=0: po=cdO
        else:
            po=h-2
            if not (u16(d,po)&0x8000): continue
        if not (0<nE<2000): continue
        tagOC = 'cd' if cdO>=0 else u16(d,po)
        heads.append((k,q,nE,po,tagOC))
    regs=[];chs=[];cur=None
    for hi,(k,q,nE,po,tagOC) in enumerate(heads):
        edges=[]
        for j in range(k,min(k+nE,len(items))):
            a=items[j]; b=items[j+1] if j+1<len(items) else e
            edges.append(edge_refs(d,a,b,sid))
        if d[po-6:po-4]==b'\x01\x00' and 100000<=u32(d,po-4)<101000:
            regs.append({'rid':u32(d,po-4)-100000,'edges':edges,'pos':q}); cur=None
        elif cur is not None and len(cur['contours'])<cur['n'] and (tagOC==cur['tagOC'] or cur['tagOC']=='cd'):
            cur['contours'].append(edges)
            if cur['tagOC']=='cd': cur['tagOC']=tagOC
        elif d[po-20:po-2]==b'moContourChooser_c' or (u16(d,po-4)&0x8000 and 0<u16(d,po-2)<500):
            cur={'pos':q,'n':u16(d,po-2),'contours':[edges],'tagOC':tagOC}; chs.append(cur)
        elif not regs and tagOC=='cd':
            regs.append({'rid':None,'edges':edges,'pos':q})
    return regs,chs
if __name__=='__main__':
    for n,D,d in parts():
        if n not in sys.argv[1:]: continue
        for f,s,e in regions(D,d):
            if f.type!='ProfileFeature': continue
            regs,chs=scan(d,s,e,f.id)
            if not regs and not chs: continue
            print(n,f.name,'regions',[(r['rid'],sorted(set(x for ed in r['edges'] for x in ed))) for r in regs])
            for c in chs: print('   chooser n=',c['n'],[sorted(set(x for ed in ce for x in ed)) for ce in c['contours']])
