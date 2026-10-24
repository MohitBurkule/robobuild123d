import sys, os, struct
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
for n, k in [a.split(':') for a in sys.argv[1:]]:
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d); S=struct.unpack_from('<I',d,0)[0]
    T=[d[a:b] for e,a,b in CR._obj_spans(d,ev) if not e.name and S-e.cls==int(k)]
    L=Counter(len(t) for t in T); print(n,k,len(T),L.most_common(6))
    for ln,_ in L.most_common(3):
        for t in [t for t in T if len(t)==ln][:2]: print('  ',ln,t.hex(' ',4))
