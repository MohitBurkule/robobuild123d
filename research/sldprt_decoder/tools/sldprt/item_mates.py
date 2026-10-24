"""Full assembly-mate decode (item: ASSEMBLY MATES).

Layout found in the moMate* stream (SW2023 'rvrn 2.0', 'Micro slx v1.0'; SW older 'RVRN'):

  <MateName CString> 00 01 00 00 00 00 00 40 <mate_id u32> ...
  per entity side:  <entity-id-rep CString> <component path CString>
                    [component transform: 9 rot + 3 trans f64, first use]
                    snapshot geometry block (FF FF FF FF + 4 f64 + geom), frame = mate-creation (stale)
  "solve" table, one entry per entity, at the end of the mate:
      u32 mate_id, u32 entity_ref, u32 side_index(0,1,..), u32 kind, 2 bytes, 14x00, FF FF FF FF,
      4 f64 (uv/parameter box), point[3], direction[3], (cylinder: radius f64)
  geometry in the tail is in the ASSEMBLY frame (verified by mapping into the component
  frame with the component transform and finding the matching Parasolid face, see README_items/mates.md).

Alignment is derived from the tail directions (aligned = dot>0). The stored flag that encodes
it is searched for in `flag_candidates` (see report).
"""
import json
from collections import Counter
import os
import re
import struct

import numpy as np

from .asm import MATE_RE, cstrings, components, DIMV

UNIT_TOL = 1e-6
# u16 at name_end+163: 1 = aligned, 2 = anti-aligned (101/101 agree with solved geometry)
ALIGN = {0: 'closest?', 1: 'aligned', 2: 'anti-aligned'}


def _f64s(d, o, n):
    if o + 8 * n > len(d):
        return None
    return list(struct.unpack_from('<%dd' % n, d, o))


def _unit(v):
    return v is not None and all(np.isfinite(v)) and abs(np.linalg.norm(v) - 1) < 1e-6


def _clean(x):
    return 0.0 if abs(x) < 1e-12 else float(x)


def _geom(d, o):
    """geometry at o (just after FF FF FF FF): 4 params, point, dir, maybe radius."""
    v = _f64s(d, o, 11)
    if v is None or not all(np.isfinite(v[:10])) or max(abs(x) for x in v[:10]) > 100:
        return None
    if not _unit(v[7:10]):
        return None
    r = v[10]
    g = {'params': [_clean(x) for x in v[:4]], 'point': [_clean(x) for x in v[4:7]],
         'dir': [_clean(x) for x in v[7:10]], 'offset': o}
    g['radius_candidate'] = float(r) if np.isfinite(r) and 1e-5 < r < 0.5 else None
    return g


def _rot_blocks(d, a, b):
    out, last = [], -999
    for o in range(a, max(a, b - 96)):
        if o - last < 96:
            continue
        v = np.frombuffer(d, '<f8', 12, o)
        if not np.all(np.isfinite(v)) or np.abs(v).max() > 10:
            continue
        R = v[:9].reshape(3, 3)
        if np.abs(R @ R.T - np.eye(3)).max() < 1e-6 and abs(abs(np.linalg.det(R)) - 1) < 1e-6 and np.abs(v[:9]).max() <= 1 + 1e-9:
            out.append((o, [float(x) for x in v]))
            last = o
    return out


