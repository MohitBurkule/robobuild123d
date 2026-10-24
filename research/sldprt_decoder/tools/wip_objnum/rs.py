import sys, json
sys.path.insert(0, '.')
from sldprt import validate as V
R = '/mnt/project-files/robot-cad/research/sldprt'
for f in (False, True):
    V.FACES = f
    r = V.run(R + '/revdev', R + '/dumps_v2')
    for sp in ('train', 'validation'):
        for k, v in r[sp].items():
            if 'Region' in k: print(f, sp, k, v['ok'], v['n'], v['pct'])
