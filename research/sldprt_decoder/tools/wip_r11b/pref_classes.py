"""Round 11b: class bodies inside DumpV3 pref archives (self-contained CArchive, numbering from 1)."""
import sys, os, glob, re, struct
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
L = defaultdict(Counter); ex = {}
for p in sorted(glob.glob(R + 'dumps_v3/*.refs.txt'))[:int(sys.argv[1])]:
    for ln in open(p, encoding='latin-1'):
        m = re.search(r'pref=([0-9A-F]+)', ln)
        if not m: continue
        b = bytes.fromhex(m.group(1))
        if len(b) <= 16: continue
        a = b[16:]
        ev = ON.number(a, start=1, ev=ON._events(a))
        for e, x, y in CR._obj_spans(a, ev):
            nm = e.name or '?%d' % e.cls
            L[nm][y - x] += 1
            ex.setdefault((nm, y - x), a[x:y][:64].hex())
for k, c in sorted(L.items(), key=lambda kv: -sum(kv[1].values())):
    print(k, sum(c.values()), c.most_common(5))
    for ln, _ in c.most_common(2): print('    ', ln, ex[(k, ln)])
