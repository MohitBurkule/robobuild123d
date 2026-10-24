from sk import *
REF=re.compile(rb'[\x00-\xff][\x80-\xff]\x00\x00[\x00-\xff][\x80-\xff][\x00-\xff]{2}(.{4})(.{4})(.{4})\x00\x00\x00\x00',re.S)
SIG=re.compile(rb'\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00[\x00-\xff][\x00\x03]\x00\x00\x00\x00\x00\x00',re.S)
def contour_sets(d,s,e,sid):
    items=[m.start() for m in SIG.finditer(d,s,e)]
    out=[]  # list of choosers: list of contours: list of edges(serial sets)
    cur=None; k=0
    while k<len(items):
        q=items[k]
        is_cls = d[q-14:q]==b'moEdgeRef_c' or d.rfind(b'moEdgeRef_c',q-20,q)>=0
        nE=u16(d,q-4); t6=u16(d,q-6)
        hdr = (t6&0x8000 and 0<nE<1000) or is_cls
        if not hdr: k+=1; continue
        if is_cls:
            # classdef form: ... u16 nE? 'ff ff 01 00 len moEdgeRef_c' ; nE before classdef
            p=d.rfind(b'\xff\xff\x01\x00\x0b\x00moEdgeRef_c',q-30,q)
            nE=u16(d,p-2)
        edges=[]
        for j in range(k,min(k+nE,len(items))):
            a=items[j]; b=items[j+1] if j+1<len(items) else e
            refs=[]
            for m in REF.finditer(d,a,b):
                if u32(d,m.start(1))==sid: refs.append(u32(d,m.start(3)))
            edges.append(refs)
        out.append((q,edges)); k+=max(nE,1)
    return out

def choosers(d,s,e,sid):
    cs=contour_sets(d,s,e,sid)
    out=[];k=0
    while k<len(cs):
        q,edges=cs[k]
        # first contour of a chooser: [tagCC|classdef][nC][tagOC|classdef][nE][tagER|classdef]SIG
        p=q
        # walk back over edge class (tag or classdef)
        cdE=d.rfind(b'\xff\xff\x01\x00\x0b\x00moEdgeRef_c',q-30,q)
        p = cdE if cdE>=0 else q-2
        p-=2  # nE
        cdO=d.rfind(b'\xff\xff\x01\x00\x0e\x00moOneContour_c',p-25,p)
        p = cdO if cdO>=0 else p-2
        nC=u16(d,p-2)
        if 0<nC<200 and (d[p-2-18:p-2]==b'moContourChooser_c' or u16(d,p-4)&0x8000):
            out.append({'pos':p-2,'contours':[x[1] for x in cs[k:k+nC]],'is_chooser':d[p-2-18:p-2]==b'moContourChooser_c' or True})
            k+=nC
        else:
            out.append({'pos':q,'contours':[edges],'orphan':True}); k+=1
    return out
