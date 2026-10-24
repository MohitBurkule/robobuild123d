"""Class-index assignment by beam DP: ClassDef k gets index t_k; t_k - t_{k-1} defaults to our counted delta,
or jumps to a candidate tag value whose instances resemble the def's first object (penalised by jump size)."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from dp1 import sim, candidates
from bisect import bisect_left, bisect_right
W = 32
def assign(d, MINSIM=0.35, LAM=0.15, BEAM=60, base=None):
    S = struct.unpack_from('<I', d, 0)[0]
    base = base if base is not None else ON.numbering(d)[0]
    defs = [e for e in base if e.kind == 'def']
    occ = candidates(d, S)
    allpos = sorted(p for ps in occ.values() for p in ps)
    by2 = {}
    for v, ps in occ.items():
        if len(ps) < 2: continue
        for p in ps:
            by2.setdefault(d[p + 2:p + 4], []).append((p, v))
    gcache = {}
    def g(p):
        x = gcache.get(p)
        if x is None:
            b = d[p:p + W]; x = gcache[p] = {b[i:i + 3] for i in range(len(b) - 2)}
        return x
    cand = []
    for e in defs:
        ge = g(e.end)
        per = {}
        for p, v in by2.get(d[e.end:e.end + 2], ()):
            if p <= e.end: continue
            l = per.setdefault(v, [])
            if len(l) < 8: l.append(p)
        cs = []
        for v, ps2 in per.items():
            ss = []
            for p in ps2:
                gp = g(p + 2); u = len(ge | gp)
                ss.append(len(ge & gp) / u if u else 0)
            good = sum(1 for s in ss if s >= MINSIM)
            if good: cs.append((v, min(good, 4) * max(ss)))
        cs.sort(key=lambda x: -x[1])
        cand.append(cs[:40])
    states = {defs[0].index: (0.0, ())}
    for k, e in enumerate(defs):
        dc = e.index - defs[k - 1].index if k else 0
        ub = bisect_left(allpos, e.offset) - bisect_left(allpos, defs[k - 1].offset) if k else 0
        new = {}
        def put(v, t):
            if v not in new or new[v][0] < t[0]: new[v] = t
        for lv, (sc, path) in states.items():
            pred = lv + dc
            base_s = dict(cand[k]).get(pred, 0)
            put(pred, (sc + base_s, path))
            for v, s in cand[k]:
                if v == pred or v < lv + 2 or (k and v > lv + 2 + ub + dc): continue
                put(v, (sc + s - LAM * abs(v - pred) ** 0.5 - 1.0, path + ((k, v),)))
        states = dict(sorted(new.items(), key=lambda x: -x[1][0])[:BEAM])
    sc, path = max(states.values())
    return {defs[k].offset: v for k, v in path}, defs
if __name__ == '__main__':
    D = load()
    for nm in sys.argv[1:]:
        d = D[('revdev', nm)]
        fix, defs = assign(d)
        print(nm, len(fix))
        for e in defs:
            if e.offset in fix: print('  ', e.offset, e.name, e.index, '->', fix[e.offset])
