"""Self-consistency: 'unresolved tags' = repeated tag-like words 0x8000|v (v >= S) that name no class
(outside zlib blobs, doubles, timestamps).  With exact numbering every instance tag names a class."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from bisect import bisect_right
def unresolved(d, ev):
    S = struct.unpack_from('<I', d, 0)[0]
    cls = {e.index for e in ev if e.kind == 'def'}
    rep = ON.repeats(d)
    bl = ON.zblobs(d); bs = [a for a, b in bl]
    acc = {e.offset for e in ev}
    from collections import Counter
    top = ev[-1].obj if ev else S
    cands = []
    for o in rep:
        v = u16(d, o)
        if v & 0x8000 and S <= (v & 0x7fff) <= top + 10 and (v & 0x7fff) not in cls and o not in acc:
            cands.append(o)
    ctx = Counter(d[o - 4:o + 4] for o in cands)
    n = 0
    for o in cands:
        if ctx[d[o - 4:o + 4]] >= 20: continue
        v = u16(d, o)
        if not v & 0x8000: continue
        v &= 0x7fff
        if v < S or v == 0x7fff or v in cls or o in acc: continue
        j = bisect_right(bs, o) - 1
        if j >= 0 and o < bl[j][1]: continue
        if ON.in_float(d, o) or ON.is_stamp(d, o): continue
        if v > (ev[-1].obj if ev else S) + 10: continue
        n += 1
    return n
if __name__ == '__main__':
    D = load(); mode = sys.argv[1]
    if mode == 'r7':
        import importlib.util
        sp = importlib.util.spec_from_file_location('sldprt.objnum_r7', '/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/objnum_round7.py')
        R7 = importlib.util.module_from_spec(sp); sp.loader.exec_module(R7)
    tot = 0; clean = 0; per = {}
    for k, d in sorted(D.items()):
        if mode == 'r7':
            ev, _ = R7.numbering(d)
        else:
            ev, _ = ON.numbering(d)
        u = unresolved(d, ev); per[k] = u; tot += u; clean += u == 0
    print(mode, 'unresolved', tot, 'clean files', clean, len(D))
    for k, v in sorted(per.items(), key=lambda x: -x[1])[:10]: print(v, k)