def parse_mates(d):
    cs = cstrings(d)
    idx = [k for k, (p, s) in enumerate(cs) if MATE_RE.match(s)]
    out = []
    for j, k in enumerate(idx):
        p, name = cs[k]
        e = cs[idx[j + 1]][0] if j + 1 < len(idx) else len(d)
        h = p + 4 + 2 * len(name)
        hdr = d[h:h + 16]
        mate_id = struct.unpack_from('<I', hdr, 8)[0]
        rec = {'name': name, 'type': re.sub(r'\d+$', '', name), 'mate_id': mate_id,
               'header_hex': hdr.hex(), 'offset': p, 'entities': []}
        if h + 172 <= e:
            al, f2, n_ent = struct.unpack_from('<HHI', d, h + 163)[0], struct.unpack_from('<H', d, h + 165)[0], struct.unpack_from('<I', d, h + 168)[0]
            rec['alignment_code'] = al
            rec['alignment'] = ALIGN.get(al, 'unknown(%d)' % al)
            rec['field_h165'] = f2
            rec['entity_count_field'] = n_ent
        # entity sides
        sides, last_rep = [], None
        strs = [(q, s) for q, s in cs[k + 1:] if q < e]
        for q, s in strs:
            if s.startswith('mo') and ',' in s:
                last_rep = [x.strip() for x in re.split(r'[\r\n]+', s.strip()) if x.strip()]
            elif '@' in s and not s.startswith(('H:', 'I:', 'C:')):
                sides.append({'component_path': s, 'entity_id_rep': last_rep, 'str_offset': q})
                last_rep = None
        for i, sd in enumerate(sides):
            nxt = sides[i + 1]['str_offset'] if i + 1 < len(sides) else e
            rb = _rot_blocks(d, sd['str_offset'], min(nxt, sd['str_offset'] + 1200))
            sd['stored_transform'] = rb[0][1] if rb else None
            sd.pop('str_offset')
        # solve table
        pat = re.compile(re.escape(struct.pack('<I', mate_id)) + rb'(.{4})(.{4})(.{4})(..)\x00{14}\xff\xff\xff\xff', re.S)
        tail = []
        for m in pat.finditer(d, p, e):
            ent_ref, side, kind = (struct.unpack('<I', m.group(i))[0] for i in (1, 2, 3))
            if side > 8 or kind > 8:
                continue
            g = _geom(d, m.end())
            if g:
                g.update({'entity_ref': ent_ref, 'side': side, 'kind': kind, 'tag_hex': m.group(4).hex()})
                tail.append(g)
        rec['solve_geometry'] = tail
        # trailer after last tail block: raw bytes for flag search
        if tail:
            t = tail[-1]['offset'] + 80
            rec['trailer_hex'] = d[t:t + 96].hex()
        for i, sd in enumerate(sides):
            g = next((g for g in tail if g['side'] == i), None)
            sd['geometry_asm'] = g
        rec['entities'] = sides
        if rec['type'] in ('Distance', 'Angle', 'Width'):
            m = DIMV.search(d, p, e)
            if m:
                rec['dim_name'] = m.group(2).decode('utf-16-le')
                rec['value'] = struct.unpack('<d', m.group(3))[0]
        out.append(rec)
    return out


# ---------------------------------------------------------------- validation against parts
def _part_faces(decoded_dir, part, cache={}):
    if part not in cache:
        fp = os.path.join(decoded_dir, part + '.json')
        cache[part] = json.load(open(fp))['faces'] if os.path.exists(fp) else None
    return cache[part]


def to_local(T, p, v):
    R = np.array(T[:9]).reshape(3, 3)
    t = np.array(T[9:12])
    return R @ (np.array(p) - t), R @ np.array(v)


def to_asm(T, p, v):
    R = np.array(T[:9]).reshape(3, 3)
    return np.array(T[9:12]) + R.T @ np.array(p), R.T @ np.array(v)


def match_face(faces, p, v, r, tol=2e-6):
    hits = []
    for f in faces or []:
        pr = f.get('params') or {}
        st = f.get('surface_type')
        if st == 'plane' and 'normal' in pr:
            n = np.array(pr['normal'])
            if abs(abs(n @ v) - 1) < 1e-6 and abs((p - np.array(pr['point'])) @ n) < tol:
                hits.append((f, 'plane', float(n @ v)))
        elif st in ('cylinder', 'cone') and 'axis' in pr:
            a = np.array(pr['axis'])
            if abs(abs(a @ v) - 1) > 1e-6:
                continue
            w = p - np.array(pr['point'])
            dist = np.linalg.norm(w - (w @ a) * a)
            if dist < tol and (st == 'cone' or r is None or abs(pr.get('radius', -1) - r) < tol):
                hits.append((f, st, float(a @ v)))
    return hits


