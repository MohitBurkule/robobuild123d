"""Region-selection misses (face-evidenced segments not selected) with/without crossing splits."""
import sys, glob, os
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, fstream as FS, answer_key as AK
R = '/mnt/project-files/robot-cad/research/sldprt/'
FS.SPLIT_CROSSINGS = '--nosplit' not in sys.argv
names = sorted(os.path.basename(p)[:-9] for p in glob.glob(R + 'dumps_v2/*.dump.txt'))
tot = {}
for k, n in enumerate(names):
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT')
    V.DEBUG = []
    acc = V.Acc()
    V.evaluate(d, AK.parse(R + 'dumps_v2/' + n + '.dump.txt'), acc)
    for key, c in acc.c.items():
        if key[0] == 'RegionSelection' and 'chooser)' in key[1]:
            sp = 'train' if k % 2 == 0 else 'val'
            t = tot.setdefault(sp, [0, 0]); t[0] += c['ok']; t[1] += c['n']
    for x in V.DEBUG:
        print(n[:20], x[0], x[1], 'missed', x[2])
print(tot)
