"""Fillet_c / Chamfer_c feature records (item: fillets & chamfers).

Layout findings (RV01, RV17, RV23; see decoded/README_items/fillets.md):
  * Region = first CString of the feature name .. next feature name (features.feature_regions).
  * Dimension records:  CString(utf16 'D1') 00*8 40 FF FF FF FF 00*4 FF FE FF 00 00 00 <value f64 LE>
    00 00 00 <u32 dim id>.  The class (ThreeDRadiusDim_c / AngleDim_c / DistanceDim) precedes it.
    Radius / distance in metres, angle in radians (pi/4 stored truncated to 14 digits).
  * Entity references: 20-byte tuples <tag u32> <doc u32> <feature_id u32> <timestamp u32> <seq u32>,
    i.e. the same (feature_id, timestamp, seq) triple as the Parasolid ATOM_ID_2001 face attribute.
    A run of tuples with <=12 bytes gap forms one reference; before the first dim record the runs
    are the selected edges (3 face ids, sometimes preceded by a body id with seq 1) followed by
    their end vertices (4 face ids).
  * The radius is repeated once per selected item in per-edge records after the face history;
    all copies equal => constant radius (no variable fillet exists in the corpus to test).
"""
import json
import math
import re
import struct

from . import features as FP

DIM = re.compile(rb'\xff\xfe\xff([\x01-\x08])((?:[\x20-\x7e]\x00){1,8})\x00{7}\x40\xff\xff\xff\xff\x00{4}'
                 rb'\xff\xfe\xff\x00\x00\x00(.{8})\x00\x00\x00(.{4})', re.S)
CLASS = re.compile(rb'([A-Za-z0-9]+Dim_c)')


def dims_in(d, a, b):
    out = []
    for m in DIM.finditer(d, a, b):
        name = m.group(2).decode('utf-16-le')
        v = struct.unpack('<d', m.group(3))[0]
        c = CLASS.findall(d[max(a, m.start() - 48):m.start()])
        out.append({'name': name, 'value': v, 'offset': m.start() - a, 'dim_class': c[-1].decode() if c else None,
                    'dim_id': struct.unpack('<I', m.group(4))[0]})
    return out


def refs_in(d, a, b, fids):
    out, i = [], a
    while i < b - 20:
        x0, x1, fid, st, seq = struct.unpack_from('<5I', d, i)
        if fid in fids and 1.0e9 < st < 2.2e9 and seq < 1000000 and x0 < 0x10000000:
            out.append({'off': i - a, 'tag': x0 & 0xffff, 'fid': fid, 'stamp': st, 'seq': seq})
            i += 20
        else:
            i += 1
    return out


def clusters(refs, gap=12):
    cl = []
    for r in refs:
        if cl and r['off'] - (cl[-1][-1]['off'] + 20) <= gap:
            cl[-1].append(r)
        else:
            cl.append([r])
    return cl


def _atom_index(faces):
    ix = {}
    for k, fc in enumerate(faces):
        for at in fc.get('atom_ids') or []:
            ix.setdefault((at[1], at[2], at[4]), set()).add(k)
    return ix


def _face_radius(fc):
    p = fc.get('params') or {}
    for k in ('minor_radius', 'radius'):
        if k in p and fc['surface_type'] in ('cylinder', 'torus', 'sphere'):
            return p[k] if k == 'minor_radius' or fc['surface_type'] != 'torus' else p.get('minor_radius', p[k])
    return None


def _loop_circle_radii(fc):
    return sorted({round(e['curve']['radius'], 9) for lp in fc.get('loops') or [] for e in lp['edges']
                   if e.get('curve', {}).get('type') == 'circle'})


def _kw(v):
    m = re.search(r'(-?\d+(?:\.\d+)?)', v)
    if not m:
        return None
    x = float(m.group(1))
    return math.radians(x) if '°' in v else x / 1000


