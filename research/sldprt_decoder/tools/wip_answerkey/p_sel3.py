import truth, collections
from regsel import *
st=collections.Counter(); ex=[]
for n,D,d in parts():
    R={f.name:(f,s,e) for f,s,e in regions(D,d)}
    for f in D.by_type('Extrusion','ICE'):
        sk=[p for p,t in f.parents if t=='ProfileFeature']
        if not sk: continue
        S=[x for x in D.top() if x.name==sk[0]]
        if not S: continue
        S=S[0]
        if not S.sketch_to_model: continue
        _,s,e=R[S.name]
        P,L,C,O=parse(d,s,e)
        ser={}
        for r in L: ser[(0,)+(r['idx'],r['id'])]=r['a']
        for r in C: ser[(1,)+(r['idx'],r['id'])]=r['a']
        E=set(); allnc=set(); geo={}
        import math
        for sg in S.segs:
            a=ser.get((sg['type'],)+sg['id'])
            if a is None: continue
            if sg['type']==0:
                (x0,y0,_),(x1,y1,_)=sg['p0'],sg['p1']; dx,dy=x1-x0,y1-y0; L_=math.hypot(dx,dy) or 1
                nx,ny=-dy/L_,dx/L_
                if nx<0 or (nx==0 and ny<0): nx,ny=-nx,-ny
                geo[a]=('L',round(nx,5),round(ny,5),round(nx*x0+ny*y0,7))
            elif sg['type']==1 and 'c' in sg:
                geo[a]=('C',round(sg['c'][0],7),round(sg['c'][1],7),round(sg.get('r',0),7))
        for sg in S.segs:
            a=ser.get((sg['type'],)+sg['id'])
            if a is None: continue
            if not sg['constr']: allnc.add(a)
            if truth.seg_hits(sg,S.sketch_to_model,f.faces): E.add(a)
        regs,chs=scan(d,s,e,S.id)
        if chs:
            Sel0=set(x for c in chs for ce in c['contours'] for ed in ce for x in ed)-{0}; RS=set(x for r in regs for ed in r['edges'] for x in ed)
            mode='chooser'
            gs=set(geo[a] for a in Sel0 if a in geo)
            Sel=Sel0|set(a for a,g in geo.items() if g in gs)
        else:
            Sel=set(allnc); mode='none'
        st[mode,'evid']+=len(E); st[mode,'evid_in_sel']+=len(E&Sel)
        exc=(allnc-Sel) if mode=='none' else ((allnc&RS)-Sel)
        st[mode,'excluded']+=len(exc); st[mode,'excluded_with_face']+=len(exc&E)
        if E-Sel and len(ex)<10: ex.append((n[:10],f.name,S.name,mode,sorted(E-Sel),sorted(Sel),sorted(allnc)))
print(sorted(st.items()))
for x in ex: print(x)
