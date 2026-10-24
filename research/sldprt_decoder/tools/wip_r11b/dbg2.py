import sys, os, struct
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, item_structs as IS
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
d = V.feature_stream(R + 'revdev/RV23 side panel LH.SLDPRT'); ev,_=ON.numbering(d); S=struct.unpack_from('<I',d,0)[0]
c=Counter(); ex=[]
for e,a,b in CR._obj_spans(d,ev):
    if not e.name and S-e.cls==146:
        r=IS.named_item(d,a,b,set()); c[bool(r)]+=1
        if not r and len(ex)<4: ex.append(d[a:a+80].hex(' ',2))
print(c); print('\n'.join(ex))
