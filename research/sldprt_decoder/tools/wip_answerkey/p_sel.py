import truth, collections
from choose2 import *
def contour_serials(d,s,e,S):
    """map each dump contour of sketch S to set of entity serials 'a'"""
    P,L,C,O=parse(d,s,e)
    m={}
    for r in L: m[(0,r['idx'],r['id'])]=r['a']
    for r in C: m[(1,r['idx'],r['id'])]=r['a']
    from sldprt.answer_key import resolve_contour
    out=[]
    for closed,ids in S.contours:
        out.append(set(m.get((sg['type'],)+sg['id']) for sg in resolve_contour(S,ids) if sg)-{None})
    return out
st=collections.Counter(); ex=[]
for n,D,d in parts():
    R={f.name:(f,s,e) for f,s,e in regions(D,d)}
    for f in D.by_type('Extrusion','ICE'):
        r=truth.contour_truth(D,f)
        if not r: continue
        S,res=r
        if not any(res): continue
        _,s,e=R[S.name]
        cser=contour_serials(d,s,e,S)
        chs=choosers(d,s,e,S.id)
        if not chs:
            pred=[True]*len(res); mode='nochooser'
        else:
            mode='chooser'
            sel=set()
            for c in chs:
                for edges in c['contours']:
                    sel|=set(x for ed in edges for x in ed)
            pred=[len(cs&sel)>0 for cs in cser]
        part='partial' if not all(res) else 'all'
        ok=pred==res
        st[mode,part,ok]+=1
        if not ok and len(ex)<12: ex.append((n[:12],f.name,S.name,mode,res,pred,[sorted(x) for x in cser],[[sorted(set(x for ed in ce for x in ed)) for ce in c['contours']] for c in chs][:4]))
print(sorted(st.items(),key=str))
for x in ex: print(x)
