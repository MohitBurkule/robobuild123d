"""Round 9: meanings of template slots by correlation with dump values (dims, sketch point coords, face data)."""
import sys, os, glob, json, re, struct
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, objnum as ON, classrec as CR, answer_key as AK
from collections import Counter, defaultdict
R = '/mnt/project-files/robot-cad/research/sldprt/'
tm = V._templates()
TOP = ['moDisplayDistanceDim_c', 'moSkDimHandleValG2_c', 'moDisplayRadialDim_c', 'moDisplayAngularDim_c',
       'moFeatureDimHandle_c', 'moSkDimHandleRadial_c', 'moRefPlane_c', 'moDefaultRefPlnData_c', 'moEdgeRef_c', 'sgSketch']
NUM = re.compile(r'-?\d+\.?\d*(?:E-?\d+)?')
stat = defaultdict(Counter)
for p in sorted(glob.glob(R + 'dumps_v2/*.dump.txt')):
    n = os.path.basename(p)[:-9]
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT')
    if d is None: continue
    A = AK.parse(p)
    dims = {round(abs(v), 9) for f in A.top() for _, v in f.dims}
    txt = open(p, errors='replace').read()
    pts = set()
    for line in txt.splitlines():
        if line.strip().startswith(('PT ', 'SEG ')):
            for x in NUM.findall(line.split(' ', 2)[2] if line.count(' ') > 2 else ''):
                try: pts.add(round(abs(float(x)), 9))
                except ValueError: pass
    ev, _ = ON.numbering(d)
    for r in CR.decode_templates(d, ev, {k: tm[k] for k in TOP if k in tm}):
        t = tm[r.cls]
        for i in range(0, t['len'] - 7):
            if all(t['const'][i + j] is not None for j in range(8)): continue
            x = struct.unpack_from('<d', d, r.start + i)[0]
            if not (1e-7 < abs(x) < 1e3): continue
            k = round(abs(x), 9)
            stat[(r.cls, i)]['n'] += 1
            stat[(r.cls, i)]['dim'] += k in dims
            stat[(r.cls, i)]['pt'] += k in pts and k not in dims
out = {}
for (c, i), s in sorted(stat.items()):
    if s['n'] >= 20 and (s['dim'] + s['pt']) / s['n'] >= 0.5:
        out.setdefault(c, []).append((i, s['n'], round(s['dim'] / s['n'], 3), round(s['pt'] / s['n'], 3)))
json.dump(out, open(R + 'tools/wip_r8/template_meanings_round9.json', 'w'), indent=1)
for c, v in out.items(): print(c, v[:12])
