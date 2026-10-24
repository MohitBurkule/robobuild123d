import sys
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import fstream as FS
def api_relations(rels):
    keyf=lambda r:(r.type, tuple(sorted(x[1] for x in r.ents)))
    f0={keyf(r) for r in rels if r.dimension and r.flag==0}
    out, seen = [], set()
    for r in rels:
        if not r.api_visible: continue
        key=keyf(r)
        if r.dimension:
            if key in seen or key not in f0: continue
            seen.add(key)
        out.append(r)
    return out
FS.api_relations=api_relations
sys.argv=sys.argv[:1]
exec(open('/mnt/project-files/robot-cad/research/sldprt/tools/wip_r10/reltest.py').read())
