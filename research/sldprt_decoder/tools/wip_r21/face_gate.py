"""Round 16 strict gate: rebuild_dump/face_audit.py per part (rebuilt B-rep vs dumps_v2 FACE lines).
python3 face_gate.py [breps_dir] -> face_audit.json / .txt.  matched% = exact patches / dump patches."""
import sys, os, json, glob, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'rebuild_dump'))
import face_audit as FA
from build123d import import_brep, export_step

def gate(brep, dump):
    st = os.path.join(tempfile.mkdtemp(), 'x.step'); export_step(import_brep(brep), st)
    r = FA.audit(FA.faces_from_dump(dump), FA.faces_from_step(st)); c = r['counts']
    nd = sum(c.get(k, 0) for k in ('matched', 'area', 'trim', 'param', 'split', 'missing'))
    return dict(counts=c, dump_patches=nd, matched=c.get('matched', 0), pct=round(100 * c.get('matched', 0) / max(nd, 1), 1))

if __name__ == '__main__':
    bd = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'breps'); out = {}
    for b in sorted(glob.glob(os.path.join(bd, '*.brep'))):
        p = os.path.basename(b)[:-5]; d = os.path.join(ROOT, 'dumps_v2', p + '.dump.txt')
        if not os.path.exists(d): continue
        try: out[p] = gate(b, d)
        except Exception as ex: out[p] = dict(error=repr(ex)[:200], pct=0.0)
        print(p, out[p].get('matched'), out[p].get('dump_patches'), out[p]['pct'], flush=True)
    tag = os.path.basename(os.path.normpath(bd))
    json.dump(out, open(os.path.join(HERE, f'face_audit_{tag}.json'), 'w'), indent=1)
