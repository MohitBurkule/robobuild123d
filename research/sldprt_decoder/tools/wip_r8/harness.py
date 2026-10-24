"""Evaluate a numbering variant: pattern seed refs (dump truth) + corpus self-consistency (objects the
counter could not account for = total size of the DP class-index jumps)."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
import dp2, seedchk, json
def numbering_dp(d, iters=3):
    S = struct.unpack_from('<I', d, 0)[0]
    ev = ON._events(d)
    base, fix = ON.numbering(d)
    jumps = 0
    for _ in range(iters):
        f2, defs = dp2.assign(d, base=base)
        cur = {e.offset: e.index for e in defs}
        f2 = {o: v for o, v in f2.items() if cur.get(o) != v}
        if not f2: break
        jumps += sum(abs(v - cur[o]) for o, v in f2.items())
        fix = {**fix, **f2}
        base = ON.number(d, fix, S, ev)
    numbering_dp.jumps = jumps
    return base, fix
def run(only=None, corpus=True):
    D = load(); ok = n = 0; drift = []; jt = 0; per = {}
    for (src, nm), d in sorted(D.items()):
        if src == 'corpus' and not corpus: continue
        if only and nm not in only: continue
        if src == 'revdev':
            for name, refs, par in seedchk.cases(nm, d, numbering_dp):
                pis = [p[0] for p in par]
                for r in refs:
                    n += 1; ok += r in pis
                    drift.append(min(abs(r - p) for p in pis) if pis else None)
        else:
            numbering_dp(d)
        per[nm] = numbering_dp.jumps; jt += numbering_dp.jumps
    return dict(seed_exact=ok, seed_n=n, drift=drift, jumps=jt, clean=sum(v == 0 for v in per.values()), files=len(per)), per
if __name__ == '__main__':
    r, per = run(corpus='-c' in sys.argv)
    print(json.dumps(r))
