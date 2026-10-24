import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
import dp2
D = load()
nm = sys.argv[1]; d = D[('revdev', nm)] if ('revdev', nm) in D else D[('corpus', nm)]
S = struct.unpack_from('<I', d, 0)[0]; ev = ON._events(d)
base, fix = ON.numbering(d)
for it in range(3):
    f2, defs = dp2.assign(d, base=base)
    cur = {e.offset: (e.index, e.name, e.end) for e in defs}
    f2 = {o: v for o, v in f2.items() if cur[o][0] != v}
    if not f2: break
    for o, v in sorted(f2.items()):
        i, n, e = cur[o]
        ps = [m.start() for m in __import__('re').finditer(struct.pack('<H', 0x8000 | v), d) if m.start() > e][:3]
        print(it, o, n, i, '->', v, d[e:e+16].hex(), [d[p+2:p+18].hex() for p in ps[:2]])
    fix = {**fix, **f2}; base = ON.number(d, fix, S, ev)
