"""Pattern seed object refs vs. the object index our numbering gives the true seed feature."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from sldprt import answer_key as AK
import os
DUMPS = '/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
PT = ('MirrorPattern', 'CirPattern', 'LPattern', 'LocalCirPattern', 'LocalLPattern', 'MirrorSolid')
def cases(nm, d, numbering=None):
    p = DUMPS + nm + '.dump.txt'
    if not os.path.exists(p): return []
    top = AK.parse(p).top(); ids = {x.name: x.id for x in top}
    ev, _ = (numbering or ON.numbering)(d)
    hdr = FS.feature_headers(d); fo = ON.feature_objects(d, hdr, ev)
    hidx = {}
    for h in hdr: hidx.setdefault(h.feature_id, h)
    out = []
    for f in top:
        if f.type not in PT or f.id not in hidx: continue
        h = hidx[f.id]
        refs = ON.seed_list(d, h)
        par = [fo[ids[pn]] for pn, pt in f.parents if pt != 'RefPlane' and ids.get(pn) in fo]
        out.append((f.name, refs, [(x[1], x[2], x[0].offset) for x in par]))
    return out
if __name__ == '__main__':
    D = load()
    ok = n = 0
    for (src, nm), d in sorted(D.items()):
        if src != 'revdev': continue
        for name, refs, par in cases(nm, d):
            pis = {p[0] for p in par}
            for r in refs:
                n += 1; ok += r in pis
            print(nm[:20], name, refs, par)
    print('exact', ok, n)
