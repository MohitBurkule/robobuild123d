from sk import *
CC=b'moContourChooser_c'
REF=re.compile(rb'[\x00-\xff][\x80-\xff]\x00\x00[\x00-\xff][\x80-\xff][\x00-\xff]{2}(.{4})(.{4})(.{4})\x00\x00\x00\x00',re.S)
ITEMSIG=b'\x01\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00'
def chooser(d,s,e,sketch_ids):
    """-> list of contours, each a list of edges, each the list of (fid,seq) refs"""
    p=d.find(CC,s,e)
    if p<0: return None
    j=p+len(CC); nC=u16(d,j); j+=2
    out=[]
    for c in range(nC):
        # contour header: tag/classdef then u16 nE
        if d[j:j+2]==b'\xff\xff':
            ln=u16(d,j+4); j+=6+ln
        else: j+=2
        nE=u16(d,j); j+=2
        edges=[]
        for k in range(nE):
            q=d.find(ITEMSIG,j,j+200)
            if q<0: break
            nxt=d.find(ITEMSIG,q+12,e)
            if nxt<0: nxt=e
            refs=[]
            for m in REF.finditer(d,q,nxt):
                fid=u32(d,m.start(1)); seq=u32(d,m.start(3))
                if fid in sketch_ids: refs.append((fid,seq))
            edges.append(refs); j=q+12
        out.append(edges)
    return out
if __name__=='__main__':
  st=collections.Counter(); ex=[]
  for n,D,d in parts():
    R=regions(D,d); sk={f.name:(f,s,e) for f,s,e in R if f.type=='ProfileFeature'}
    sids={f.id:f for f,s,e in R if f.type=='ProfileFeature'}
    for f,s,e in R:
        if f.type=='ProfileFeature': continue
        ch=chooser(d,s,e,set(sids))
        if ch is None: continue
        st['features_with_chooser']+=1
        ex.append((n[:10],f.name,f.type,[[sorted(set(x[1] for x in r)) for r in c] for c in ch]))
  print(st)
  for x in ex[:25]: print(x)
  st=collections.Counter(); ex=[]
  for n,D,d in parts():
    R=regions(D,d)
    for f,s,e in R:
        if f.type!='ProfileFeature': continue
        st['sketch']+=1
        p=s
        while True:
            p=d.find(CC,p,e)
            if p<0: break
            ch=chooser(d,p-10,e,{f.id})
            P,L,C,O=parse(d,s,e)
            a2seg={}
            for r in L: a2seg[r['a']]=(r['idx'],r['id'])
            for r in C: a2seg.setdefault(r['a'],(r['idx'],r['id']))
            st['choosers']+=1
            dc=[set(c[1]) for c in f.contours]
            for c in ch:
                ser=sorted(set(x[1] for r in c for x in r)-{0})
                segs=set(a2seg.get(a,('?',a)) for a in ser)
                best=max([len(segs&x)/max(len(segs|x),1) for x in dc] or [0])
                st['contour_exact' if best==1 else ('contour_partial' if best>0 else 'contour_none')]+=1
                if best<1 and len(ex)<15: ex.append((n[:10],f.name,ser,sorted(segs,key=str),[sorted(x) for x in dc]))
            p+=10
  print(st)
  for x in ex: print(x)
