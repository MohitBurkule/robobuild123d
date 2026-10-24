"""Sketch relations (geometric constraints) and dimension-to-entity links.

Layout (reverse engineered; see decoded/README_items/relations.md)
--------------------------------------------------------------------
There are no per-relation MFC classes.  Inside each sketch's sgSketch body
the relations are a run of fixed records:

    u32 type  u16 2  u16 flag(0|1)  u16 ?(0|1|2)  u16 0xFFFE  u16 0      (14 bytes)
    slot*     u16 handle_tag  u16 index  i32 -1  u32 0                   (12 bytes each)

`type` is SolidWorks' public swConstraintType_e enum (4 HORIZONTAL,
5 VERTICAL, 6 TANGENT, 9 COINCIDENT, 12 ATMIDDLE ...), confirmed below by
geometric verification.  handle_tag is an MFC class reference (0x8000|n) to
sgPointHandle / sgLineHandle / sgArcHandle / ... ; a slot may also carry the
inline first-use ClassDef (FF FF 01 00 len name) instead of a tag.
Indices: point handles = 0-based index into the sketch's point records in file
order (same convention as segment start/end); line/arc handles = the segment
record's rec_id (u32 before the sketch marker) minus a per-sketch base of
0 or 1 (chosen by geometric agreement; the source of the base is unknown); lines and arcs have separate
id spaces (a line and an arc in one sketch can both have id 1).

Tag -> handle class is not computable without the full MFC object count, so it
is inferred per stream from relation semantics (tag used by single-slot
HORIZONTAL/VERTICAL = line; tag used by HORIZPOINTS/VERTPOINTS = point;
tag paired with a point in CONCENTRIC/CORADIAL = arc).

Dimension links: after each DimValue (CString 'D<n>' ... f64) the same slot
structure lists the dimensioned entities.
"""
import json
import math
import os
import re
import struct
from collections import Counter, defaultdict

from . import sketch as SK
from . import streams as S
from . import mfc

# swConstraintType_e (SolidWorks API, public enum)
CTYPE = {1: 'distance', 2: 'angle', 3: 'radius', 4: 'horizontal', 5: 'vertical', 6: 'tangent', 7: 'parallel',
         8: 'perpendicular', 9: 'coincident', 10: 'concentric', 11: 'symmetric', 12: 'midpoint',
         13: 'intersection', 14: 'equal', 15: 'diameter', 16: 'offset_edge', 17: 'fixed', 18: 'arc_ang90',
         25: 'horizontal_points', 26: 'vertical_points', 27: 'collinear', 28: 'coradial', 32: 'use_edge',
         40: 'pierce?', 57: 'unknown_57', 75: 'slot_handle?'}

HDR = re.compile(rb'([\x01-\x7f])\x00\x00\x00\x02\x00[\x00\x01]\x00[\x00-\x02]\x00\xfe\xff\x00\x00', re.S)
INLINE = re.compile(rb'\xff\xff\x01\x00([\x01-\x40])\x00')
TOL = 1e-6


def read_slots(d, j, maxn=6):
    """Slots starting at j -> ([(tag|classname, idx)], end)."""
    out = []
    while len(out) < maxn and j + 12 <= len(d):
        tag = struct.unpack_from('<H', d, j)[0]
        m = INLINE.match(d, j)
        if m:
            ln = m.group(1)[0]
            name = d[m.end():m.end() + ln].decode('latin1')
            k = m.end() + ln
            if d[k + 2:k + 6] == b'\xff\xff\xff\xff':
                out.append((name, struct.unpack_from('<H', d, k)[0]))
                j = k + 10
                continue
            break
        if tag & 0x8000 and tag != 0xFFFF and d[j + 4:j + 8] == b'\xff\xff\xff\xff':
            out.append((tag, struct.unpack_from('<H', d, j + 2)[0]))
            j += 12
            continue
        break
    return out, j


def relation_records(d, start, end):
    out = []
    for m in HDR.finditer(d, start, end):
        slots, _ = read_slots(d, m.end())
        out.append({'pos': m.start(), 'type_code': m.group(1)[0], 'flag': struct.unpack_from('<H', d, m.start() + 6)[0],
                    'slots': slots})
    return out


