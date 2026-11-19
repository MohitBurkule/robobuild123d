"""Round 6b: lid screws 4 -> 8 (3 per long edge + 2 by the switch slot) and the power switch moved
up under a slot in the lid (photo aws74)."""
import json, sys, copy, os
SRC, DST = sys.argv[1], sys.argv[2]
ZS = float(os.environ.get('ZS', '11.4'))
TOPZ = 16.6
s = json.load(open(SRC)); P = {p['id']: p for p in s['parts']}
SW = (-0.0, -28.5)
def fix(n):
    if isinstance(n, dict):
        a = n.get('at'); sh = n.get('shape')
        if isinstance(a, list) and len(a) == 3 and abs(a[1] + 28.5) < 1e-6 and isinstance(sh, dict) and sh.get('type') == 'box':
            sz = sh['size']
            if abs(a[2] + 8.5) < 1e-6:            # switch body / its pocket walls
                a[2] = ZS
            elif abs(a[2] + 10.75) < 1e-6:        # lever slot (was through the belly) -> up through the lid
                wall = sz[2] - 4.5                # 0 for the clearance cut, 5 for the walls
                h = (TOPZ - ZS) + wall
                a[2] = round((TOPZ + ZS) / 2, 3); sz[2] = round(h, 3)
        for v in n.values(): fix(v)
    elif isinstance(n, list):
        for v in n: fix(v)
fix(P['chassis']['shape']); fix(P['top_plate']['shape'])
sw = P['el_switch']; sw['at'] = [0.0, -28.5, ZS]; sw['rot'] = [0, 0, 0]
sw['retained_reason'] = 'switch body sits in a printed pocket under the lid; the lever comes up through an 8 x 4 mm slot in the lid (photo aws74)'
for c in s['connections']:
    if c['a'] == 'el_switch':
        c['reason'] = 'slide switch sits in a printed pocket just under the lid, lever reached through an 8 x 4 mm slot in the lid; the pocket walls hold it on every side'

# extra screws: copy screw 0's boss, tap hole, lid counterbore and clearance hole to new places
base = s['fasteners'][0]; bx, by = base['at'][0], base['at'][1]
def copies(tree_items, x, y):
    out = []
    for it in tree_items:
        if isinstance(it, dict) and it.get('type') == 'place' and it['at'][0] == bx and it['at'][1] == by:
            c = copy.deepcopy(it); c['at'][0] = x; c['at'][1] = y; out.append(c)
    return out
new = [(-32.6, -9.0), (32.6, -9.0), (-9.0, -39.0), (9.0, -39.0)]
ch = P['chassis']['shape']; tp = P['top_plate']['shape']
for i, (x, y) in enumerate(new):
    ch['base']['items'] += copies(ch['base']['items'], x, y)
    ch['cut'] += copies(ch['cut'], x, y)
    tp['cut'] += copies(tp['cut'], x, y)
    f = copy.deepcopy(base); f['id'] = f'fs_look_top_plate_{4 + i}'; f['at'][0] = x; f['at'][1] = y
    f['reason'] = 'M2 button-head screw where the photo (aws74) shows an extra lid screw, flush in a counterbore; clamps `top_plate` to `chassis`'
    s['fasteners'].append(f)
# wire window from the switch pocket forward into the hollow (battery and ESC leads)
P['chassis']['shape']['cut'].append({"type": "place", "shape": {"type": "box", "size": [7.0, 7.0, 5.0]},
                                     "at": [0.0, -24.0, ZS - 2.6], "rot": [0, 0, 0]})
json.dump(s, open(DST, 'w'), indent=1)
