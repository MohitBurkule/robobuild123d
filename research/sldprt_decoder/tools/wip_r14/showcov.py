import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, answer_key as AK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
src, dumps, n, key, k = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
d = V.feature_stream(R + src + '/' + n + '.SLDPRT'); ev, _ = ON.numbering(d); S = int.from_bytes(d[:4], 'little')
dec = V.evaluate(d, AK.parse(R + dumps + '/' + n + '.dump.txt'), V.Acc())
cov = bytearray(len(d))
for a, b in dec.spans:
    a, b = max(0, a), min(len(d), b)
    if b > a: cov[a:b] = b'\x01' * (b - a)
pat = collections.Counter()
for e, a, b in CR._obj_spans(d, ev):
    if CR.class_key(e, S, ext_abs=True) != key: continue
    if cov[a:b].count(1) == b - a: continue
    s = ''.join((d[i:i+1].hex() if cov[i] else d[i:i+1].hex().upper()) for i in range(a, min(b, a + 90)))
    pat[(b - a, ''.join('c' if cov[i] else 'U' for i in range(a, b)))] += 1
    if k > 0: print(a, b - a, s); k -= 1
for (L, m), c in pat.most_common(8): print(c, L, m[:120])
