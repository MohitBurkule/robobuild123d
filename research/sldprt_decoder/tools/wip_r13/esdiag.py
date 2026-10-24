import sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS, answer_key as AK
D0 = sys.argv[1]
for dp in sorted(glob.glob(D0 + '/*.dump.txt')):
    n = os.path.basename(dp)[:-9]; src = os.path.join(D0, n + '.SLDPRT')
    if not os.path.exists(src): continue
    d = V.feature_stream(src)
    if d is None: continue
    D = AK.parse(dp); ex = {f.id: f for f in D.top() if f.extrude}
    if not ex: continue
    dec = FS.decode(d, set(ex))
    for fid, f in ex.items():
        x = f.extrude; es = dec.endspecs.get(fid)
        ok = es and es.end1 == x['end1'] and es.end2 == x['end2'] and es.both == x['both']
        if not ok:
            print(n[:40], f.type, f.name, 'want', x['end1'], x['end2'], x['both'], 'got', es and (es.end1, es.end2, es.both, es.offset), es and d[es.offset:es.offset+40].hex())
