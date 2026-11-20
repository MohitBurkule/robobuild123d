"""Make the chassis outer shape a two-way arrow: build ONE quarter and mirror it
left-right (x) and front-back (y about the wheel-pair midline y0)."""
import json, sys, copy, os

SRC, DST = sys.argv[1], sys.argv[2]
import os
FX=float(os.environ.get('FX','32.6')); WALL=float(os.environ.get('WALL','1.6'))
P = dict(
    y0=-9.0,          # midline between the wheel pairs (y=-28, y=10)
    half_len=float(sys.argv[3]) if len(sys.argv) > 3 else 52.0,
    ramp_top=float(sys.argv[4]) if len(sys.argv) > 4 else 31.0,  # v where the ramp starts at top
    side_x=39.0,      # body side between the wheels
    wing_v=float(os.environ.get('WING','34.5')),      # end block (full width) starts past the wheel clearance
    wing_x=52.0,      # end block half width, covers the wheels
    chamfer_v=float(sys.argv[5]) if len(sys.argv) > 5 else 39.0,
    tip_x=float(sys.argv[6]) if len(sys.argv) > 6 else 36.0,
    fast_v=30.0, plate_half=32.0,
)
L, H = P['half_len'], 28.0

def place(shape, at=(0, 0, 0), rot=(0, 0, 0)):
    return {"type": "place", "shape": shape, "at": list(at), "rot": list(rot)}

def quarter():
    side = place({"type": "prism", "height": 2 * (P['wing_x'] + 1),
                  "points": [[0, 0], [L, 0], [L, 1.5], [P['ramp_top'], H], [0, H]]},
                 (0, 0, -12.0), (90.0, 0.0, 90.0))
    plan = {"type": "prism", "height": 80.0, "points": [
        [0, 0], [P['side_x'], 0], [P['side_x'], P['wing_v']], [P['wing_x'], P['wing_v']],
        [P['wing_x'], P['chamfer_v']], [P['tip_x'], L], [0, L]]}
    return {"type": "intersect", "items": [side, plan]}

def outer():
    q = quarter()
    half = {"type": "union", "items": [q, {"type": "mirror", "axis": "x", "shape": copy.deepcopy(q)}]}
    full = {"type": "union", "items": [half, {"type": "mirror", "axis": "y", "shape": copy.deepcopy(half)}]}
    return place(full, (0, P['y0'], 0))

def is_old_outer(n):
    return (isinstance(n, dict) and n.get('type') == 'intersect' and len(n['items']) == 2
            and n['items'][0].get('type') == 'place'
            and n['items'][0]['shape'].get('type') == 'prism'
            and n['items'][0]['shape'].get('height') == 106.0)

count = [0]
def walk(n):
    if isinstance(n, dict):
        for k, v in list(n.items()):
            if is_old_outer(v):
                n[k] = outer(); count[0] += 1
            else:
                walk(v)
    elif isinstance(n, list):
        for i, v in enumerate(n):
            if is_old_outer(v):
                n[i] = outer(); count[0] += 1
            else:
                walk(v)

s = json.load(open(SRC))
walk(s['parts'])
print('outer replaced', count[0])

# symmetric fastener rows, plate centred on y0
ymap = {-43.4: P['y0'] - P['fast_v'], 3.1: P['y0'] + P['fast_v']}
def fix_xy(n):
    if isinstance(n, dict):
        for k in ('at',):
            a = n.get(k)
            if isinstance(a, list) and len(a) == 3 and abs(abs(a[0]) - 33.4) < 1e-6 and a[1] in ymap:
                a[1] = ymap[a[1]]; a[0] = (FX if a[0] > 0 else -FX)
            if isinstance(a, list) and len(a) == 3 and a[1] == -20.125:
                a[1] = P['y0']
        if n.get('type') == 'box' and n.get('size', [0, 0])[1] == 51.75:
            n['size'][1] = 2 * P['plate_half']
        for v in n.values(): fix_xy(v)
    elif isinstance(n, list):
        for v in n: fix_xy(v)
fix_xy(s['parts']); fix_xy(s['fasteners'])
# skin: cavity = outer eroded by WALL (six shifted copies of the outer)
def fix_wall(n):
    if isinstance(n, dict):
        if n.get('type') == 'place' and isinstance(n.get('shape'), dict) and n['shape'].get('type') == 'place' \
           and n['shape'].get('at') == [0, P['y0'], 0]:
            n['at'] = [(WALL if c > 0 else -WALL) if abs(abs(c) - 2.0) < 1e-9 else c for c in n['at']]
        for v in n.values(): fix_wall(v)
    elif isinstance(n, list):
        for v in n: fix_wall(v)
fix_wall(s['parts'])
json.dump(s, open(DST, 'w'), indent=1)
