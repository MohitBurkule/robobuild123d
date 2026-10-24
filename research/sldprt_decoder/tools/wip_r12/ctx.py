import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON
cls = sys.argv[1]
for src in [l.strip() for l in open('files.txt')][:int(sys.argv[2])]:
    d = V.feature_stream(src); ev, _ = ON.numbering(d)
    names = {e.cls: e.name for e in ev if e.kind == 'def'}; acc = {e.offset for e in ev}
    a = [k for k, v in names.items() if v == cls]
    if not a: continue
    k = a[0]; na = nr = 0
    for m in ON.REF.finditer(d):
        p = m.start()
        if ON.u16(d, p) & 0x7fff != k or ON.u16(d, p) == 0xffff: continue
        ok = p in acc
        if (ok and na < 4) or (not ok and nr < 6):
            print(os.path.basename(src)[:20], 'ACC' if ok else 'rej', p, d[p-6:p].hex(), '|', d[p:p+34].hex())
            na += ok; nr += not ok
