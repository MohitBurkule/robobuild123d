"""Round 14: census of accepted external-class tags (absolute class index) per file."""
import sys, os, json, collections, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
todo = json.load(open('seedfiles.json'))
tot = collections.Counter(); files = collections.Counter()
for dd, src, n in todo:
    d = V.feature_stream(R + src + '/' + n + '.SLDPRT')
    if d is None: continue
    S = struct.unpack_from('<I', d, 0)[0]
    ev, _ = ON.numbering(d)
    c = collections.Counter(e.cls for e in ev if e.kind == 'new' and e.cls < S)
    tot.update(c); files.update(c.keys())
    print(n[:30], S, ON.numbering.residual, sorted(c.items()), flush=True)
print('TOTAL', sorted(tot.items())); print('FILES', sorted(files.items()))
