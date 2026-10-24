"""Round 12: per residual interval (between fixed ClassDefs), the net counting error and the candidate tags in it."""
import sys, os, struct, bisect
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
for n in sys.argv[1:]:
    src = R + ('revdev/' if os.path.exists(R + 'revdev/' + n + '.SLDPRT') else 'corpus/') + n + '.SLDPRT'
    d = V.feature_stream(src); ev, fix = ON.numbering(d)
    S = struct.unpack_from('<I', d, 0)[0]
    acc = {e.offset: e for e in ev}; names = {e.cls: e.name for e in ev if e.kind == 'def'}
    res = [r for r in ON.numbering.residuals if r[1]]
    print(n, 'residuals', res)
    prev = 0
    allr = ON.numbering.residuals
    for k, (o, r) in enumerate(allr):
        lo = allr[k - 1][0] if k else 0
        if r == 0: continue
        cands = Counter()
        for m in ON.REF.finditer(d, lo, o):
            p = m.start(); v = ON.u16(d, p)
            if p in acc or v == 0xffff: continue
            a = v & 0x7fff
            if a not in names and not 0 < a < S: continue
            if not any(x in acc for x in (p + 2, p + 4, p + 6, p + 10, p + 12)): continue
            why = 'float' if ON.in_float(d, p) else 'stamp' if ON.is_stamp(d, p) else 'rej' if p in ON._numbering7.reject else 'other'
            cands[(names.get(a) or 'S-%d' % (S - a), why)] += 1
        print('  interval', lo, o, 'delta', r, 'span', o - lo, 'cands', cands.most_common(8))