def resolve(r, comps, decoded_dir, sub_comps=None):
    """Attach current instance, part face match, geometric checks."""
    by_T = {}
    for c in comps:
        if c['rotation_rows']:
            by_T.setdefault(tuple(round(x, 6) + 0.0 for x in c['rotation_rows'] + c['translation_m']), []).append(c['instance'])
    for m in r:
        for sd in m['entities']:
            T = sd['stored_transform']
            inst = by_T.get(tuple(round(x, 6) + 0.0 for x in T)) if T else None
            sd['instance_current'] = inst
            g = sd['geometry_asm']
            sd['face_match'] = None
            if not (g and T):
                continue
            part = None
            if inst:
                part = re.sub(r'-\d+$', '', inst[0])
            cands = [part] if part else []
            lp, lv = to_local(T, g['point'], g['dir'])
            res = []
            for pt in cands:
                for f, st, sgn in match_face(_part_faces(decoded_dir, pt), lp, lv, g['radius_candidate']):
                    res.append({'part': pt, 'xt_index': f['xt_index'], 'surface': st, 'face_sense': f['face_sense'],
                                'dir_vs_surface': round(sgn), 'radius': f['params'].get('radius'),
                                'feature': f.get('feature_first_name'), 'feature_last': f.get('feature_last_name')})
            sd['local_point'] = [_clean(x) for x in lp]
            sd['local_dir'] = [_clean(x) for x in lv]
            sd['face_match'] = res
        check(m)
    resolve_instances(r, comps)
    for m in r:
        for sd in m['entities']:
            inst = sd.get('instance_resolved')
            part = re.sub(r'-\d+$', '', inst) if inst else None
            fmap = _part_features(decoded_dir, part) if part else {}
            sd['rep_features'] = [{'feature_id': fid, 'feature_name': fmap.get(fid)}
                                  for fid in (rep_feature_id(x) for x in (sd.get('entity_id_rep') or [])) if fid is not None]
    return r


def rep_feature_id(rep):
    """entity-id-rep CString 'moFromSktEntSurfIdRep_c,42,18,' -> 42: the id of the feature (in the
    component part) that created the mated face (checked against the part dumps' FACE lists)."""
    p = rep.split(',')
    try:
        return int(p[1])
    except (IndexError, ValueError):
        return None


def _part_features(decoded_dir, part, cache={}):
    if part not in cache:
        fp = os.path.join(decoded_dir, part + '.json')
        out = {}
        if os.path.exists(fp):
            def walk(fs):
                for f in fs:
                    if isinstance(f, dict):
                        out.setdefault(f.get('id'), f.get('name'))
                        walk(f.get('children') or [])
            walk(json.load(open(fp)).get('features') or [])
        cache[part] = out
    return cache[part]


def _inst_no(n):
    m = re.search(r'-(\d+)$', n)
    return m.group(1) if m else None


def _tokens(n):
    return set(re.sub(r'-\d+$', '', n).lower().split())


def rename_match(head, names):
    """Round 10: a component replaced / renamed after the mate was made keeps its old
    instance name.  Match on the same instance number plus the longest common name
    suffix (>= 8 chars, e.g. 'RVRN 1.7 C1 Turnabot Spicy N10 2200 RPM-2' -> 'RV12 N10 2200
    RPM-2') or, failing that, >= 2 shared words ('side panel multipart-1' -> 'RV23 side
    panel LH-1').  Unique best only."""
    k = _inst_no(head)
    if k is None:
        return None
    cs = [n for n in names if _inst_no(n) == k]

    def suf(n):
        i = 0
        while i < min(len(n), len(head)) and n[-1 - i].lower() == head[-1 - i].lower():
            i += 1
        return i
    best = sorted(((suf(n), n) for n in cs), reverse=True)
    if best and best[0][0] >= 8 + len(k) + 1 and (len(best) == 1 or best[1][0] < best[0][0]):
        return best[0][1]
    th = _tokens(head)
    best = sorted(((len(th & _tokens(n)), n) for n in cs), reverse=True)
    if best and best[0][0] >= 2 and (len(best) == 1 or best[1][0] < best[0][0]):
        return best[0][1]
    return None


