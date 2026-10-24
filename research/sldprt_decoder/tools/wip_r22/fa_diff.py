"""round 18 check tool: per-dump-face audit status of two breps of one part (which faces moved)."""
import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'rebuild_dump')); import face_audit as FA
from build123d import import_brep, export_step
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
def stat(part, b, dumps='dumps_v2'):
    st = os.path.join(tempfile.mkdtemp(), 'x.step'); export_step(import_brep(b), st)
    r = FA.audit(FA.faces_from_dump(os.path.join(R, dumps, part + '.dump.txt')), FA.faces_from_step(st)); out = {}
    for k in ('matched', 'area', 'trim', 'param', 'split', 'missing'):
        for x in r[k]:
            d = x.get('dump')
            if d is None: continue
            out[(d['kind'], tuple(d['box']))] = (k, d['features'])
    return out
if __name__ == '__main__':
    part, a, b = sys.argv[1:4]; A, B = stat(part, a), stat(part, b)
    for key in A:
        if A[key][0] != B.get(key, ('?',))[0]: print(A[key][0], '->', B.get(key, ('?',))[0], key[0], key[1], A[key][1])
