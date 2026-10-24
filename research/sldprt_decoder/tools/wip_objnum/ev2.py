exec(open('ev1.py').read().split('if __name__')[0])
from collections import Counter
def parent_hits(nm, shift=0, prune=True, per=None):
    d = D[nm]; p = DUMPS + nm + '.dump.txt'
    if not os.path.exists(p): return Counter()
    ev, fix = ON.numbering(d, prune=prune)
    fo = feat_obj(d, ev)
    top = AK.parse(p).top(); ids = {x.name: x.id for x in top}
    c = Counter()
    for f in top:
        if f.id not in fo: continue
        h = fo[f.id][0]
        reg = d[h.offset:h.region_end]
        for pn, pt in f.parents:
            if ids.get(pn) not in fo: continue
            t = fo[ids[pn]][1] + shift
            ok = struct.pack('<H', t) in reg
            c[(pt if per else 'all', ok)] += 1
    return c
if __name__ == '__main__':
    tot = Counter(); ctl = Counter()
    for nm in D:
        a = parent_hits(nm); b = parent_hits(nm, 7)
        tot += a; ctl += b
        n = a[('all', True)] + a[('all', False)]
        if n: print(nm[:24], a[('all', True)], n, 'ctl', b[('all', True)])
    print(tot, ctl)
