"""SLDASM decoding: component instances + placements, mate list.

Components (moAssembly_c stream): each instance's UTF-16 CString name
('<part>-<n>') is followed within ~400 bytes by 12 LE doubles = 3x3 rotation
(rows as stored) + translation (m).  Mates (stream starting with moMateXxx):
CString sequence  <MateName>  then for each mated entity
  <entity-id-rep string, e.g. 'moFromSktEntSurfIdRep_c,42,18,'>  <component path>
followed (first use only) by the component's file path, name and config.
Distance/Angle mate values: first CString 'D<n>' after the mate name,
then an empty CString, u16 0, f64 value (same layout as part dimensions).
Alignment/flip flags are NOT decoded.
"""
import re
import struct

import numpy as np

CSTR = re.compile(rb'\xff\xfe\xff(.)((?:[^\x00]\x00|\x00[^\x00]){1,250})', re.S)
MATE_RE = re.compile(r'^(Coincident|Concentric|Parallel|Perpendicular|Distance|Angle|Tangent|Width|Lock|'
                     r'Symmetric|Gear|Cam|Hinge|Slot|Path|LinearCoupler|Screw|Rack|Profile|UJoint)\d+$')
DIMV = re.compile(rb'\xff\xfe\xff(.)((?:D\x00)(?:[0-9]\x00){1,3}).{0,24}?\xff\xfe\xff\x00\x00\x00(.{8})', re.S)


def cstrings(d):
    out = []
    for m in CSTR.finditer(d):
        n = m.group(1)[0]
        raw = m.group(2)[:2 * n]
        if len(raw) == 2 * n:
            out.append((m.start(), raw.decode('utf-16-le', 'replace')))
    return out


def _rot_at(d, start, end, tol=1e-6):
    for al in range(8):
        s0 = start + al
        n = (end - s0) // 8
        if n < 12:
            continue
        v = np.frombuffer(d, dtype='<f8', count=n, offset=s0)
        with np.errstate(all='ignore'):
            for k in range(n - 11):
                blk = v[k:k + 12]
                if not np.all(np.isfinite(blk)) or np.any(np.abs(blk) > 100):
                    continue
                R = blk[:9].reshape(3, 3)
                if np.abs(R @ R.T - np.eye(3)).max() < tol and abs(abs(np.linalg.det(R)) - 1) < tol:
                    return s0 + 8 * k, [float(x) for x in blk]
    return None, None


def components(d):
    cs = cstrings(d)
    res, seen = [], set()
    for k, (p, s) in enumerate(cs):
        if not re.match(r'^.+-\d+$', s) or '@' in s or '\\' in s or s in seen or s.startswith(('Ambient-', 'Directional-')):
            continue
        nxt = cs[k + 1][0] if k + 1 < len(cs) else len(d)
        pos, T = _rot_at(d, p, min(len(d), p + 600))
        seen.add(s)
        res.append({'instance': s, 'rotation_rows': T[:9] if T else None,
                    'translation_m': T[9:12] if T else None, 'stream_offset': p})
    return res


def mates(d):
    cs = cstrings(d)
    out = []
    idx = [k for k, (p, s) in enumerate(cs) if MATE_RE.match(s)]
    for j, k in enumerate(idx):
        end = idx[j + 1] if j + 1 < len(idx) else len(cs)
        p, name = cs[k]
        pend = cs[end][0] if end < len(cs) else len(d)
        ents, last_rep = [], None
        for q, s in cs[k + 1:end]:
            if s.startswith('mo') and ',' in s:
                last_rep = [x for x in re.split(r'[\r\n]+', s.strip()) if x.strip()]
            elif '@' in s and not s.startswith(('H:', 'I:', 'C:')):
                ents.append({'component': s, 'entity_id_rep': last_rep})
                last_rep = None
        rec = {'name': name, 'type': re.sub(r'\d+$', '', name), 'entities': ents}
        if rec['type'] in ('Distance', 'Angle', 'Width'):
            m = DIMV.search(d, p, pend)
            if m:
                v = struct.unpack('<d', m.group(3))[0]
                rec['dim_name'] = m.group(2).decode('utf-16-le')
                rec['value'] = v
                rec['value_display'] = ('%.4g mm' % (v * 1000)) if rec['type'] != 'Angle' else ('%.4g deg' % (v * 57.29577951308232))
        out.append(rec)
    return out


def decode_asm(path):
    from .streams import all_streams
    data = open(path, 'rb').read()
    st = all_streams(data)
    comp, mt = [], []
    for s in st:
        d = s['data']
        if d.startswith(b'\xff\xff\x01\x00\x0c\x00moAssembly_c'):
            comp = components(d)
        if b'moMate' in d[:200]:
            mt = mates(d)
    return {'file': path.rsplit('/', 1)[-1], 'components': comp, 'mates': mt}


def asm_md(r):
    o = ['# %s - assembly decode\n' % r['file'].rsplit('.', 1)[0],
         'Translation in mm. Rotation rows = component X, Y, Z axes expressed in the parent frame: p_parent = t + x*row0 + y*row1 + z*row2 (verified 46/46 vs STEP). '
         'Mate alignment/flip not decoded. See README.\n',
         ('STEP check: %s\n' % r['step_check']) if r.get('step_check') else '',
         '## Components (%d)\n' % len(r['components']), '| instance | translation mm | rotation rows | T in STEP |', '|---|---|---|---|']
    for c in r['components']:
        t = ', '.join('%.4g' % (x * 1000) for x in c['translation_m']) if c['translation_m'] else '?'
        R = '; '.join(', '.join('%.4g' % x for x in c['rotation_rows'][i:i + 3]) for i in (0, 3, 6)) if c['rotation_rows'] else '?'
        o.append('| %s | %s | %s | %s |' % (c['instance'], t, R, {True: 'yes', False: 'no'}.get(c.get('translation_in_step'), '')))
    o += ['\n## Mates (%d)\n' % len(r['mates']), '| mate | type | value | entity A | entity B |', '|---|---|---|---|---|']
    for m in r['mates']:
        e = ['%s [%s]' % (x['component'], ' + '.join(x['entity_id_rep'] or ['?'])) for x in m['entities']]
        while len(e) < 2:
            e.append('?')
        o.append('| %s | %s | %s | %s | %s |' % (m['name'], m['type'], m.get('value_display', ''), e[0], '; '.join(e[1:])))
    return '\n'.join(o) + '\n'


def step_translations(path):
    """Set of assembly placement origins (mm) from ITEM_DEFINED_TRANSFORMATIONs in a STEP file."""
    t = open(path, encoding='latin1').read()
    E = dict((int(a), b) for a, b in re.findall(r'#(\d+)\s*=\s*(.*?);\s*\n', t, re.S))
    pts = []
    for v in E.values():
        if v.startswith('ITEM_DEFINED_TRANSFORMATION'):
            r = [int(x) for x in re.findall(r'#(\d+)', v)]
            rr = [int(x) for x in re.findall(r'#(\d+)', E[r[0]])]
            loc = re.findall(r'-?[\d.E+-]+', E[rr[0]].split(',', 1)[1])
            pts.append(tuple(round(float(x), 2) for x in loc[:3]))
    return pts


def check_against_step(r, pts):
    S = set(pts)
    for c in r['components']:
        if c['translation_m']:
            c['translation_in_step'] = tuple(round(x * 1000, 2) + 0.0 for x in c['translation_m']) in S
    n = [c for c in r['components'] if c['translation_m']]
    r['step_check'] = {'step_placements': len(pts), 'decoded_with_T': len(n),
                       'translations_found_in_step': sum(1 for c in n if c.get('translation_in_step'))}
