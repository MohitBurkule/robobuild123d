import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
d = V.feature_stream(R + 'revdev/RV01 Chassis.SLDPRT'); ev,_=ON.numbering(d)
names={e.cls:e.name for e in ev if e.kind=='def'}; k=0
for e,a,b in CR._obj_spans(d,ev):
    if e.name!='moFR_c': continue
    for i in range(a+10,b-1,2):
        v=struct.unpack_from('<H',d,i)[0]
        if v&0x8000 and v!=0xffff and names.get(v&0x7fff)=='moFilletSurfIdRep_c':
            print(hex(i), (i-a), d[e.offset:b+8].hex(' ',2), 'float',ON.in_float(d,i),'stamp',ON.is_stamp(d,i), 'rej', i in ON._numbering7.reject); k+=1
    if k>4: break
