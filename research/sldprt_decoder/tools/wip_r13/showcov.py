import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, answer_key as AK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dumps_ab/')
n, cls, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv)>3 else 6
d = V.feature_stream(R + n + '.SLDPRT'); ev,_ = ON.numbering(d)
dec = V.evaluate(d, AK.parse(R+n+'.dump.txt'), V.Acc())
cov = bytearray(len(d))
for a, b in dec.spans:
    a, b = max(0, a), min(len(d), b)
    if b > a: cov[a:b] = b'\x01' * (b - a)
for e,a,b in CR._obj_spans(d, ev):
    if e.cls == cls and e.kind=='new':
        s=''.join((d[i:i+1].hex() if cov[i] else d[i:i+1].hex().upper()) for i in range(a,b))
        print(a, b-a, s); k-=1
        if not k: break
