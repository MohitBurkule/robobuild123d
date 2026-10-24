"""Global class-index assignment: monotone DP matching ClassDefs to frequent tag values by first-object similarity."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from collections import defaultdict
W = 32
def grams(b):
    return {b[i:i + 3] for i in range(len(b) - 2)}
def sim(a, b):
    ga, gb = grams(a), grams(b)
    if not ga or not gb: return 0
    return len(ga & gb) / len(ga | gb)
def candidates(d, S):
    occ = defaultdict(list)
    for m in ON.REF.finditer(d):
        o = m.start(); v = u16(d, o) & 0x7fff
        if v < S or v == 0x7fff: continue
        if ON.in_float(d, o) or ON.is_stamp(d, o): continue
        occ[v].append(o)
    return occ
def assign(d, MINSIM=0.35, verbose=False):
    S = struct.unpack_from('<I', d, 0)[0]
    ev = ON._events(d)
    defs = [(o, o + 6 + a, nm) for o, k, a, nm in ev if k == 0]
    occ = candidates(d, S)
    # per def: list of (v, score)
    cand = []
    for o, e, nm in defs:
        sg = d[e:e + W]
        cs = []
        for v, ps in occ.items():
            ps2 = [p for p in ps if p > e]
            if not ps2: continue
            # require v first plausible occurrence after def? allow earlier noise
            ss = [sim(sg, d[p + 2:p + 2 + W]) for p in ps2[:8]]
            good = sum(1 for s in ss if s >= MINSIM)
            if good: cs.append((v, good * max(ss)))
        cand.append(cs)
    # DP over defs: state = chosen v (or None = keep counting). Track best score with last chosen value.
    # dp list of (lastv, score, path) pruned to best per lastv
    states = {S - 2: (0.0, ())}
    for k, cs in enumerate(cand):
        new = {}
        for lv, (sc, path) in states.items():
            # option none
            key = lv
            if key not in new or new[key][0] < sc: new[key] = (sc, path)
            for v, s in cs:
                if v >= lv + 2:
                    t = (sc + s, path + ((k, v),))
                    if v not in new or new[v][0] < t[0]: new[v] = t
        # prune: keep states not dominated (higher lv with lower score is dominated)
        items = sorted(new.items())
        best = -1; pr = {}
        for lv, t in items:
            if t[0] > best:
                pr[lv] = t; best = t[0]
        states = pr
    sc, path = max(states.values())
    return {defs[k][0]: v for k, v in path}, defs
if __name__ == '__main__':
    D = load()
    import time
    for nm in sys.argv[1:]:
        d = D[('revdev', nm)]
        t = time.time()
        fix, defs = assign(d)
        ev0, _ = ON.numbering(d)
        cur = {e.offset: e.index for e in ev0 if e.kind == 'def'}
        print(nm, time.time() - t)
        for o, e, n in defs:
            print('  ', o, n, cur.get(o), fix.get(o))
