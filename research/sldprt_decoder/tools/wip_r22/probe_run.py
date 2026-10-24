"""r21 diagnostic: run_part with the current env into a scratch dir; print oracle, faces, log of FAIL/revolve lines."""
import sys, os, json
os.environ.setdefault('R15_OUT', os.path.dirname(os.path.abspath(__file__)))
import decode_replay as D
part, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
r = D.run_part(part, out_dir=out)
json.dump(r, open(os.path.join(out, part + '.json'), 'w'), indent=1, default=float)
print('oracle', r.get('oracle_iou'), r.get('ops'), r.get('seconds'), r.get('beam'))
for x in r.get('log', []):
    if x['status'] in ('FAIL', 'OK') and ('Revol' in x['feature'] or x['status'] == 'FAIL' or 'beam' in x['feature']) or x['feature'] in sys.argv[3:]:
        print({k: str(v)[:140] for k, v in x.items()})
