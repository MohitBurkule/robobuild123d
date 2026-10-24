import sys, os, struct
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
n, MAXSPAN = sys.argv[1], int(sys.argv[2])
src = R + ('revdev/' if os.path.exists(R + 'revdev/' + n + '.SLDPRT') else 'corpus/') + n + '.SLDPRT'
d = V.feature_stream(src); ev, fix = ON.numbering(d)
S = struct.unpack_from('<I', d, 0)[0]
acc = {e.offset: e for e in ev}; names = {e.cls: e.name for e in ev if e.kind == 'def'}
allr = ON.numbering.residuals
for k, (o, r) in enumerate(allr):
    lo = allr[k - 1][0] if k else 0
    if r == 0 or o - lo > MAXSPAN: continue
    print('interval', lo, o, 'delta', r)
    for m in ON.REF.finditer(d, lo, o):
        p = m.start(); v = ON.u16(d, p)
        if p in acc or v == 0xffff: continue
        a = v & 0x7fff
        if a not in names: continue
        why = 'float' if ON.in_float(d, p) else 'stamp' if ON.is_stamp(d, p) else 'rej' if p in ON._numbering7.reject else 'other'
        prv = max((x for x in acc if x < p), default=0)
        print('   ', p, names[a], why, 'prevacc', prv, acc[prv].name or acc[prv].cls if prv in acc else '', d[p-8:p].hex(), '|', d[p:p+16].hex())
