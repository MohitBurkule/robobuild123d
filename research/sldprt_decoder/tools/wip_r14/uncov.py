"""Round 14 (3): uncovered bytes by class key (ext_abs) on a split of a dump set."""
import sys, os, glob, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, answer_key as AK, fstream as FS
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
src, dumps, split = sys.argv[1], sys.argv[2], int(sys.argv[3])
names = sorted(os.path.basename(p)[:-9] for p in glob.glob(R + dumps + '/*.dump.txt'))
data = [n for n in names if os.path.exists(R + src + '/' + n + '.SLDPRT') and V.feature_stream(R + src + '/' + n + '.SLDPRT') is not None]
U = collections.Counter(); T = collections.Counter(); N = collections.Counter(); per = {}
gap = 0
for k, n in enumerate(data):
    if k % 2 != split: continue
    d = V.feature_stream(R + src + '/' + n + '.SLDPRT')
    dec = V.evaluate(d, AK.parse(R + dumps + '/' + n + '.dump.txt'), V.Acc())
    cov = bytearray(len(d))
    for a, b in dec.spans:
        a, b = max(0, a), min(len(d), b)
        if b > a: cov[a:b] = b'\x01' * (b - a)
    ev, _ = ON.numbering(d); S = int.from_bytes(d[:4], 'little')
    first = ev[0].offset if ev else len(d)
    gap += first - cov[:first].count(1)
    for e, a, b in CR._obj_spans(d, ev):
        key = CR.class_key(e, S, ext_abs=True)
        u = (b - a) - cov[a:b].count(1)
        U[key] += u; T[key] += b - a; N[key] += 1
    per[n] = round(FS.coverage(d, dec.spans), 2)
    print(n, per[n], len(d), flush=True)
tot = sum(T.values())
print('mean', round(sum(per.values()) / len(per), 2), 'pre-first-event uncovered', gap)
for k, u in U.most_common(40): print('%-40s unc %8d of %8d  n=%d' % (k, u, T[k], N[k]))
json.dump(dict(per=per, unc=U.most_common(200)), open('uncov_%s_%d.json' % (dumps, split), 'w'))
