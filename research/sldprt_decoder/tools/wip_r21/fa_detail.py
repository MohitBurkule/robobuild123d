"""r21 diagnostic: per dump patch face-audit category for one brep (rebuilt vs dump)."""
import sys, os, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'rebuild_dump'))
import face_audit as FA
from build123d import import_brep, export_step
b, d = sys.argv[1], sys.argv[2]
st = os.path.join(tempfile.mkdtemp(), 'x.step'); export_step(import_brep(b), st)
r = FA.audit(FA.faces_from_dump(d), FA.faces_from_step(st))
print(r['counts'])
for k, v in r.items():
    if k != 'counts': print(k, str(v)[:3000])
