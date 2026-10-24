import sys, os, struct, glob, re
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, answer_key as AK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dumps_ab/')
cls=int(sys.argv[1]); U=Counter(); N=Counter(); EX={}
for p in sorted(glob.glob(R+'*.dump.txt'))[::int(sys.argv[2])]:
    n=os.path.basename(p)[:-9]
    if not os.path.exists(R+n+'.SLDPRT'): continue
    d = V.feature_stream(R + n + '.SLDPRT'); ev,_ = ON.numbering(d)
    dec = V.evaluate(d, AK.parse(p), V.Acc())
    cov = bytearray(len(d))
    for a, b in dec.spans:
        a, b = max(0, a), min(len(d), b)
        if b > a: cov[a:b] = b'\x01' * (b - a)
    for e,a,b in CR._obj_spans(d, ev):
        if e.cls == cls and e.kind=='new':
            m=re.match(rb'\xff\xfe\xff(.)', d[a:a+4], re.S)
            nm = d[a+4:a+4+2*m.group(1)[0]].decode('utf-16-le','replace') if m else '?'
            nm = re.sub(r'\d+','#',nm)
            u=(b-a)-sum(cov[a:b]); U[nm]+=u; N[nm]+=1
            if u>50 and nm not in EX: EX[nm]=(n,a,b-a)
for k,v in U.most_common(25): print(k, v, N[k], EX.get(k))
