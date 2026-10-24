import sys, os, struct
from collections import Counter
sys.path.insert(0, '..')
from sldprt import validate as V, objnum as ON
d = V.feature_stream('../../revdev/' + sys.argv[1] + '.SLDPRT')
ev, fix = ON.numbering(d); acc = {e.offset for e in ev}; names = {e.cls: e.name for e in ev if e.kind == 'def'}
for lo, hi in [tuple(map(int, x.split(':'))) for x in sys.argv[2:]]:
    c = Counter(); ex = {}
    for m in ON.REF.finditer(d, lo, hi):
        p = m.start(); v = ON.u16(d, p)
        if p in acc or v == 0xffff or (v & 0x7fff) not in names: continue
        why = 'float' if ON.in_float(d, p) else 'stamp' if ON.is_stamp(d, p) else 'rej' if p in ON._numbering7.reject else 'other'
        k = (names[v & 0x7fff], why); c[k] += 1; ex.setdefault(k, []).append(d[p:p+14].hex())
    print(lo, hi)
    for k, n in c.most_common(25): print('  ', n, k, ex[k][:3])
