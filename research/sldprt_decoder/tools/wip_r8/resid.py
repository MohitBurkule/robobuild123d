"""For residual intervals (between a fixed ClassDef and the previous def), list rejected tag candidates."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from collections import Counter
D = load()
reasons = Counter(); n_int = 0
for (src, nm), d in sorted(D.items()):
    S = struct.unpack_from('<I', d, 0)[0]
    ev, fix = ON.numbering(d)
    res = dict(ON.numbering.residuals)
    defs = [e for e in ev if e.kind == 'def']
    acc = {e.offset for e in ev}
    for k in range(1, len(defs)):
        r = res.get(defs[k].offset, 0)
        if r <= 0 or r > 3: continue
        a, b = defs[k - 1].end, defs[k].offset
        if b - a > 30000: continue
        n_int += 1
        known = {e.index for e in defs[:k]}
        rows = []
        for m in ON.REF.finditer(d, a, b):
            o = m.start()
            if o in acc: continue
            v = u16(d, o) & 0x7fff
            if v in known: why = 'float' if ON.in_float(d, o) else 'stamp' if ON.is_stamp(d, o) else 'other'
            elif 0 < v < S: why = 'extfloat' if ON.in_float(d, o) else 'ext' if not ON.ext_ok(d, o) else 'ext-other'
            else: continue
            rows.append((o, v, why, d[o - 4:o + 10].hex()))
        for x in rows: reasons[x[2]] += 1
        if '-v' in sys.argv and len(rows) <= 6:
            print(nm[:14], a, b, 'r=%d' % r, rows)
print(n_int, reasons)
