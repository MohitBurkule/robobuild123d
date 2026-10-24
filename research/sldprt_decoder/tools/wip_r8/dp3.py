import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
import dp2, seedchk
def numbering_dp(d, iters=3):
    S = struct.unpack_from('<I', d, 0)[0]
    ev = ON._events(d)
    base, fix = ON.numbering(d)
    reject = frozenset()
    for _ in range(iters):
        f2, _ = dp2.assign(d, base=base)
        if not f2: break
        fix = {**fix, **f2}
        base = ON.number(d, fix, S, ev, reject)
    return base, fix
if __name__ == '__main__':
    D = load(); ok = n = 0
    for (src, nm), d in sorted(D.items()):
        if src != 'revdev': continue
        cs = seedchk.cases(nm, d, numbering_dp)
        for name, refs, par in cs:
            pis = {p[0] for p in par}
            for r in refs:
                n += 1; ok += r in pis
            print(nm[:20], name, refs, par, flush=True)
    print('exact', ok, n)
