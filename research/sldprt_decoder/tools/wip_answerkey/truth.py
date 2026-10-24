"""face-evidence truth: which dump contours of the parent sketch produced faces of an extrude"""
import math
from common import *
def xf(T,p):
    R=T[:9]; t=T[9:12]
    x,y,z=p
    # row-vector convention p*R + t
    return (x*R[0]+y*R[3]+z*R[6]+t[0], x*R[1]+y*R[4]+z*R[7]+t[1], x*R[2]+y*R[5]+z*R[8]+t[2])
def sub(a,b): return tuple(i-j for i,j in zip(a,b))
def dot(a,b): return sum(i*j for i,j in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def nrm(a):
    l=math.sqrt(dot(a,a)); return tuple(i/l for i in a) if l>1e-15 else a
def seg_hits(sg,T,faces,tol=1e-7):
    if sg['type']==0:
        a,b=xf(T,sg['p0']),xf(T,sg['p1'])
        for fc in faces:
            if fc['kind']=='plane' and 'n' in fc:
                n=nrm(fc['n']); o=fc['o']
                if abs(dot(sub(a,o),n))<tol and abs(dot(sub(b,o),n))<tol and abs(dot(nrm(sub(b,a)),n))<1e-6: return True
    elif sg['type']==1 and 'c' in sg:
        c=xf(T,sg['c']); r=sg.get('r')
        for fc in faces:
            if fc['kind']=='cyl' and 'ax' in fc and r and abs(fc['r']-r)<1e-8:
                ax=nrm(fc['ax']); v=sub(c,fc['o']); w=cross(v,ax)
                if math.sqrt(dot(w,w))<1e-7: return True
    return False
def contour_truth(D,f):
    """-> (sketch Feat, [used? per contour]) or None"""
    sk=[p for p,t in f.parents if t=='ProfileFeature']
    if not sk: return None
    S=[x for x in D.top() if x.name==sk[0]]
    if not S or not S[0].sketch_to_model: return None
    S=S[0]; T=S.sketch_to_model
    from sldprt.answer_key import resolve_contour
    res=[]
    for closed,ids in S.contours:
        res.append(any(seg_hits(sg,T,f.faces) for sg in resolve_contour(S,ids) if sg))
    return S,res
if __name__=='__main__':
    import collections
    st=collections.Counter()
    for n,D,d in parts():
        for f in D.by_type('Extrusion','ICE'):
            r=contour_truth(D,f)
            if not r: st['nosk']+=1; continue
            S,res=r
            st['contours']+=len(res); st['used']+=sum(res)
            st['feat_partial' if 0<sum(res)<len(res) else ('feat_all' if all(res) else 'feat_none')]+=1
    print(st)
