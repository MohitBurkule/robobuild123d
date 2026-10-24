import truth, collections
from choose2 import *
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
        E=set(); allnc=set()
        for sg in S.segs:
            a=ser.get((sg['type'],)+sg['id'])
            if a is None: continue
            if not sg['constr']: allnc.add(a)
            if truth.seg_hits(sg,S.sketch_to_model,f.faces): E.add(a)
        chs=choosers(d,s,e,S.id)
        if chs:
            Sel=set(x for c in chs for ce in c['contours'] for ed in ce for x in ed)-{0}
            mode='chooser'
        else:
            Sel=set(allnc); mode='none'
        st[mode,'evid']+=len(E); st[mode,'evid_in_sel']+=len(E&Sel)
        exc=allnc-Sel
        st[mode,'excluded']+=len(exc); st[mode,'excluded_with_face']+=len(exc&E)
        if E-Sel and len(ex)<10: ex.append((n[:10],f.name,S.name,mode,sorted(E-Sel),sorted(Sel),sorted(allnc)))
print(sorted(st.items()))
for x in ex: print(x)
