import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, item_structs as IS
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
d = V.feature_stream(R + 'revdev/RV04 Drisk spacer.SLDPRT'); ev,_=ON.numbering(d)
for e,a,b in CR._obj_spans(d,ev):
    if e.name=='moFavoriteHandle_c' and b-a>300:
        g=lambda o: struct.unpack_from('<d',d,a+o)[0]
        print(b-a, g(52), struct.unpack_from('<H',d,a+68), struct.unpack_from('<I',d,a+150), d[a+155:a+182].hex(), g(182), g(198), d[a+206:a+224].hex()); break
