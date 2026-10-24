import sys, os, struct, glob, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dumps_ab/')
objs={}
for n in sys.argv[2:]:
    d = V.feature_stream(R + n + '.SLDPRT'); ev,_ = ON.numbering(d)
    for e,a,b in CR._obj_spans(d, ev):
        if e.cls==4 and d[a:a+4]==b'\xff\xfe\xff\x02' and d[a+4:a+8]==sys.argv[1].encode('utf-16-le'):
            objs[n]=d[a:b]; break
L=Counter=None
base=list(objs.values())[0]
for n,o in objs.items():
    diffs=[i for i in range(min(len(o),len(base))) if o[i]!=base[i]]
    print(n[:30], len(o), 'diff8:', sorted({i//8*8 for i in diffs})[:40])
for i in range(0,len(base)-7):
    pass
