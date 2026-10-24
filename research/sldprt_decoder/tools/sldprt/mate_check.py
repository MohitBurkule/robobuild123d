"""Check decoded assembly-mate entities (item_mates.py) against the API assembly dump.

    python3 -I -m sldprt.mate_check <revdev> <dumps_v2> <decoded> [asm name]

Per ENT line of dumps_v2/<asm>.asmdump.txt (component path, params = point, dir, radius):
  geometry   decoded solve-table point / dir / radius equal the dump params (assembly frame)
  component  decoded component instance (stored transform matched to the current instance)
             equals the dump's top-level component; for sub-assembly paths also the leaf part
  face       the entity-id-rep CString names (feature id, ...) of the component *part*: the feature
             exists in the part dump and owns a FACE whose geometry, mapped into the part frame by
             the component XFORM, matches the ENT geometry
"""
import json
import math
import os
import re
import sys
from collections import Counter

from . import answer_key as AK


def parse_asmdump(path):
    comps, mates, cur, m = {}, [], None, None
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.rstrip('\n')
        if line.startswith('COMP '):
            name, rest = line[5:].split(' | ', 1)
            f = re.search(r'file=([^|]*)', rest).group(1).strip()
            cur = comps[name.strip()] = {'file': f, 'xform': None}
        elif line.startswith('  XFORM') and cur is not None:
            cur['xform'] = [float(x) for x in line.split()[1].split(',') if x]
        elif line.startswith('MATE '):
            p = line[5:].split(' | ')
            m = {'name': p[0].strip(), 'type': int(p[1].split('=')[1]), 'ents': []}
            mates.append(m)
            cur = None
        elif line.startswith('  ENT') and m is not None:
            g = re.match(r'\s+ENT (\d+) comp=(.*) reftype=(\d+) params=(.*)$', line)
            if g:
                pr = [float(x) for x in g.group(4).split(',') if x]
                m['ents'].append({'i': int(g.group(1)), 'comp': g.group(2).strip(), 'reftype': int(g.group(3)), 'params': pr})
    return comps, mates


def _close(a, b, tol):
    return a is not None and b is not None and len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def _par(u, v, tol=1e-6):
    c = sum(x * y for x, y in zip(u, v))
    return abs(abs(c) - 1) < tol


def to_part(X, p, v):
    """assembly -> component frame. SolidWorks ArrayData: rows of R (component axes in asm), then t;
    p_asm = p_loc . R + t (row-vector convention)."""
    R = [X[0:3], X[3:6], X[6:9]]
    t = X[9:12]
    q = [p[i] - t[i] for i in range(3)]
    loc = [sum(R[j][i] * 0 for j in range(3)) for i in range(3)]
    loc = [sum(R[i][j] * q[j] for j in range(3)) for i in range(3)]
    dv = [sum(R[i][j] * v[j] for j in range(3)) for i in range(3)]
    return loc, dv


def face_matches(face, p, v, r, tol=2e-6):
    if face['kind'] == 'plane':
        n, o = face['n'], face['o']
        return _par(n, v) and abs(sum((p[i] - o[i]) * n[i] for i in range(3))) < tol
    if face['kind'] == 'cyl':
        a, o = face['ax'], face['o']
        if not _par(a, v) or (r and abs(face['r'] - r) > tol):
            return False
        w = [p[i] - o[i] for i in range(3)]
        t = sum(w[i] * a[i] for i in range(3))
        return math.sqrt(max(0.0, sum((w[i] - t * a[i]) ** 2 for i in range(3)))) < tol
    return False


FACE_RE = re.compile(r'\s+FACE (\w+) (.*)$')


def part_faces(dump_path):
    """feature id -> [face dicts] from a part dump (FACE lines under FEATURE)."""
    out, fid = {}, None
    vec = lambda s, k: [float(x) for x in re.search(k + r'=\(([^)]*)\)', s).group(1).split(',')]
    for line in open(dump_path, encoding='utf-8', errors='replace'):
        if line.startswith('FEATURE'):
            fid = int(re.search(r'id=(-?\d+)', line).group(1))
        g = FACE_RE.match(line)
        if g and fid is not None:
            k, s = g.group(1), g.group(2)
            try:
                if k == 'plane':
                    f = {'kind': 'plane', 'n': vec(s, 'n'), 'o': vec(s, 'o')}
                elif k == 'cyl':
                    f = {'kind': 'cyl', 'o': vec(s, 'o'), 'ax': vec(s, 'ax'), 'r': float(re.search(r' r=([^ ]*)', s).group(1))}
                else:
                    f = {'kind': k}
            except Exception:
                continue
            out.setdefault(fid, []).append(f)
    return out


