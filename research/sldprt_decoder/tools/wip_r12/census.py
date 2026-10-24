import sys, os, struct, glob
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON
import importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) > 2: importlib.import_module(sys.argv[2])
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
POS, NEG = Counter(), Counter()
files = [l.strip() for l in open(sys.argv[1])]
for src in files:
    d = V.feature_stream(src)
    if d is None: continue
    ev, fix = ON.numbering(d)
    S = struct.unpack_from('<I', d, 0)[0]
    acc = {e.offset: e for e in ev}; names = {e.cls: e.name for e in ev if e.kind == 'def'}
    allr = ON.numbering.residuals
    for k, (o, r) in enumerate(allr):
        lo = allr[k - 1][0] if k else 0
        if r == 0 or o - lo > 30000: continue
        if r > 0:
            for m in ON.REF.finditer(d, lo, o):
                p = m.start(); v = ON.u16(d, p)
                if p in acc or v == 0xffff or (v & 0x7fff) not in names: continue
                why = 'float' if ON.in_float(d, p) else 'stamp' if ON.is_stamp(d, p) else 'rej' if p in ON._numbering7.reject else 'other'
                POS[(names[v & 0x7fff], why)] += 1
        else:
            for e in ev:
                if lo <= e.offset < o and e.kind == 'new': NEG[e.name or 'ext'] += 1
    print(os.path.basename(src), ON.numbering.residual, flush=True)
print('POS', POS.most_common(30)); print('NEG', NEG.most_common(20))
