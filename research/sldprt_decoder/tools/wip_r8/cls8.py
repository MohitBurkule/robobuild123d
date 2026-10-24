"""Unexplained bytes per class after the round-8 decoders (42 dump parts)."""
import sys, json
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/')
from common import *
from sldprt import classrec as CR
from collections import Counter
D = load(); tot = Counter(); une = Counter(); cnt = Counter()
for (src, nm), d in sorted(D.items()):
    if src != 'revdev': continue
    dec = FS.decode(d, set())
    ev, _ = ON.numbering(d)
    hs = FS.feature_headers(d)
    recs = CR.decode(d, ev, {h.feature_id for h in hs})
    sp = dec.spans + CR.spans(recs) + [(e.offset, e.end) for e in ev] + [(a, b) for a, b, _ in CR.ps_blobs(d)]
    objs = ON.objects(d, ev, hs)
    for k, (t, u, n) in ON.class_bytes(d, objs, sp).items():
        tot[k] += t; une[k] += u; cnt[k] += n
out = [(k, une[k], tot[k], cnt[k]) for k, _ in une.most_common(25)]
for x in out: print(x)
json.dump(out, open('/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/cls8.json', 'w'), indent=1)
