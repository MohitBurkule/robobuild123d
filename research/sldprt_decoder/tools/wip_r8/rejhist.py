"""Histogram of rejected known-class tag candidates in [a, b) by (class, reason, next u16)."""
import sys; sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/')
from common import *
from collections import Counter
nm, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = load()[('revdev', nm)]
ev, fix = ON.numbering(d); cls = {e.index: e.name for e in ev if e.kind == 'def'}; acc = {e.offset for e in ev}
bl = ON.zblobs(d); c = Counter(); ex = {}
for m in ON.REF.finditer(d, a, b):
    o = m.start()
    if o in acc or any(x <= o < y for x, y in bl): continue
    v = u16(d, o) & 0x7fff
    if v in cls:
        k = (cls[v], 'f' if ON.in_float(d, o) else 's' if ON.is_stamp(d, o) else 'o', d[o + 2:o + 4].hex()); c[k] += 1; ex.setdefault(k, o)
for k, n in c.most_common(12): print(n, k, d[ex[k] - 8:ex[k] + 14].hex(' ', 2))
