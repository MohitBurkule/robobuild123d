"""List accepted events and rejected tag-like candidates in [a, b) of a part."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
D = load(); nm, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = D[('revdev', nm)] if ('revdev', nm) in D else D[('corpus', nm)]
ev, fix = ON.numbering(d)
S = struct.unpack_from('<I', d, 0)[0]
classes = {e.index: e.name for e in ev if e.kind == 'def'}
acc = {e.offset: e for e in ev}
for o in range(a, b - 1):
    if o in acc:
        e = acc[o]; print('%7d ACC %-4s obj=%5d cls=%4d %-28s %s' % (o, e.kind, e.obj, e.cls, e.name or 'ext[S-%d]' % (S - e.cls), d[e.end:e.end + 16].hex()))
    elif d[o + 1] >= 0x80 and d[o] | d[o + 1] << 8 != 0xffff:
        v = u16(d, o) & 0x7fff
        if v in classes or 0 < v < S:
            print('%7d rej      v=%4d %-28s f=%d s=%d %s' % (o, v, classes.get(v, 'ext[S-%d]' % (S - v)), ON.in_float(d, o), ON.is_stamp(d, o), d[o - 4:o + 14].hex()))
