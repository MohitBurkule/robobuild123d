import sys, os, struct
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
for n in sys.argv[1:]:
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d); S=struct.unpack_from('<I',d,0)[0]
    names={e.cls:e.name for e in ev if e.kind=='def'}
    c=Counter(); w=Counter()
    for e,a,b in CR._obj_spans(d,ev):
        if e.name!='moFR_c': continue
        L=b-a; c[(L-10)%4]+=1
        for i in range(a+10, b-1, 2):
            v=struct.unpack_from('<H',d,i)[0]
            if v&0x8000 and v!=0xffff and (v&0x7fff) in names: w[names[v&0x7fff]]+=1
    print(n, c, w.most_common(8))
