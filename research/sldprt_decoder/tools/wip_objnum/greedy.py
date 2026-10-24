import sys, pickle, struct
sys.path.insert(0, '.')
from sldprt import fstream as FS
D = pickle.load(open(sys.argv[1], 'rb'))

def run(d, start=1):
    defs = {m.start(): (m.group(2)[0], m.group(2)[:m.group(1)[0]].decode()) for m in FS.CLASSDEF.finditer(d)}
    cnt = start; classes = {}; i = 0; log = []
    while i < len(d) - 1:
        if i in defs:
            ln, nm = defs[i]
            classes[cnt] = nm; log.append((i, cnt, nm, 'def')); cnt += 2; i += 6 + ln; continue
        v = struct.unpack_from('<H', d, i)[0]
        if v & 0x8000 and (v & 0x7fff) in classes:
            log.append((i, cnt, classes[v & 0x7fff], 'ref')); cnt += 1; i += 2; continue
        i += 1
    return log
for n in list(D)[:6]:
    d = D[n]; tm = FS.tag_map(d)
    log = run(d)
    idx = {nm: c for (_, c, nm, k) in log if k == 'def'}
    print(n, [(t & 0x7fff, idx.get(c)) for t, c in tm.items()], len(log))
