exec(open('ev1.py').read().split('if __name__')[0])
def seed_list(d, h, S):
    best = None
    for k in (28, 29):
        t = struct.pack('<H', 0x8000 | (S - k)); j = d.find(t, h.offset, h.region_end)
        while j >= 0:
            n = struct.unpack_from('<H', d, j + 2)[0]
            if 1 <= n <= 32:
                refs = list(struct.unpack_from('<%dH' % n, d, j + 4))
                if all(0 < r < 0x7fff for r in refs):
                    if best is None or j < best[0]: best = (j, refs)
                    break
            j = d.find(t, j + 1, h.region_end)
    return best[1] if best else []
def resolve(refs, fo, before, tol):
    cand = [(i, fid) for fid, (h, i) in fo.items() if h.offset < before and i is not None]
    out = []
    for r in refs:
        i, fid = min(cand, key=lambda x: abs(x[0] - r))
        out.append(fid if abs(i - r) <= tol else None)
    return out
def seeds(nm, tol=0, **kw):
    d = D[nm]; p = DUMPS + nm + '.dump.txt'
    if not os.path.exists(p): return []
    top = AK.parse(p).top(); ids = {x.name: x.id for x in top}
    pats = [f for f in top if f.type in ('MirrorPattern', 'CirPattern', 'LPattern')]
    if not pats: return []
    ev, fix = ON.numbering(d, **kw); fo = feat_obj(d, ev); S = struct.unpack_from('<I', d, 0)[0]
    res = []
    for f in pats:
        if f.id not in fo: continue
        h = fo[f.id][0]
        refs = seed_list(d, h, S)
        got = resolve(refs, fo, h.offset, tol)
        exp = [ids[pn] for pn, pt in f.parents if pt != 'RefPlane' and pn in ids]
        res.append((f.name, exp, got, refs, [fo[x][1] for x in exp if x in fo]))
    return res
if __name__ == '__main__':
    names = sorted(D)
    for tol in (0, 3, 10, 30, 100000):
        tot = {0: [0, 0], 1: [0, 0]}
        for k, nm in enumerate(names):
            for name, exp, got, refs, ours in seeds(nm, tol):
                g = set(x for x in got if x)
                # seeds = parents that the list names; truth: every listed seed must be a parent, and list non-empty
                ok = bool(g) and g <= set(exp) and len(g) == len(refs)
                tot[k % 2][0] += ok; tot[k % 2][1] += 1
                if tol == -1: print(k % 2, nm[:16], name, ok, refs, ours)
        print('tol', tol, 'train', tot[0], 'val', tot[1])
