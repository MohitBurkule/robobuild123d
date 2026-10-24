"""Round 12: T-series byte diffs. Pairs feature streams of two SLDPRTs, aligns with SequenceMatcher,
labels each changed run (timestamp / guid / f64 value / name / flag / other) and the owning object class."""
import sys, os, struct, bisect, difflib
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, streams as ST
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dumps_v3/')
A = R + 'swtests/swtests/'; B = R + 'revdev/swtests/'

def is_stamp(v): return 1_400_000_000 < v < 1_900_000_000

def label(a, b, d_a, ia):
    """a,b replaced byte strings (same length), ia = offset in stream a."""
    n = len(a)
    # widen to 4/8 aligned window around the change in a
    for w, lo in ((4, 3), (8, 7)):
        pass
    if n == 16: return 'guid'
    for o in range(max(4, ia - 3), ia + 1):
        if o + 4 >= ia + n and 0x01D00000 <= struct.unpack_from('<I', d_a, o - 4)[0] < 0x01E00000:
            return 'filetime'   # (hi, lo) FILETIME: hi dword unchanged, lo dword differs
        if 0x01D00000 <= struct.unpack_from('<I', d_a, o)[0] < 0x01E00000 and o + 8 >= ia + n:
            return 'filetime'
    s = max(0, ia - 3)
    for o in range(s, ia + 1):
        if o + 4 <= len(d_a) and o + 4 >= ia + n:
            v = struct.unpack_from('<I', d_a, o)[0]
            if is_stamp(v): return 'timestamp'
    s = max(0, ia - 7)
    for o in range(s, ia + 1):
        if o + 8 <= len(d_a) and o + 8 >= ia + n:
            f = struct.unpack_from('<d', d_a, o)[0]
            if 1e-6 < abs(f) < 1e4: return 'f64'
    if all(32 <= c < 127 or c == 0 for c in a + b) and any(32 < c < 127 for c in a + b): return 'name'
    if n <= 2: return 'flag'
    return 'other'

def owner(d, ev):
    offs = [e.offset for e in ev if e.kind in ('new', 'def')]
    nm = {}
    cls = {e.offset: e for e in ev if e.kind in ('new', 'def')}
    names = {e.cls: e.name for e in ev if e.kind == 'def'}
    def f(o):
        k = bisect.bisect_right(offs, o) - 1
        if k < 0: return '-'
        e = cls[offs[k]]
        return getattr(e, 'name', None) or names.get(getattr(e, 'cls', None)) or '?'
    return f

def diff(pa, pb, verbose=False):
    da, db = V.feature_stream(pa), V.feature_stream(pb)
    ev, _ = ON.numbering(da); own = owner(da, ev)
    sm = difflib.SequenceMatcher(None, da, db, autojunk=False)
    L = Counter(); C = Counter(); rows = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        if op == 'replace' and i2 - i1 == j2 - j1:
            lab = label(da[i1:i2], db[j1:j2], da, i1)
        else:
            lab = op + ('_name' if all(32 <= c < 127 or c == 0 for c in da[i1:i2] + db[j1:j2]) else '')
        L[lab] += 1; C[(own(i1), lab)] += 1
        rows.append((i1, lab, own(i1), da[i1:i2][:24].hex(), db[j1:j2][:24].hex()))
    return len(da), len(db), L, C, rows

if __name__ == '__main__':
    pairs = [('ident', A + t, B + t) for t in sorted(os.listdir(A)) if t.endswith('.SLDPRT')] if sys.argv[1:] == ['ident'] else \
            [(x, *x.split('|')) if '|' in x else (x, A + x.split(':')[0] + '.SLDPRT', A + x.split(':')[1] + '.SLDPRT') for x in sys.argv[1:]]
    tot = Counter()
    for tag, pa, pb in pairs:
        if not os.path.exists(pb): continue
        na, nb, L, C, rows = diff(pa, pb)
        print('==', tag, os.path.basename(pa), os.path.basename(pb), na, nb, dict(L))
        for k, v in C.most_common(25): print('   ', k, v)
        for r in rows[:60]: print('     ', r)
        for k, v in C.items(): tot[k] += v
    print('TOTAL', tot.most_common(40))
