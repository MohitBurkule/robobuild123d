"""r22: per-part oracle IoU / faces matched, R21 vs R22 (results/, face_audit_r21.json vs face_audit_breps.json)."""
import json, glob, os
HERE = os.path.dirname(os.path.abspath(__file__)); R21 = os.path.join(HERE, '..', 'wip_r21')
fa0 = json.load(open(os.path.join(R21, 'face_audit_r21.json'))); fa1 = json.load(open(os.path.join(HERE, 'face_audit_breps.json')))
m0 = sum(v.get('matched') or 0 for v in fa0.values()); n0 = sum(v.get('dump_patches') or 0 for v in fa0.values())
m1 = sum(v.get('matched') or 0 for v in fa1.values()); n1 = sum(v.get('dump_patches') or 0 for v in fa1.values())
print(f'faces R21 {m0}/{n0} = {100*m0/max(n0,1):.1f} %   R22 {m1}/{n1} = {100*m1/max(n1,1):.1f} %')
a, b, t0, t1 = [], [], 0, 0
for f in sorted(glob.glob(os.path.join(HERE, 'results', '*.json'))):
    p = os.path.basename(f)[:-5]; r1 = json.load(open(f)); r0 = json.load(open(os.path.join(R21, 'results', p + '.json')))
    o0, o1 = r0.get('oracle_iou'), r1.get('oracle_iou'); t0 += r0.get('seconds') or 0; t1 += r1.get('seconds') or 0
    if o0 is not None and o1 is not None: a.append(o0); b.append(o1)
    f0 = (fa0.get(p) or {}).get('pct'); f1 = (fa1.get(p) or {}).get('pct')
    if o0 != o1 or f0 != f1: print(f'| {p} | {o0} -> {o1} | {f0} -> {f1} | {r0.get("seconds")} -> {r1.get("seconds")} |')
print(f'mean oracle over {len(a)}: R21 {sum(a)/len(a):.4f} R22 {sum(b)/len(b):.4f}; seconds {t0:.0f} -> {t1:.0f}')
