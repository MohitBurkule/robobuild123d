import sys, os, glob
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, fstream as FS, item_structs as IS
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
C=Counter(); B=Counter()
for n in sys.argv[1:]:
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d); fids={h.feature_id for h in FS.feature_headers(d)}
    sp=list(CR._obj_spans(d,ev)); r=IS.decode(d,sp,fids)
    tot=Counter(e.name or 'ext' for e,a,b in sp)
    for c,o,e,f in r: C[c]+=1; B[c]+=e-o
    print(n, Counter(c for c,*_ in r), 'moFR total', tot['moFR_c'], 'fav', tot['moFavoriteHandle_c'])
print(C,B)
