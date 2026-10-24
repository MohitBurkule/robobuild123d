import sys, os, glob, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
n=sys.argv[1]; want=sys.argv[2:]
d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d); S=struct.unpack_from('<I',d,0)[0]
spans=list(CR._obj_spans(d,ev)); c={}
for k,(e,a,b) in enumerate(spans):
    nm=e.name or 'S-%d'%(S-e.cls)
    if nm in want and c.get(nm,0)<5:
        c[nm]=c.get(nm,0)+1
        prev=spans[k-1][0]; pn=prev.name or 'S-%d'%(S-prev.cls)
        nx=spans[k+1][0] if k+1<len(spans) else None
        print(nm,'obj',e.obj,'len',b-a,'prev',pn,'next',(nx.name or 'S-%d'%(S-nx.cls)) if nx else None); print('  ',d[e.offset:b].hex(' ',4))