def rep_feature_id(rep):
    """'moFromSktEntSurfIdRep_c,42,18,' -> 42 (the feature that made the face, in the component part)."""
    p = rep.split(',')
    try:
        return int(p[1])
    except (IndexError, ValueError):
        return None


def check(asm, dumps, decoded):
    comps, mates = parse_asmdump(os.path.join(dumps, asm + '.asmdump.txt'))
    dec = json.load(open(os.path.join(decoded, asm + '.mates_full.json')))
    byname = {m['name']: m for m in dec['mates']}
    acc = Counter()
    fcache = {}
    for m in mates:
        dm = byname.get(m['name'])
        acc[('mate', 'found', dm is not None)] += 1
        if dm is None:
            continue
        for e in m['ents']:
            if e['i'] >= len(dm['entities']):
                acc[('ent', 'decoded', False)] += 1
                continue
            de = dm['entities'][e['i']]
            acc[('ent', 'decoded', True)] += 1
            g = de.get('geometry_asm') or {}
            p, v, r = e['params'][0:3], e['params'][3:6], e['params'][6] if len(e['params']) > 6 else 0
            gv = g.get('dir')
            acc[('geometry', 'point+dir', _close(g.get('point'), p, 1e-7) and gv is not None and _par(gv, v))] += 1
            if r:
                acc[('geometry', 'radius', abs((g.get('radius_candidate') or 0) - r) < 1e-9)] += 1
            top = e['comp'].split('/')[0]
            inst = de.get('instance_current') or []
            acc[('component', 'top-level instance (transform only, round 6)', inst == [top])] += 1
            if 'instance_resolved' in de:
                acc[('component', 'top-level instance (name / transform / rename)', de['instance_resolved'] == top)] += 1
            leaf = e['comp'].split('/')[-1]
            part = re.sub(r'-\d+$', '', leaf)
            cp = de.get('component_path', '')
            leaf_stored = re.sub(r'-\d+(@.*)?$', '', cp.split('/')[-1])
            acc[('component', 'leaf part name in stored path', leaf_stored.lower() in part.lower())] += 1
            # face via the entity-id-rep feature id
            c = comps.get(e['comp'])
            fdump = os.path.join(dumps, part + '.dump.txt')
            reps = de.get('entity_id_rep') or []
            if c is None or c['xform'] is None or not os.path.exists(fdump) or not reps:
                acc[('face', 'checkable', False)] += 1
                continue
            acc[('face', 'checkable', True)] += 1
            if fdump not in fcache:
                fcache[fdump] = part_faces(fdump)
            pf = fcache[fdump]
            lp, lv = to_part(c['xform'], p, v)
            fids = [rep_feature_id(x) for x in reps]
            if de.get('rep_features') is not None:
                pd = AK.parse(fdump)
                nm = {f.id: f.name for f in pd.features}
                acc[('face', 'decoded rep feature name = part dump feature name',
                     all(x['feature_name'] == nm.get(x['feature_id']) for x in de['rep_features']) and bool(de['rep_features']))] += 1
            ok = any(face_matches(f, lp, lv, r) for fid in fids if fid in pf for f in pf[fid])
            exists = any(fid in pf for fid in fids)
            acc[('face', 'rep feature id exists in part', exists)] += 1
            if exists:
                acc[('face', 'rep feature owns a face matching the ENT geometry', ok)] += 1
    return acc


def table(acc):
    rows = {}
    for (a, b, ok), n in acc.items():
        rows.setdefault((a, b), [0, 0])
        rows[(a, b)][1] += n
        if ok:
            rows[(a, b)][0] += n
    return {f'{a}.{b}': {'ok': v[0], 'n': v[1], 'pct': round(100 * v[0] / max(1, v[1]), 2)} for (a, b), v in sorted(rows.items())}


if __name__ == '__main__':
    revdev, dumps, decoded = sys.argv[1:4]
    asm = sys.argv[4] if len(sys.argv) > 4 else 'rvrn 2.0'
    print(json.dumps(table(check(asm, dumps, decoded)), indent=1))
