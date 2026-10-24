"""Per ClassDef: votes for the class's true index from later instance tags with the same first-object bytes."""
import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from collections import Counter
def votes(d, ev, K=4, W=2000):
    S = struct.unpack_from('<I', d, 0)[0]
    defs = [e for e in ev if e.kind == 'def']
    idx = {e.index for e in defs}
    out = []
    for e in defs:
        sig = d[e.end:e.end + K]
        c = Counter()
        if len(set(sig)) >= 3:
            j = d.find(sig, e.end + 1)
            while j >= 0:
                v = u16(d, j - 2)
                if v & 0x8000 and abs((v & 0x7fff) - e.index) <= W:
                    c[(v & 0x7fff) - e.index] += 1
                j = d.find(sig, j + 1)
        out.append((e, c))
    return out
if __name__ == '__main__':
    D = load()
    d = D[('revdev', sys.argv[1])]
    ev, fix = ON.numbering(d)
    for e, c in votes(d, ev):
        print(e.offset, e.index, e.name, c.most_common(3))
