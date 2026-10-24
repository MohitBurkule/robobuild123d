import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, answer_key as AK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
src, dumps = sys.argv[1], sys.argv[2]
for n in sys.argv[3:]:
    d = V.feature_stream(R + src + '/' + n + '.SLDPRT'); ev, _ = ON.numbering(d); S = int.from_bytes(d[:4], 'little')
    dec = V.evaluate(d, AK.parse(R + dumps + '/' + n + '.dump.txt'), V.Acc())
    cov = bytearray(len(d))
    for a, b in dec.spans:
        a, b = max(0, a), min(len(d), b)
        if b > a: cov[a:b] = b'\x01' * (b - a)
    U = collections.Counter(); first = ev[0].offset if ev else len(d)
    U['<before first event>'] = first - cov[:first].count(1)
    for e, a, b in CR._obj_spans(d, ev): U[CR.class_key(e, S, ext_abs=True)] += (b - a) - cov[a:b].count(1)
    print(n, len(d), 'unc', len(d) - cov.count(1), U.most_common(12))
