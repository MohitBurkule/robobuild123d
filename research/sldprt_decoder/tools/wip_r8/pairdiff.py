"""Pair diff of two feature streams: align object sequences by class, then list changed fields
inside matched objects (8-byte doubles where both sides decode to plausible values)."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
import difflib
from collections import Counter
def objs(d):
    ev, _ = ON.numbering(d)
    return ON.objects(d, ev, FS.feature_headers(d))
def fdiff(a, b):
    """changed byte runs between equal-length object bodies -> list of (off, old, new)"""
    out = []; i = 0; n = min(len(a), len(b))
    while i < n:
        if a[i] != b[i]:
            j = i
            while j < n and a[j] != b[j]: j += 1
            out.append((i, a[i:j], b[j - (j - i):j] if False else b[i:j])); i = j
        else: i += 1
    return out
def as_doubles(body_a, body_b, off, ln):
    """the 8-byte-aligned (relative to some start) double windows covering the change"""
    res = []
    for s in range(max(0, off - 7), off + 1):
        if s + 8 > len(body_a) or s + 8 > len(body_b) or s + 8 < off + ln: continue
        x = struct.unpack_from('<d', body_a, s)[0]; y = struct.unpack_from('<d', body_b, s)[0]
        if 1e-7 < abs(x) < 1e4 and 1e-7 < abs(y) < 1e4:
            res.append((s, x, y))
    return res
def run(A, B, vals=()):
    D = load()
    da, db = D[('revdev', A)], D[('revdev', B)]
    oa, ob = objs(da), objs(db)
    sa = [o.name for o in oa]; sb = [o.name for o in ob]
    sm = difflib.SequenceMatcher(None, sa, sb, autojunk=False)
    rep = {'objects': (len(oa), len(ob)), 'opcodes': [], 'changed': []}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            rep['opcodes'].append((tag, i1, i2, j1, j2, sa[i1:i2][:6], sb[j1:j2][:6]))
            continue
        for k in range(i2 - i1):
            x, y = oa[i1 + k], ob[j1 + k]
            ba, bb = da[x.start:x.end], db[y.start:y.end]
            if ba == bb: continue
            ch = fdiff(ba, bb) if len(ba) == len(bb) else [('len', len(ba), len(bb))]
            dbl = []
            for c in ch:
                if c[0] != 'len':
                    dbl += as_doubles(ba, bb, c[0], len(c[1]))
            rep['changed'].append(dict(cls=x.name, obj=(x.index, y.index), off=(x.start, y.start), size=(len(ba), len(bb)),
                                       nchg=len(ch), runs=[(c[0], c[1].hex() if isinstance(c[1], bytes) else c[1], c[2].hex() if isinstance(c[2], bytes) else c[2]) for c in ch[:6]],
                                       doubles=[(s, x_, y_) for s, x_, y_ in dbl if any(abs(abs(y_) - v) < 1e-9 or abs(abs(x_) - v) < 1e-9 for v in vals)] if vals else dbl[:6]))
    return rep
if __name__ == '__main__':
    import json
    A, B = sys.argv[1], sys.argv[2]
    r = run(A, B)
    print('objects', r['objects'], 'non-equal opcodes', len(r['opcodes']), 'changed objects', len(r['changed']))
    for o in r['opcodes'][:20]: print('  OP', o)
    cc = Counter(c['cls'] for c in r['changed'])
    print('changed by class', cc.most_common(20))
    out = sys.argv[3] if len(sys.argv) > 3 else None
    if out: json.dump(r, open(out, 'w'), indent=1, default=str)
