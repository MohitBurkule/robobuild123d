import sys, os, struct, glob
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
T=[]
for p in sorted(glob.glob(R+'dumps_v2/*.dump.txt'))[:12]:
    n=os.path.basename(p)[:-9]; d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d)
    for e,a,b in CR._obj_spans(d,ev):
        if e.name=='moFavoriteHandle_c' and d[a+4:a+8]==b'\xff'*4: T.append(d[a:b])
print(len(T), Counter(len(t) for t in T).most_common(8))
row=[]
for i in range(52,440):
    c=Counter(t[i] for t in T if len(t)>i); v,m=c.most_common(1)[0]
    row.append('%02x'%v if m>=0.97*sum(c.values()) else '..')
for k in range(0,len(row),32): print(52+k, ' '.join(row[k:k+32]))
