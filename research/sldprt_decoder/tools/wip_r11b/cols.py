import sys, os, struct
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
def cend(b, i):
    if b[i:i+3] != b'\xff\xfe\xff': return None
    n = b[i+3]
    return i+4+2*n
for n, k in [a.split(':') for a in sys.argv[1:]]:
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d); S=struct.unpack_from('<I',d,0)[0]
    T=[]; L=Counter()
    for e,a,b in CR._obj_spans(d,ev):
        if e.name or S-e.cls!=int(k): continue
        j=cend(d,a)
        if j is None: L['nocstr']+=1; continue
        T.append(d[j:b]); L[b-j]+=1
    print(n, k, len(T), L.most_common(6))
    row=[]
    for i in range(160):
        c=Counter(t[i] for t in T if len(t)>i); v,m=c.most_common(1)[0]
        row.append('%02x'%v if m>=0.97*sum(c.values()) else '..')
    print(' '.join(row))
    for t in [t for t in T if len(t) in (65,66)][:6]: print('  ', len(t), t.hex(' ',2))
