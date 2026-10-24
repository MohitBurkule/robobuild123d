"""Accepted 'new' tags in [a,b) whose following bytes resemble no other instance of the same class."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from collections import defaultdict
D = load(); nm, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = D[('revdev', nm)] if ('revdev', nm) in D else D[('corpus', nm)]
ev, fix = ON.numbering(d)
S = struct.unpack_from('<I', d, 0)[0]
def g(p): x = d[p:p + 24]; return {x[i:i + 3] for i in range(len(x) - 2)}
by = defaultdict(list)
for e in ev: by[e.cls].append(e)
for e in ev:
    if not (a <= e.offset < b) or e.kind != 'new': continue
    ge = g(e.end); best = 0
    for f in by[e.cls]:
        if f is e: continue
        gf = g(f.end); u = len(ge | gf); best = max(best, len(ge & gf) / u if u else 0)
    if best < 0.3:
        print(e.offset, e.obj, e.cls, e.name or 'ext[S-%d]' % (S - e.cls), len(by[e.cls]), round(best, 2), d[e.offset - 6:e.end + 14].hex(' ', 2))
