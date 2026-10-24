"""Round 11b: uncovered bytes by enclosing object class (ext classes named S-k), dumps_v2 parts."""
import sys, os, glob, struct, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, fstream as FS, answer_key as AK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
U = Counter(); N = Counter(); L = defaultdict(Counter); tot = 0
for p in sorted(glob.glob(R + 'dumps_v2/*.dump.txt')):
    n = os.path.basename(p)[:-9]; d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT')
    dec = V.evaluate(d, AK.parse(p), V.Acc())
    cov = bytearray(len(d))
    for a, b in dec.spans:
        cov[max(0, a):min(len(d), b)] = b'\x01' * (min(len(d), b) - max(0, a))
    ev, _ = ON.numbering(d); S = struct.unpack_from('<I', d, 0)[0]
    for e, a, b in CR._obj_spans(d, ev):
        nm = e.name or ('S-%d' % (S - e.cls))
        u = (b - a) - sum(cov[a:b]); U[nm] += u; N[nm] += 1; L[nm][b - a] += 1
    tot += len(d) - sum(cov)
print('total uncovered', tot)
for k, v in U.most_common(40): print(f'{k:40s} {v:9d} {100*v/tot:5.1f}%  n={N[k]} lens={L[k].most_common(4)}')
