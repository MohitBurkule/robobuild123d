"""Train whole-object templates on the train half (even positions of the sorted dump parts)."""
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
T = CR.learn_templates(train)
json.dump(T, open(R + 'tools/sldprt/templates_round8.json', 'w'))
print(len(T), sorted(((v['len'], v['train_n'], k) for k, v in T.items()), key=lambda x: -x[0] * x[1])[:20])
