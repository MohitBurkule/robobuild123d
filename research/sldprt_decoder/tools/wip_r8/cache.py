"""Extract feature streams of all 135 files into a pickle (r8 work cache)."""
import sys, os, glob, pickle
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V
R = '/mnt/project-files/robot-cad/research/sldprt/'
out = {}
for src in ('revdev', 'corpus'):
    for p in sorted(glob.glob(R + src + '/*.SLDPRT')):
        nm = os.path.basename(p)[:-7]
        try:
            d = V.feature_stream(p)
        except Exception as e:
            d = None
        out[(src, nm)] = d
pickle.dump(out, open(sys.argv[1], 'wb'))
print(len(out), sum(v is None for v in out.values()))
