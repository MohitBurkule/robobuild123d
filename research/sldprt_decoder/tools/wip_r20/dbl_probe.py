import sys, os, json, struct, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sldprt import item_sketchplane as ISP, sketch as SK
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
part, name, val = sys.argv[1], sys.argv[2], float(sys.argv[3])
j = json.load(open(f'{ROOT}/decoded/{part}.json')); f, surfs = ISP.load_part(f'{ROOT}/revdev/{part}.SLDPRT')
regs = {r[0]: r for r in SK.sketch_regions(f, [s['name'] for s in j['sketches']])}
_, a, b = regs[name]; print(name, a, b, len(f))
for v in (val, -val):
    pat = struct.pack('<d', v); i = max(0, a - 3000)
    while True:
        i = f.find(pat, i, b + 3000)
        if i < 0: break
        ctx = [struct.unpack_from('<d', f, i + 8 * k)[0] for k in range(-6, 6)]
        print(f'{v:+} @{i} rel {i-a}', np.round(ctx, 5).tolist(), f[i-16:i].hex()); i += 1
