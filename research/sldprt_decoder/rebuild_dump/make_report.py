"""Write RV01_DUMP_REPORT.md from rv01_from_dump.log.json.   python3 make_report.py <run-label>"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(H, 'rv01_from_dump.log.json')))
c = d.get('compare', {})
hp = os.path.join(H, 'report_history.json')
hist = json.load(open(hp)) if os.path.exists(hp) else []
lab = sys.argv[1] if len(sys.argv) > 1 else f'run{len(hist) + 1}'
dv = c.get('dev', {})
row = dict(run=lab, iou=c.get('iou'), extra=c.get('extra'), missing=c.get('missing'), ours=c.get('volume', {}).get('ours'),
           ref=c.get('volume', {}).get('ref'), dmax=max(dv.get('ours_to_ref_max', 0), dv.get('ref_to_ours_max', 0)),
           dmean=(dv.get('ours_to_ref_mean', 0) + dv.get('ref_to_ours_mean', 0)) / 2, within=dv.get('frac_within_0p05'))
hist = [h for h in hist if h['run'] != lab] + [row]
json.dump(hist, open(hp, 'w'), indent=1)
L = ['# RV01 Chassis rebuilt from the SolidWorks API dump', '',
     'Script: `rv01_from_dump.py` (build123d). Source: `dumps_v2/RV01 Chassis.dump.txt`. Reference: RV01 body of the rvrn STEP',
     '(`rebuild/ref_rv01_asmframe.brep`, moved into the part frame). The reference is only queried, never added to the model.', '',
     f'## Latest result ({lab})', '',
     f"| metric | value |\n|---|---|\n| IoU | {row['iou']:.4f} |\n| volume ours / ref (mm3) | {row['ours']:.1f} / {row['ref']:.1f} |\n"
     f"| extra volume (ours - ref) | {row['extra']:.1f} mm3 |\n| missing volume (ref - ours) | {row['missing']:.1f} mm3 |\n"
     f"| max surface deviation | {row['dmax']:.3f} mm |\n| mean surface deviation | {row['dmean']:.4f} mm |\n"
     f"| surface within 0.05 mm | {100 * (row['within'] or 0):.1f} % |", '',
     '## Run history', '', '| run | IoU | extra | missing | max dev | mean dev |', '|---|---|---|---|---|---|']
L += [f"| {h['run']} | {h['iou']:.4f} | {h['extra']:.1f} | {h['missing']:.1f} | {h['dmax']:.3f} | {h['dmean']:.4f} |" for h in hist]
L += ['', '## Per-feature status (latest run)', '', '| feature | status | detail |', '|---|---|---|']
for e in d['log']:
    det = e.get('msg', '')
    for k in ('cells', 'ivs', 'edges', 'iou', 'vol', 'fixed'):
        if k in e: det += f' {k}={e[k]}'
    L.append(f"| {e['feature']} | {e['status']} | {det.strip()} |")
pcs = c.get('pieces', [])
if pcs:
    L += ['', '## Largest remaining differences', '', '| kind | vol mm3 | bbox lo | bbox hi |', '|---|---|---|---|']
    L += [f"| {p['kind']} | {p['vol']} | {p['lo']} | {p['hi']} |" for p in pcs]
for img in ('rv01_dump_iso.png', 'rv01_dump_top.png'):
    if os.path.exists(os.path.join(H, img)): L += ['', f'![{img}]({img})']
open(os.path.join(H, 'RV01_DUMP_REPORT.md'), 'w').write('\n'.join(L) + '\n')
print('report written', lab, row['iou'])