def decode_feature(d, f, a, b, J, fids, aix):
    faces = J['faces']
    is_ch = 'chamfer' in (f['type'] + f['name']).lower()
    dims = dims_in(d, a, b)
    first_dim = min([x['offset'] for x in dims], default=b - a)
    refs = refs_in(d, a, b, fids)
    kw = {k: _kw(v) for k, v in f['dims']}
    created = [k for k, fc in enumerate(faces) if any(at[1] == f['id'] for at in fc.get('atom_ids') or [])]
    own = [c for c in clusters([r for r in refs if r['off'] < first_dim])]
    created_seqs = [r['seq'] for c in own for r in c if r['fid'] == f['id']]
    sel = [c for c in own if not any(r['fid'] == f['id'] for r in c)]
    multi = {r['tag'] for c in sel for r in c if r['seq'] != 1}
    seen, cand = set(), []
    for c in sel:
        fr = tuple(sorted({(r['fid'], r['stamp'], r['seq']) for r in c if not (r['seq'] == 1 and r['tag'] not in multi)}))
        if fr and fr not in seen:
            seen.add(fr)
            cand.append((c[0]['off'], fr))
    edges, verts = [], []
    for off, fr in cand:
        ent = {'offset': off, 'face_refs': [[x[0], x[2]] for x in fr],
               'parasolid_faces': sorted({k for x in fr for k in aix.get(x, ())})}
        if any(set(o) < set(fr) for _, o in cand):
            verts.append(ent)
        else:
            edges.append(ent)
    for e in edges:
        sup = set(e['parasolid_faces'])
        ov = [(len(sup & set(faces[k].get('adjacent_faces') or [])), k) for k in created]
        best = max([o for o, _ in ov], default=0)
        e['blend_faces'] = [k for o, k in ov if o == best and o > 0]
        if is_ch:
            angs = []
            for k in e['blend_faces']:
                n1 = (faces[k].get('params') or {}).get('normal')
                for j in sup:
                    n2 = (faces[j].get('params') or {}).get('normal')
                    if n1 and n2 and faces[k]['surface_type'] == faces[j]['surface_type'] == 'plane':
                        c = abs(sum(x * y for x, y in zip(n1, n2)))
                        angs.append(round(math.degrees(math.acos(min(1, c))), 4))
            e['blend_support_plane_angles_deg'] = sorted(set(angs))
    vals = [x for x in dims]
    rad = [x['value'] for x in vals if x['name'] == 'D1']
    rec = {'name': f['name'], 'type': f['type'], 'region': [a, b], 'dims_decoded': vals,
           'keywords_dims': f['dims'], 'selected_edges': edges, 'edge_end_vertices': len(verts),
           'created_faces': created, 'created_face_seqs_in_record': created_seqs}
    if is_ch:
        dist = next((x['value'] for x in vals if kw.get(x['name']) is not None and abs(kw[x['name']] - x['value']) < 1e-9
                     and '°' not in dict(f['dims'])[x['name']]), None)
        ang = next((x['value'] for x in vals if x['name'] in kw and '°' in dict(f['dims']).get(x['name'], '')
                    and abs(kw[x['name']] - x['value']) < 1e-9), None)
        rec['chamfer_type'] = 'angle-distance' if ang is not None else ('distance-distance' if len(vals) >= 2 else 'unknown')
        rec['distance_m'], rec['angle_deg'] = dist, (math.degrees(ang) if ang is not None else None)
        legs = []
        if dist is not None and ang is not None:
            legs = [dist, dist * math.tan(ang)]
        rec['matches_keywords'] = dist is not None and ang is not None
        # Parasolid check: chamfer faces are planes; the chord width = dist/cos(angle) for 45 deg
        rec['expected_face_width_m'] = math.hypot(*legs) if legs else None
    else:
        r = rad[0] if rad else None
        copies = len(re.findall(re.escape(struct.pack('<d', r)), d[a:b])) if r else 0
        rec['fillet_type'] = 'constant-radius' if r else 'unknown'
        rec['radius_m'] = r
        rec['radius_copies_in_region'] = copies
        rec['n_items_from_radius_copies'] = max(copies - 4, 0)  # 4 header copies + 1 per selected item
        rec['variable_radius'] = False if r else None
        rec['matches_keywords'] = r is not None and abs(kw.get('D1', 1) - r) < 1e-9
        prad = []
        for k in created:
            pr = _face_radius(faces[k])
            if pr is not None:
                prad.append(('surface', k, pr))
            elif faces[k]['surface_type'] == 'blended_edge':
                for cr in _loop_circle_radii(faces[k]):
                    prad.append(('loop_circle', k, cr))
        rec['parasolid_blend_radii'] = sorted({round(x[2], 9) for x in prad})
        rec['parasolid_radius_match'] = (None if not prad else any(abs(x[2] - r) < 1e-7 for x in prad) if r else False)
    return rec


def decode(feat, J):
    fids = {f['id'] for f in J['features']}
    aix = _atom_index(J['faces'])
    out = []
    for f, a, b in FP.feature_regions(feat, J['features']):
        t = (f['type'] + ' ' + f['name']).lower()
        if 'fillet' in t or 'chamfer' in t:
            out.append(decode_feature(feat, f, a, b, J, fids, aix))
    return out


def run(sldprt_path, json_path, out_path):
    from . import streams as S
    data = open(sldprt_path, 'rb').read()
    fs = [s['data'] for s in S.all_streams(data) if S.classify(s) == 'features']
    J = json.load(open(json_path))
    res = decode(max(fs, key=len), J) if fs else []
    with open(out_path, 'w') as fh:
        json.dump({'file': J['file'], 'features': res}, fh, indent=1)
    return res