def resolve_instances(r, comps, asm_name=None):
    """Current component instance of every entity side, in order of evidence:
    0 'assembly'  no stored path, or a plane reference '<feature>@<comp>@<asm>' whose
                  component no longer exists: the API reports the assembly itself (round 10)
    1 'name'      the stored path's first element (before '@') is a current instance name
    1b 'renamed'  old instance name matched by instance number + name suffix/words (round 10)
    2 'transform' the stored component transform equals a current instance's transform (unique)
    3 'rename'    the stored name was resolved by transform on another side of this file
                  (components renamed after the mate was made keep their old name in the path)"""
    names = {c['instance'] for c in comps}
    if asm_name is None:
        tails = Counter(sd['component_path'].split('/')[0].split('@')[-1] for m in r for sd in m['entities']
                        if '@' in (sd.get('component_path') or ''))
        asm_name = tails.most_common(1)[0][0] if tails else None
    learned = {}
    for m in r:
        for sd in m['entities']:
            head = (sd.get('component_path') or '').split('/')[0].split('@')[0]
            inst = sd.get('instance_current') or []
            if head not in names and len(inst) == 1:
                learned.setdefault(head, Counter())[inst[0]] += 1
    for m in r:
        for sd in m['entities']:
            cp = sd.get('component_path') or ''
            el = cp.split('/')[0].split('@')
            head = el[0]
            inst = sd.get('instance_current') or []
            ren = None if head in names else rename_match(head, names)
            if not cp:
                sd['instance_resolved'], sd['instance_how'] = asm_name, 'assembly'
            elif len(el) == 3 and el[1] not in names and not rename_match(el[1], names):
                sd['instance_resolved'], sd['instance_how'] = asm_name, 'assembly'
            elif head in names:
                sd['instance_resolved'], sd['instance_how'] = head, 'name'
            elif ren:
                sd['instance_resolved'], sd['instance_how'] = ren, 'renamed'
            elif len(inst) == 1:
                sd['instance_resolved'], sd['instance_how'] = inst[0], 'transform'
            elif head in learned:
                sd['instance_resolved'], sd['instance_how'] = learned[head].most_common(1)[0][0], 'rename'
            else:
                sd['instance_resolved'], sd['instance_how'] = None, None


def check(m):
    gs = [sd['geometry_asm'] for sd in m['entities'][:2]]
    if len(gs) < 2 or not all(gs):
        m['check'] = 'no geometry'
        return
    a, b = gs
    pa, va, pb, vb = (np.array(a['point']), np.array(a['dir']), np.array(b['point']), np.array(b['dir']))
    dot = float(va @ vb)
    m['dir_dot'] = round(dot, 6)
    m['alignment_geometric'] = 'aligned' if dot > 1e-6 else ('anti-aligned' if dot < -1e-6 else 'perpendicular')
    t = m['type']
    if t == 'Width':
        m['alignment_geometric'] = None  # 4 entities: two face pairs, dot of side0/side1 is not the mate alignment
    sep_plane = float((pb - pa) @ va)
    w = pb - pa
    axis_dist = float(np.linalg.norm(w - (w @ va) * va))
    ok = None
    if t == 'Coincident':
        ok = abs(abs(dot) - 1) < 1e-6 and abs(sep_plane) < 1e-6 or (abs(dot) < 1e-6)
        if a['radius_candidate'] is None and b['radius_candidate'] is None and abs(abs(dot) - 1) < 1e-6:
            ok = abs(sep_plane) < 1e-6
        m['residual_m'] = sep_plane
    elif t == 'Concentric':
        ok = abs(abs(dot) - 1) < 1e-6 and axis_dist < 1e-6
        m['residual_m'] = axis_dist
    elif t == 'Parallel':
        ok = abs(abs(dot) - 1) < 1e-6
    elif t == 'Perpendicular':
        ok = abs(dot) < 1e-6
    elif t == 'Distance':
        m['measured_m'] = abs(sep_plane)
        m['signed_offset_along_A_m'] = sep_plane  # sign = which side of entity A; candidate for 'flip'
        ok = abs(dot) > 1 - 1e-6 and m.get('value') is not None and abs(abs(sep_plane) - m['value']) < 1e-6
    m['geometric_check'] = ok


def decode_asm_mates(path, decoded_dir):
    from .streams import all_streams
    data = open(path, 'rb').read()
    comp, mt = [], []
    for s in all_streams(data):
        d = s['data']
        if d.startswith(b'\xff\xff\x01\x00\x0c\x00moAssembly_c'):
            comp = components(d)
        if b'moMate' in d[:200]:
            mt = parse_mates(d)
    resolve(mt, comp, decoded_dir)
    groups = []
    for s in all_streams(data):
        d = s['data']
        for m in re.finditer(rb'NumberMates(.)\xa5class\xadmoMateGroup_c\xa5class\xacmoNodeList_c\xa6hidden.\xa4name(.)', d, re.S):
            n = m.group(2)[0] & 0x1f
            nm = d[m.end():m.end() + n].decode('latin1')
            groups.append({'name': nm, 'NumberMates': m.group(1)[0], 'source': 'msgpack feature index'})
    seen = set()
    groups = [g for g in groups if not (g['name'], g['NumberMates']) in seen and not seen.add((g['name'], g['NumberMates']))]
    for g in groups:
        g['members'] = [m['name'] for m in mt] if g['NumberMates'] == len(mt) else None
    return {'file': os.path.basename(path), 'n_mates': len(mt), 'mates': mt, 'mate_groups': groups}


