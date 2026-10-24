"""Round 14: looser string-aware templates keyed by absolute ext class index, trained on the
train halves (even positions, as validate.run splits) of dumps_v2, corpus and dumps_ab."""
import sys, json, glob, os
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, objnum as ON, classrec as CR
R = '/mnt/project-files/robot-cad/research/sldprt/'
train = []
for src, dumps in (('revdev', 'dumps_v2'), ('corpus', 'dumps_corpus'), ('dumps_ab', 'dumps_ab')):
    names = sorted(os.path.basename(p)[:-9] for p in glob.glob(R + dumps + '/*.dump.txt'))
    data = []
    for n in names:
        f = R + src + '/' + n + '.SLDPRT'
        d = V.feature_stream(f) if os.path.exists(f) else None
        if d is not None: data.append(d)
    for k, d in enumerate(data):
        if k % 2 == 0:
            ev, _ = ON.numbering(d); train.append((d, ev))
T = CR.learn_templates2(train, min_n=int(sys.argv[1]) if len(sys.argv) > 1 else 2, const_share=float(sys.argv[2]) if len(sys.argv) > 2 else 0.9, min_const=float(sys.argv[3]) if len(sys.argv) > 3 else 0.4, ext_abs=True)
json.dump(T, open(R + 'tools/sldprt/templates_round14.json', 'w'))
print(len(train), len(T), sum(len(v) for v in T.values()))
