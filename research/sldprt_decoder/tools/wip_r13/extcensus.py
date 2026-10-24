"""Round 13: ext-class census on dumps_ab.  Per file: uncovered bytes and instance count
per enclosing class (ext classes keyed S-k); per class: groups where it appears."""
import sys, os, glob, struct, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, answer_key as AK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dumps_ab/')
out = {}
for p in sorted(glob.glob(R + '*.dump.txt')):
    n = os.path.basename(p)[:-9]
    if not os.path.exists(R + n + '.SLDPRT'): continue
    d = V.feature_stream(R + n + '.SLDPRT')
    if d is None: continue
    dec = V.evaluate(d, AK.parse(p), V.Acc())
    cov = bytearray(len(d))
    for a, b in dec.spans:
        a, b = max(0, a), min(len(d), b)
        if b > a: cov[a:b] = b'\x01' * (b - a)
    ev, _ = ON.numbering(d); S = struct.unpack_from('<I', d, 0)[0]
    U = Counter(); N = Counter(); L = defaultdict(Counter); EX = defaultdict(list)
    for e, a, b in CR._obj_spans(d, ev):
        nm = e.name or ('S-%d' % (S - e.cls))
        U[nm] += (b - a) - sum(cov[a:b]); N[nm] += 1; L[nm][b - a] += 1
        if len(EX[nm]) < 3: EX[nm].append((a, d[a:min(b, a + 64)].hex()))
    out[n] = {'S': S, 'len': len(d), 'unc': len(d) - sum(cov), 'U': U, 'N': N,
              'L': {k: v.most_common(3) for k, v in L.items()}, 'EX': EX}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extcensus.json'), 'w'))
print(len(out), 'files; S values', Counter(v['S'] for v in out.values()).most_common(5))