def dim_links(d, start, end):
    out = []
    for r in mfc.dim_values(d[start:end]):
        a = start + r.end
        # first slot run within 120 bytes after the value
        for j in range(a, min(a + 120, end)):
            if d[j + 1] & 0x80 and d[j + 4:j + 8] == b'\xff\xff\xff\xff' and d[j:j + 2] != b'\xff\xff':
                slots, e = read_slots(d, j)
                if slots:
                    out.append({'pos': start + r.offset, 'dim': r.value['name'], 'value': r.value['value'],
                                'slots': slots})
                break
    return out


def infer_tags(rels):
    votes = defaultdict(Counter)
    for r in rels:
        t, s = r['type_code'], r['slots']
        if t in (4, 5) and len(s) == 1:
            votes[s[0][0]]['line'] += 1
        if t in (25, 26) and len(s) >= 2:
            for x in s[:2]:
                votes[x[0]]['point'] += 1
    pt = {k for k, v in votes.items() if v.most_common(1)[0][0] == 'point'}
    for r in rels:
        if r['type_code'] in (10, 28):
            for x in r['slots'][:2]:
                if x[0] not in pt:
                    votes[x[0]]['arc'] += 1
    roles = {k: v.most_common(1)[0][0] for k, v in votes.items()}
    if 'point' not in roles.values():  # fallback: the non-line/arc tag most used by COINCIDENT
        c = Counter(x[0] for r in rels if r['type_code'] == 9 for x in r['slots'][:2] if x[0] not in roles)
        if c:
            roles[c.most_common(1)[0][0]] = 'point'
    for k in list(roles):
        if isinstance(k, str):
            roles[k] = {'sgPointHandle': 'point', 'sgLineHandle': 'line', 'sgArcHandle': 'arc'}.get(k, roles[k])
    return roles


# ---------------------------------------------------------------- geometry
def _ent(role, idx, pts, segs_by_id):
    if role == 'point':
        if idx < len(pts) and pts[idx]['x'] is not None:
            return {'kind': 'point', 'p': (pts[idx]['x'], pts[idx]['y'])}
        return None
    g = segs_by_id.get((0 if role == 'line' else 1, idx))
    if not g:
        return None
    P = lambda i: (pts[i]['x'], pts[i]['y']) if i is not None and i < len(pts) and pts[i]['x'] is not None else None
    A, B = P(g['start']), P(g['end'])
    if g['kind'] == 0 and A and B:
        return {'kind': 'line', 'a': A, 'b': B}
    if g['kind'] == 1:
        C = P(g['centre'])
        if C and A:
            return {'kind': 'arc', 'c': C, 'r': math.dist(A, C), 'a': A, 'b': B}
    return None


