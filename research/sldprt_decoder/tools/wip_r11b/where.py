import sys, os, glob, struct
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
for p in sorted(glob.glob(R + 'dumps_v2/*.dump.txt')):
    n = os.path.basename(p)[:-9]; d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d); S=struct.unpack_from('<I',d,0)[0]
    c=Counter('S-%d'%(S-e.cls) for e in ev if not e.name)
    print(n[:25], S, {k:c[k] for k in sys.argv[1:]})
