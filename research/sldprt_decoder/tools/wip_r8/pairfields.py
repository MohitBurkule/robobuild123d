"""Match pair-diff double changes to dump deltas (old -> new value pairs from the two dumps)."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
import re, json, pairdiff
from collections import Counter, defaultdict
DUMPS = '/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
NUM = re.compile(r'-?\d+\.?\d*(?:E-?\d+)?')
def deltas(A, B):
    la = open(DUMPS + A + '.dump.txt', errors='replace').read().replace(A, 'X').splitlines()
    lb = open(DUMPS + B + '.dump.txt', errors='replace').read().replace(B, 'X').splitlines()
    out = defaultdict(set)    # (old,new) -> labels
    def keyed(ls):
        out, seen = {}, Counter()
        for x in ls:
            t = x.strip().split(' ')
            k = ' '.join(t[:2]) if t and t[0] in ('DIM', 'PT', 'SEG', 'FEAT', 'SKETCH') else (t[0] if t else '')
            seen[k] += 1
            out[(k, seen[k])] = x
        return out
    ka, kb = keyed(la), keyed(lb)
    for key in ka:
        x, y = ka[key], kb.get(key)
        if y is None or x == y: continue
        na = [float(v) for v in NUM.findall(x)]; nb = [float(v) for v in NUM.findall(y)]
        lab = x.strip().split(' ')[0] + ' ' + (x.strip().split(' ')[1] if ' ' in x.strip() else '')
        for p, q in zip(na, nb):
            if p != q: out[(p, q)].add(lab)
    return out
def match(A, B):
    dl = deltas(A, B)
    r = pairdiff.run(A, B)
    hits = Counter(); unexplained = Counter(); found = defaultdict(set); ex = {}
    for c in r['changed']:
        for s, x, y in c['doubles']:
            labs = set()
            for (p, q), l in dl.items():
                for sc in (1, 1000):      # dump in m; some fields mm?
                    if abs(x - p * sc) < 1e-12 + 1e-9 * abs(p * sc) and abs(y - q * sc) < 1e-12 + 1e-9 * abs(q * sc):
                        labs |= l; found[(p, q)].add(c['cls'])
            key = (c['cls'], s)
            if labs: hits[key] += 1; ex[key] = sorted(labs)[:3]
            else: unexplained[key] += 1
    tot = len(dl); got = sum(1 for k in dl if k in found)
    return dict(dump_deltas=tot, deltas_found_in_stream=got,
                fields=[(k[0], 'off+%d' % k[1], n, ex[k]) for k, n in hits.most_common(30)],
                unexplained_double_changes=[(k[0], 'off+%d' % k[1], n) for k, n in unexplained.most_common(15)],
                missing=[(k, sorted(v)) for k, v in dl.items() if k not in found][:20])
if __name__ == '__main__':
    out = {}
    for A, B in (('fork 5', 'fork 5 long'), ('RV21 Rear Wheel', 'RV21 oversize Rear Wheel')):
        m = match(A, B); out[A + ' | ' + B] = m
        print('==', A, '|', B, 'dump deltas', m['dump_deltas'], 'found', m['deltas_found_in_stream'])
        for f in m['fields']: print('  ', f)
        print('  unexplained', m['unexplained_double_changes'][:8])
        print('  missing', m['missing'][:10])
    json.dump(out, open('/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/pairdiff_round8.json', 'w'), indent=1, default=str)
