exec(open('g.py').read())
from collections import Counter, defaultdict
def class_deltas(d, S=None, K=6, W=40, log=None):
    """For each class def (offset, our idx, name): Counter of deltas v-our over later tags 0x8000|v whose next K bytes equal the def's first-object bytes."""
    S = S or struct.unpack_from('<I', d, 0)[0]
    log = log or run(d, S, len(d))
    defs = [(o, c, n) for o, c, n, k in log if k == 'def']
    out = []
    cset = {c for _, c, _ in defs}
    for o, c, n in defs:
        e = o + 6 + len(n); sig = d[e:e + K]
        if sig.count(0) >= K - 1: out.append((o, c, n, None)); continue
        cnt = Counter()
        j = d.find(sig, e + K)
        while j >= 0:
            v = struct.unpack_from('<H', d, j - 2)[0]
            if v & 0x8000 and abs((v & 0x7fff) - c) <= W and ((v & 0x7fff) == c or (v & 0x7fff) not in cset or (v & 0x7fff) < S): cnt[(v & 0x7fff) - c] += 1
            j = d.find(sig, j + 1)
        out.append((o, c, n, cnt))
    return out
def sync(d, maxit=60, K=6):
    S = struct.unpack_from('<I', d, 0)[0]; fix = {}
    for it in range(maxit):
        log = run(d, S, len(d), fix)
        cd = class_deltas(d, S, K, log=log)
        ch = None
        for o, c, n, cnt in cd:
            if not cnt: continue
            dl, k = cnt.most_common(1)[0]
            if dl != 0 and k >= 2 and k >= 2 * cnt.get(0, 0) and o not in fix:
                ch = (o, c + dl); break
        if not ch: return log, fix, cd
        fix[ch[0]] = ch[1]
    return log, fix, cd
