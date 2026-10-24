import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
D = load(); nm = sys.argv[1]
d = D[('revdev', nm)]
ev, _ = ON.numbering(d)
byobj = {e.obj: e for e in ev}
n = sum(e.name == 'moExtObject_c' for e in ev); print('ext objs', n, 'events', len(ev))
k = 0
for e in ev:
    if e.name == 'moFR_c':
        r = u16(d, e.end); x = byobj.get(r)
        print(e.obj, d[e.end:e.end+14].hex(), '->', r, x and x.name, x and d[x.end:x.end+40].hex())
        k += 1
        if k > 12: break