def _ldist(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(vx, vy)
    return abs((p[0] - a[0]) * vy - (p[1] - a[1]) * vx) / L if L > 0 else math.dist(p, a)


def _dir(e):
    return (e['b'][0] - e['a'][0], e['b'][1] - e['a'][1])


def verify(t, E):
    """True/False when checkable, None when not."""
    E = [e for e in E if e]
    k = [e['kind'] for e in E]
    try:
        if t in (4, 5) and k[:1] == ['line']:
            dx, dy = _dir(E[0])
            return abs(dy if t == 4 else dx) < TOL
        if t in (4, 5, 25, 26) and k[:2] == ['point', 'point']:
            i = 1 if t in (4, 25) else 0
            return abs(E[0]['p'][i] - E[1]['p'][i]) < TOL
        if t == 9 and len(E) >= 2:
            a, b = sorted(E[:2], key=lambda e: e['kind'] != 'point')
            if a['kind'] != 'point':
                return None
            if b['kind'] == 'point':
                return math.dist(a['p'], b['p']) < TOL
            if b['kind'] == 'line':
                return _ldist(a['p'], b['a'], b['b']) < TOL
            return abs(math.dist(a['p'], b['c']) - b['r']) < TOL
        if t == 12 and len(E) >= 2:
            a, b = sorted(E[:2], key=lambda e: e['kind'] != 'point')
            if a['kind'] == 'point' and b['kind'] == 'line':
                m = ((b['a'][0] + b['b'][0]) / 2, (b['a'][1] + b['b'][1]) / 2)
                return math.dist(a['p'], m) < TOL
        if t in (7, 8, 27) and k[:2] == ['line', 'line']:
            u, v = _dir(E[0]), _dir(E[1])
            nu, nv = math.hypot(*u), math.hypot(*v)
            cr = (u[0] * v[1] - u[1] * v[0]) / (nu * nv)
            dt = (u[0] * v[0] + u[1] * v[1]) / (nu * nv)
            if t == 7:
                return abs(cr) < 1e-6
            if t == 8:
                return abs(dt) < 1e-6
            return abs(cr) < 1e-6 and _ldist(E[1]['a'], E[0]['a'], E[0]['b']) < TOL
        if t == 14 and len(E) >= 2 and k[0] == k[1]:
            if k[0] == 'line':
                return abs(math.dist(E[0]['a'], E[0]['b']) - math.dist(E[1]['a'], E[1]['b'])) < TOL
            if k[0] == 'arc':
                return abs(E[0]['r'] - E[1]['r']) < TOL
        if t == 6 and len(E) >= 2:
            ks = sorted(k[:2])
            if ks == ['arc', 'line']:
                a = E[0] if k[0] == 'arc' else E[1]
                l = E[1] if k[0] == 'arc' else E[0]
                return abs(_ldist(a['c'], l['a'], l['b']) - a['r']) < TOL
            if ks == ['arc', 'arc']:
                dd = math.dist(E[0]['c'], E[1]['c'])
                return min(abs(dd - E[0]['r'] - E[1]['r']), abs(dd - abs(E[0]['r'] - E[1]['r']))) < TOL
        if t in (10, 28) and len(E) >= 2:
            cs = [e['c'] if e['kind'] == 'arc' else e.get('p') for e in E[:2]]
            if None in cs:
                return None
            ok = math.dist(*cs) < TOL
            if t == 28 and k[:2] == ['arc', 'arc']:
                ok = ok and abs(E[0]['r'] - E[1]['r']) < TOL
            return ok
        if t == 11 and len(E) >= 3 and k[2] == 'line':
            p, q, l = E[0], E[1], E[2]
            if p['kind'] == q['kind'] == 'point':
                m = ((p['p'][0] + q['p'][0]) / 2, (p['p'][1] + q['p'][1]) / 2)
                u = _dir(l)
                w = (q['p'][0] - p['p'][0], q['p'][1] - p['p'][1])
                return _ldist(m, l['a'], l['b']) < TOL and abs(u[0] * w[0] + u[1] * w[1]) < TOL * max(1e-3, math.hypot(*u))
    except (IndexError, ZeroDivisionError, TypeError):
        return None
    return None


def dim_value_check(val, E):
    E = [e for e in E if e]
    if not E:
        return None
    k = [e['kind'] for e in E]
    c = []
    if k == ['arc']:
        c = [E[0]['r'], 2 * E[0]['r']]
    elif k == ['line']:
        c = [math.dist(E[0]['a'], E[0]['b'])]
    elif len(E) >= 2:
        a, b = E[:2]
        if k[:2] == ['point', 'point']:
            c = [math.dist(a['p'], b['p']), abs(a['p'][0] - b['p'][0]), abs(a['p'][1] - b['p'][1])]
        elif sorted(k[:2]) == ['line', 'point']:
            p, l = (a, b) if k[0] == 'point' else (b, a)
            c = [_ldist(p['p'], l['a'], l['b'])]
        elif k[:2] == ['line', 'line']:
            c = [_ldist(b['a'], a['a'], a['b'])]
        elif k[:2] == ['arc', 'arc']:
            dd = math.dist(a['c'], b['c'])
            c = [dd, abs(a['r'] - b['r']), dd + a['r'] + b['r'], abs(dd - a['r'] - b['r'])]
        else:
            pa = a.get('p') or a.get('c')
            pb = b.get('p') or b.get('c')
            if pa and pb:
                c = [math.dist(pa, pb), abs(pa[0] - pb[0]), abs(pa[1] - pb[1])]
            if 'r' in a and pb:
                c.append(abs(math.dist(pa, pb) - a['r']))
            if 'r' in b and pa:
                c.append(abs(math.dist(pa, pb) - b['r']))
    if not c:
        return None
    return any(abs(x - val) < TOL for x in c)


def choose_base(recs, roles, pts, sid):
    """Line/arc handle index = rec_id - base; base is 0 or 1 per sketch (unexplained, see notes).
    Picked by geometric agreement; ties -> 0."""
    best = (None, 0)
    for base in (0, 1):
        sc = 0
        for r in recs:
            E = [_ent(roles.get(t), i + (base if roles.get(t) in ('line', 'arc') else 0), pts, sid)
                 if roles.get(t) in ('point', 'line', 'arc') else None for t, i in r['slots']]
            v = verify(r['type_code'], E)
            sc += 1 if v else (-1 if v is False else 0)
        if best[0] is None or sc > best[0]:
            best = (sc, base)
    return best[1]


# ---------------------------------------------------------------- driver
def feature_stream(path):
    feat = None
    for s in S.all_streams(open(path, 'rb').read()):
        if S.classify(s) == 'features' and (feat is None or len(s['data']) > len(feat)):
            feat = s['data']
    return feat


def decode_part(sldprt_path, decoded_json):
    d = feature_stream(sldprt_path)
    j = json.load(open(decoded_json))
    sk = sorted([s for s in j.get('sketches', []) if s.get('stream_offset') is not None], key=lambda s: s['stream_offset'])
    allrels = relation_records(d, 0, len(d))
    roles = infer_tags(allrels)
    out = {'file': j['file'], 'tag_roles': {(hex(k) if isinstance(k, int) else k): v for k, v in roles.items()},
           'sketches': [], 'totals': Counter()}
    for n, s in enumerate(sk):
        a = s['stream_offset']
        b = sk[n + 1]['stream_offset'] if n + 1 < len(sk) else len(d)
        pts, segs, _ = SK.parse_records(d, a, b)
        sid = {(g['kind'], g['rec_id']): g for g in segs}
        recs = relation_records(d, a, b)
        base = choose_base(recs, roles, pts, sid)
        rels = []
        for r in recs:
            refs, E = [], []
            for tag, idx in r['slots']:
                role = roles.get(tag, 'unknown')
                refs.append({'role': role, 'index': idx, 'tag': hex(tag) if isinstance(tag, int) else tag})
                E.append(_ent(role, idx + (base if role in ('line', 'arc') else 0), pts, sid)
                         if role in ('point', 'line', 'arc') else None)
            v = verify(r['type_code'], E)
            rels.append({'type': CTYPE.get(r['type_code'], 'unknown_%d' % r['type_code']), 'type_code': r['type_code'],
                         'refs': refs, 'verified': v, 'offset': r['pos']})
            out['totals']['relations'] += 1
            out['totals']['verified_true' if v else ('verified_false' if v is False else 'unchecked')] += 1
        dl = []
        for x in dim_links(d, a, b):
            refs = [{'role': roles.get(t, 'unknown'), 'index': i} for t, i in x['slots']]
            E = [_ent(r['role'], r['index'] + (base if r['role'] in ('line', 'arc') else 0), pts, sid) if r['role'] in ('point', 'line', 'arc') else None for r in refs]
            v = dim_value_check(x['value'], E)
            dl.append({'dim': x['dim'], 'value_m': x['value'], 'refs': refs, 'value_matches_geometry': v})
            out['totals']['dim_links'] += 1
            out['totals']['dim_true' if v else ('dim_false' if v is False else 'dim_unchecked')] += 1
        out['sketches'].append({'name': s['name'], 'segment_id_base': base, 'relations': rels, 'dimension_links': dl,
                                'summary': dict(Counter(r['type'] for r in rels))})
    out['totals'] = dict(out['totals'])
    return out


def main(argv):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for part in argv:
        o = decode_part(os.path.join(root, 'revdev', part + '.SLDPRT'), os.path.join(root, 'decoded', part + '.json'))
        with open(os.path.join(root, 'decoded', part + '.relations.json'), 'w') as f:
            json.dump(o, f, indent=1)
        print(part, o['tag_roles'], o['totals'])


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
