import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'wip_r14')); sys.path.insert(0, os.path.join(HERE, '..'))
import decode_only as D, xt_mesh as X
from sldprt import displaylist as DL
for p in sys.argv[1:]:
    st = {}; A = X.mesh(os.path.join(D.DEC, p + '.json'), st)
    B = DL.triangles(os.path.join(D.ROOT, 'revdev', p + '.SLDPRT'))
    print(p, st, 'xt-vs-display IoU', None if B is None else round(D.iou(A, B)[0], 4), 'xt vol', round(abs(DL.volume(A)), 1), flush=True)
