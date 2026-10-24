import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from collections import Counter
D = load()
for (src, nm), d in sorted(D.items()):
    if src != 'revdev': continue
    ev, _ = ON.numbering(d)
    byobj = {e.obj: e for e in ev}
    c = Counter(); miss = 0
    hdr = FS.feature_headers(d); fo = ON.feature_objects(d, hdr, ev)
    dd = Counter()
    for e in ev:
        if e.name == 'moFR_c' and e.end + 6 <= len(d):
            r = u16(d, e.end); fid = struct.unpack_from('<I', d, e.end+2)[0]
            x = byobj.get(r)
            c[x.name or 'ext%d' % x.cls if x else None] += 1
            if fid in fo: dd[(fo[fid][2], r - fo[fid][1])] += 1
    print(nm[:20], len(d), sum(c.values()), c.most_common(4), dd.most_common(3))
