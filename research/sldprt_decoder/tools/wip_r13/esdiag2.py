import sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS, answer_key as AK
SRC, DU = sys.argv[1], sys.argv[2]
def run():
    r = {}
    for dp in sorted(glob.glob(DU + '/*.dump.txt')):
        n = os.path.basename(dp)[:-9]; src = os.path.join(SRC, n + '.SLDPRT')
        if not os.path.exists(src): continue
        d = V.feature_stream(src)
        if d is None: continue
        D = AK.parse(dp); ex = {f.id: f for f in D.top() if f.extrude}
        if not ex: continue
        dec = FS.decode(d, set(ex))
        for fid, f in ex.items():
            x = f.extrude; es = dec.endspecs.get(fid)
            r[(n, fid)] = (bool(es and es.both == x['both']), (x['end1'], x['end2'], x['both']), es and (es.end1, es.end2, es.both, es.dir1))
    return r
for flag in sys.argv[3:]:
    a = run(); setattr(FS, flag, {'ES_TAG_MAX':1<<16,'ES_TAG_MIN':0}.get(flag, False)); b = run()
    print(flag, 'on', sum(v[0] for v in a.values()), 'off', sum(v[0] for v in b.values()))
    for k in a:
        if a[k][0] != b[k][0]: print('  ', k, 'on', a[k], 'off', b[k][2])
    setattr(FS, flag, {'ES_TAG_MAX':0x3000,'ES_TAG_MIN':0x10}.get(flag, True))
