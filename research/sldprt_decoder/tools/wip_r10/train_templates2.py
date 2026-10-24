"""Train round-10 string-aware templates on the train half (even positions)."""
import sys, json, glob, os
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, objnum as ON, classrec as CR
R = '/mnt/project-files/robot-cad/research/sldprt/'
names = sorted(os.path.basename(p)[:-9] for p in glob.glob(R + 'dumps_v2/*.dump.txt'))
train = []
for k, n in enumerate(names):
    if k % 2: continue
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT')
    ev, _ = ON.numbering(d)
    train.append((d, ev))
T = CR.learn_templates2(train, min_n=int(sys.argv[1]) if len(sys.argv) > 1 else 4)
json.dump(T, open(R + 'tools/sldprt/templates_round10.json', 'w'))
print(len(T), sum(len(v) for v in T.values()))
