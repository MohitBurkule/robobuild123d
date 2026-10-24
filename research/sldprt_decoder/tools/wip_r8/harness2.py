"""Round-8 numbering evaluation: seed refs (truth) + residual (self-consistency) on all files."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
import seedchk, json, time
def run(corpus=True, names=None):
    D = load(); ok = n = 0; drift = []; per = {}
    for (src, nm), d in sorted(D.items()):
        if src == 'corpus' and not corpus: continue
        if names and nm not in names: continue
        if src == 'revdev':
            for name, refs, par in seedchk.cases(nm, d):
                pis = [p[0] for p in par]
                for r in refs:
                    n += 1; ok += r in pis
                    drift.append((nm[:12], name, min((r - p for p in pis), key=abs) if pis else None))
        else:
            ON.numbering(d)
        per[(src, nm)] = ON.numbering.residual
    vals = list(per.values())
    return dict(seed_exact=ok, seed_n=n, residual=sum(vals), clean=sum(v == 0 for v in vals), files=len(vals),
                drift=[x[2] for x in drift]), per, drift
if __name__ == '__main__':
    t = time.time()
    r, per, drift = run(corpus='-c' in sys.argv)
    print(json.dumps(r), round(time.time() - t))
    if '-v' in sys.argv:
        for x in drift: print(x)
        for k, v in sorted(per.items(), key=lambda x: -x[1])[:15]: print(v, k)
