"""Is moFR_c objref a back-reference to its feature's object (anchor for numbering drift)?"""
import sys, os, glob
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, fstream as FS, classrec as CR, item_fr as IF
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
for n in sys.argv[1:]:
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev, _ = ON.numbering(d)
    heads = FS.feature_headers(d); fobj = ON.feature_objects(d, heads, ev)
    idobj = {fid: i for fid, (h, i, c) in fobj.items()}
    refs = IF.decode(d, CR._obj_spans(d, ev))
    c = Counter()
    for r in refs:
        if r['feature_id'] in idobj:
            c[r['objref'] - idobj[r['feature_id']]] += 1
    print(n, ON.numbering.residual, c.most_common(8), len(refs))
