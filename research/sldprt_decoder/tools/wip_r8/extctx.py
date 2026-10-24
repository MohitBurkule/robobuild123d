"""Context statistics of external-class tags (class index < S): accepted vs rejected, by (S-v, prev4, follow byte pattern)."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from collections import Counter, defaultdict
D = load()
acc_c = Counter(); rej_c = Counter()
for (s, nm), d in D.items():
    S = struct.unpack_from('<I', d, 0)[0]
    ev, _ = ON.numbering(d)
    acc = {e.offset for e in ev}
    for m in ON.REF.finditer(d):
        o = m.start(); v = u16(d, o) & 0x7fff
        if 0 < v < S and o >= 4:
            key = (S - v, d[o - 4:o].hex(), d[o + 4:o + 6].hex())
            if ON.in_float(d, o): continue
            (acc_c if o in acc else rej_c)[key] += 1
print('top rejected contexts')
for k, n in rej_c.most_common(40): print(n, acc_c.get(k, 0), k)