def stats(r):
    ms = r['mates']
    geo = [m for m in ms if m.get('alignment_geometric') in ('aligned', 'anti-aligned')]
    return {'mates': len(ms),
            'with_solve_geometry': sum(1 for m in ms if m.get('geometric_check') is not None),
            'geometric_check_true': sum(1 for m in ms if m.get('geometric_check') is True),
            'geometric_check_false': [m['name'] for m in ms if m.get('geometric_check') is False],
            'alignment_flag_vs_geometry': '%d/%d' % (sum(1 for m in geo if m['alignment'] == m['alignment_geometric']), len(geo)),
            'entities_total': sum(len(m['entities']) for m in ms),
            'entities_face_matched': sum(1 for m in ms for e in m['entities'] if e.get('face_match')),
            'entities_unique_face': sum(1 for m in ms for e in m['entities'] if e.get('face_match') and len(e['face_match']) == 1)}


def _fmt_ent(e):
    inst = (e.get('instance_current') or ['?'])[0]
    g = e.get('geometry_asm')
    fm = e.get('face_match') or []
    face = ', '.join('#%d %s%s %s' % (f['xt_index'], f['surface'], (' r%.4g' % (f['radius'] * 1000)) if f.get('radius') else '', f.get('feature') or '') for f in fm[:3])
    if len(fm) > 3:
        face += ' (+%d)' % (len(fm) - 3)
    geo = ('p(%s) d(%s)%s' % (','.join('%.4g' % (x * 1000) for x in g['point']), ','.join('%.3g' % x for x in g['dir']),
           (' r%.4g' % (g['radius_candidate'] * 1000)) if g.get('radius_candidate') else '')) if g else '-'
    return '%s<br>`%s`<br>rep %s<br>asm %s<br>face %s' % (e['component_path'], inst, ' + '.join(e.get('entity_id_rep') or ['?']), geo, face or '-')


def to_md(r):
    st = stats(r)
    o = ['# %s - mates (full decode)\n' % r['file'].rsplit('.', 1)[0],
         'Generated by `tools/sldprt/item_mates.py`. Geometry in mm, assembly frame. "face" = Parasolid face in the component part (decoded/<part>.json xt_index) that the solved geometry lands on after mapping by the stored component transform. See README_items/mates.md.\n',
         'Stats: `%s`\n' % json.dumps(st),
         '## Mate groups\n'] + ['- %s: NumberMates=%d %s' % (g['name'], g['NumberMates'], '(= all mates below)' if g['members'] else '') for g in r['mate_groups']] + [
         '\n## Mates\n', '| mate | id | type | alignment (flag / geometry) | value | check | entity A | entity B (+more) |', '|---|---|---|---|---|---|---|---|']
    for m in r['mates']:
        v = ''
        if m.get('value') is not None:
            v = '%.4g mm' % (m['value'] * 1000) + (' (measured %.4g)' % (m['measured_m'] * 1000) if m.get('measured_m') is not None else '')
        es = [_fmt_ent(e) for e in m['entities']] + ['-', '-']
        o.append('| %s | %d | %s | %s / %s | %s | %s | %s | %s |' % (m['name'], m['mate_id'], m['type'], m.get('alignment'), m.get('alignment_geometric') or '-',
                 v, {True: 'ok', False: 'FAIL', None: '-'}[m.get('geometric_check')], es[0], '<br>---<br>'.join(es[1:len(m['entities'])]) or '-'))
    return '\n'.join(o) + '\n'


def run(root, out_dir):
    res = {}
    for a in ('rvrn 2.0', 'RVRN', 'Micro slx v1.0'):
        r = decode_asm_mates(os.path.join(root, a + '.SLDASM'), out_dir)
        r['stats'] = stats(r)
        json.dump(r, open(os.path.join(out_dir, a + '.mates_full.json'), 'w'), indent=1)
        open(os.path.join(out_dir, a + '.mates_full.md'), 'w').write(to_md(r))
        res[a] = r['stats']
    return res


if __name__ == '__main__':
    import sys
    print(json.dumps(run(sys.argv[1], sys.argv[2]), indent=1))
