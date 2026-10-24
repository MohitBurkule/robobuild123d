import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from collections import Counter
D = load()
for nm in sys.argv[1:]:
    d = D[('revdev', nm)]
    ev, _ = ON.numbering(d)
    byobj = {e.obj: e for e in ev}
    hdr = FS.feature_headers(d); fo = ON.feature_objects(d, hdr, ev)
    fobjs = {i: c for h, i, c in fo.values()}
    S = struct.unpack_from('<I', d, 0)[0]
    c = Counter(); rows = []
    for e in ev:
        if e.kind == 'new' and e.cls in (S - 28, S - 29):
            n = u16(d, e.end)
            if 1 <= n <= 64:
                refs = struct.unpack_from('<%dH' % n, d, e.end + 2)
                for r in refs:
                    x = byobj.get(r)
                    c[(S - e.cls, 'feat' if r in fobjs else (x.name if x else None))] += 1
                rows.append((e.offset, e.obj, refs[:6]))
    print(nm, len(rows), c.most_common(12))
    for r in rows[:15]: print('  ', r)
