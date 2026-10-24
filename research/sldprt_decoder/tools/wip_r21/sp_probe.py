import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sldprt import item_sketchplane as ISP, sketch as SK
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
part, names = sys.argv[1], sys.argv[2:]
j = json.load(open(f'{ROOT}/decoded/{part}.json')); f, surfs = ISP.load_part(f'{ROOT}/revdev/{part}.SLDPRT')
regs = {r[0]: r for r in SK.sketch_regions(f, [s['name'] for s in j['sketches']])}
for n in names:
    _, a, b = regs[n]; print(n, a, b)
    for o, T in SK._orth_blocks(f, max(0, a - 1600), b):
        print('  ', o, o - a, ISP.classify(f, o), np.round(T, 4).tolist(), f[o-12:o].hex())
allb = SK._orth_blocks(f, 0, len(f))
print('all blocks', len(allb))
for o, T in allb:
    if any(abs(abs(x) - float(sys.argv[-1] if False else 0.017)) < 1e-9 for x in T[9:12]): print(' t=17', o, ISP.classify(f, o), np.round(T, 4).tolist(), [r[0] for r in regs.values() if r[1]-1600 <= o <= r[2]])
