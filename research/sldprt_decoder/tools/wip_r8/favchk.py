import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from sldprt import answer_key as AK
from collections import Counter
import os
DUMPS = '/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
D = load()
c = Counter()
for (src, nm), d in sorted(D.items()):
    if src != 'revdev' or not os.path.exists(DUMPS + nm + '.dump.txt'): continue
    A = AK.parse(DUMPS + nm + '.dump.txt')
    vals = set()
    for f in A.top():
        for full, v in f.dims: vals.add(round(abs(v), 9))
    ev, _ = ON.numbering(d)
    for e in ev:
        if e.name in ('moFavoriteHandle_c', 'moSkDimHandleValG2_c', 'moDisplayDistanceDim_c', 'moDisplayRadialDim_c', 'moDisplayAngularDim_c'):
            for off in range(2, 64, 1):
                if e.offset + off + 8 > len(d): break
                x = struct.unpack_from('<d', d, e.offset + off)[0]
                if 1e-6 < abs(x) < 100:
                    c[(e.name, e.kind, off, round(abs(x), 9) in vals)] += 1
for k in sorted(c):
    if c[k] > 20 and k[3]: print(k, c[k], c[(k[0], k[1], k[2], False)])
