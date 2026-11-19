"""Round 6: wheel pairs closer (gap ~4 mm), photo colours, clear ramp skins, more lid screws,
switch moved under a lid slot. Input: the round-5 spec; output: new spec."""
import json, sys, copy, math, os

SRC, DST = sys.argv[1], sys.argv[2]
DY = float(os.environ.get('DY', '3.0'))          # each wheel pair moves DY toward the midline
MAT = os.environ.get('MAT', 'asa')
SKIN_T = float(os.environ.get('SKIN_T', '0.5'))
Y0 = -9.0
s = json.load(open(SRC))
P = {p['id']: p for p in s['parts']}

YR, YF = -28.0, 10.0
ymap = {YR: YR + DY, YF: YF - DY, -7.483: float(os.environ.get('BY', '-9.0'))}   # wheels/motors/pockets, battery centred on y0

def remap(n):
    if isinstance(n, dict):
        a = n.get('at')
        if isinstance(a, list) and len(a) == 3 and a[1] in ymap:
            a[1] = ymap[a[1]]
        for v in n.values(): remap(v)
    elif isinstance(n, list):
        for v in n: remap(v)
for p in s['parts']:
    if p['id'].startswith('dt_hub_'):
        yy = [a[1] for a in [n for n in [p['shape']['base']['items'][0]['base']['items'][0]['at']]]][0]
        p['at'] = [0.0, DY if yy == YR else -DY, 0.0]
        continue
    if p['id'].startswith(('wheel_', 'dm_', 'el_')):
        if p['at'][1] in ymap: p['at'][1] = ymap[p['at'][1]]
        continue
    remap(p)

# wire channels: the cylinders near the motor terminals ride with the motors
def chan(n):
    if isinstance(n, dict):
        if n.get('type') == 'place' and isinstance(n.get('shape'), dict) and n['shape'].get('type') == 'cylinder' \
                and n['shape'].get('radius', 0) < 3.6 and 8 < abs(n['at'][0]) < 13 and abs(n['at'][2]) < 0.2:
            y = n['at'][1]
            if y < -18: n['at'][1] = round(y + DY, 3)
            elif y > 2.4: n['at'][1] = round(y - DY, 3)
        for v in n.values(): chan(v)
    elif isinstance(n, list):
        for v in n: chan(v)
if os.environ.get("CH","1")=="1": chan(P["chassis"]["shape"]); chan(P["top_plate"]["shape"])

# colours from the photos: black tyres, red 3-spoke hubs
for p in s['parts']:
    if p['id'].startswith('wheel_'): p['color'] = '#1c1c1e'
    if p['id'].startswith('dt_hub_'): p['color'] = '#c8303a'
    if p['id'] in ('chassis', 'top_plate'): p['material'] = MAT
P['chassis']['color'] = '#2f8fe0'

# clear ramp skins: tape sheet on each ramp, inset 2.5 mm below the top band, down to the lip
L, RT, H0, H1 = 48.0, 31.0, 16.0, -10.5
run, rise = L - RT, H0 - H1
slen = math.hypot(run, rise); ang = math.degrees(math.atan2(rise, run))
u = (run / slen, -rise / slen); nrm = (rise / slen, run / slen)
s0, s1 = 2.5, slen - 0.3
mid = (s0 + s1) / 2
cy = RT + mid * u[0] + nrm[0] * (SKIN_T / 2 + 0.2)
cz = H0 + mid * u[1] + nrm[1] * (SKIN_T / 2 + 0.2)
for nm, sg in (('skin_front', 1), ('skin_rear', -1)):
    s['parts'].append({
        "id": nm, "kind": "other", "material": "tape", "process": "sheet_cut",
        "color": "#d8ecf7",
        "shape": {"type": "box", "size": [70.0, round(s1 - s0, 2), SKIN_T]},
        "at": [0.0, round(Y0 + sg * cy, 3), round(cz, 3)], "rot": [round(-sg * ang, 3), 0.0, 0.0],
        "retained": "tape",
        "retained_reason": "clear tape sheet laid flat on the ramp face (photo aws71/aws74); 70 x 29 mm contact patch",
    })
    s['connections'].append({"a": nm, "b": "chassis", "method": "tape",
                             "reason": "replaceable clear tape skin over the printed ramp, as in the photos; light (about 1 g) and fully backed by the ramp face"})
json.dump(s, open(DST, 'w'), indent=1)
print('skin', cy, cz, ang, slen)
