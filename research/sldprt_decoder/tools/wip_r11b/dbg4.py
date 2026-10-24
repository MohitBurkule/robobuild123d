import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
n,k=sys.argv[1],int(sys.argv[2])
d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d); S=struct.unpack_from('<I',d,0)[0]
acc={e.offset for e in ev}; c=0
for m in ON.REF.finditer(d):
    o=m.start(); v=ON.u16(d,o)
    if o in acc or (v&0x7fff)!=S-k or not any(x in acc for x in (o+2,o+4,o+6)): continue
    print(hex(o), d[o-12:o+16].hex(' ',2)); c+=1
    if c>5: break
