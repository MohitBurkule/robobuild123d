import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dumps_ab/')
n, cls, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv)>3 else 6
d = V.feature_stream(R + n + '.SLDPRT'); ev,_ = ON.numbering(d)
for e,a,b in CR._obj_spans(d, ev):
    if e.cls == cls and e.kind=='new':
        print(a, b-a, d[a:b].hex()); k-=1
        if not k: break
