"""IoU of the SLDPRT display mesh (Contents/DisplayLists) against the reference STL: oracle sanity check."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r14')); sys.path.insert(0, os.path.join(HERE, '..'))
import decode_only as D
from sldprt import displaylist as DL
import numpy as np
class M:  # mesh posing as a shape for D.compare
    def __init__(s, T): s.T = T
D.tri_of = lambda b, tol=0.02: b.T
if __name__ == '__main__':
    for part in sys.argv[1:]:
        T = DL.triangles(os.path.join(D.ROOT, 'revdev', part + '.SLDPRT'))
        print(part, None if T is None else D.compare(M(T), part), flush=True)
