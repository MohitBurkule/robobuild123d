import sys, os, struct, glob, re
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = sys.argv[1]
L=Counter(); P=Counter(); tot=0
for p in sorted(glob.glob(R+'/*.SLDPRT'))[::int(sys.argv[2])]:
    d = V.feature_stream(p)
    if d is None: continue
    ev,_ = ON.numbering(d)
    for e,a,b in CR._obj_spans(d, ev):
        m=re.match(rb'\xff\xfe\xff(.)((?:D\x00)(?:[0-9]\x00){1,3})', d[a:a+12], re.S)
        if not m or d[a+m.end():a+m.end()+8]!=b'\x00'*6+b'\x00\x40': continue
        j=a+m.end()
        body=d[j:b]; tot+=1
        L[(len(body), e.name or 'ext')]+=1
        if len(body)>=40:
            v=body[23:31]
            P[tuple(i for i in range(0,len(body)-7) if body[i:i+8]==v)]+=1
print(tot); print(L.most_common(12)); print(P.most_common(6))
