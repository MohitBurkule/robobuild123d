"""Sketch entity decoder for the SolidWorks feature stream (moXxx_c MFC archive).

We do not reimplement MFC CArchive.  Sketch entities are found by a fixed
17-byte record marker that precedes every sketch point / segment record:

    FF FF 1F 00 03  <8 bytes, usually FF*8>  00 00 80 BF      (f32 -1.0)

The 8 bytes before the marker are <u32 a><u32 id>.  Relative to the end of
the marker (i), field R = i+47:

  point   : u16 @R == 0x001E ; f64 x @R+2, f64 y @R+10   (sketch-local metres)
  ext pt  : (points with an external reference, e.g. projected vertex/origin)
            same 00 00 F0 3F + 8x00 + 1E 00 + x + y pattern later in the record
  segment : u16 start @R, u16 end @R+2, u16 flag @R+4, f64 -1.0 @R+8,
            u16 kind @R+16 (0 = line, 1 = arc/circle), u16 centre @R+20 (arcs)

Segment point references are 0-based indices into the sketch's point records
in file order (verified: arc start/end equidistant from centre, lines
horizontal/vertical where expected, XT cylinder radii reproduced).
Sketch boundaries come from the sketch's UTF-16 CString name (FF FE FF len).
"""
import math
import re
import struct

MARK = re.compile(rb'\xff\xff\x1f\x00\x03.{8}\x00\x00\x80\xbf', re.S)
PT_PAT = b'\x00\x00\xf0\x3f' + b'\x00' * 8 + b'\x1e\x00'
NEG1 = struct.pack('<d', -1.0)


def cstring_positions(d, name):
    enc = name.encode('utf-16-le')
    if len(name) > 254:
        return []
    pat = b'\xff\xfe\xff' + bytes([len(name)]) + enc
    return [m.start() for m in re.finditer(re.escape(pat), d)]


def sketch_regions(d, sketch_names):
    """[(name, start, end)] using the first CString occurrence of each name."""
    found = []
    for n in sketch_names:
        p = cstring_positions(d, n)
        if p:
            found.append((p[0], n))
    found.sort()
    out = []
    for k, (p, n) in enumerate(found):
        e = found[k + 1][0] if k + 1 < len(found) else len(d)
        out.append((n, p, e))
    return out


def _orth_blocks(d, start, end):
    """All 12-double LE blocks (3x3 orthonormal rows + translation) in a range."""
    import numpy as np
    res, seen = [], set()
    for al in range(8):
        s0 = start + al
        n = (end - s0) // 8
        if n < 12:
            continue
        v = np.frombuffer(d, dtype='<f8', count=n, offset=s0)
        with np.errstate(all='ignore'):
            ok = np.isfinite(v) & (np.abs(v) <= 10)
            sq = np.where(ok, v, 0.0) ** 2
            nrm = sq[:-2] + sq[1:-1] + sq[2:]
            unit = (np.abs(nrm - 1) < 1e-9) & ok[:-2] & ok[1:-1] & ok[2:]
        m = len(v) - 11
        if m <= 0:
            continue
        cand = np.nonzero(unit[:m] & unit[3:m + 3] & unit[6:m + 6])[0]
        for k in cand:
            blk = v[k:k + 12]
            if not np.all(np.isfinite(blk)) or np.any(np.abs(blk) > 10):
                continue
            R = blk[:9].reshape(3, 3)
            if np.abs(R @ R.T - np.eye(3)).max() > 1e-9:
                continue
            t = tuple(round(float(x), 12) + 0.0 for x in blk)
            if t not in seen:
                seen.add(t)
                res.append((s0 + 8 * int(k), t))
    res.sort()
    return res


def parse_records(d, start, end):
    marks = [m for m in MARK.finditer(d, start, end)]
    points, segs, other = [], [], []
    for k, m in enumerate(marks):
        s, i = m.start(), m.end()
        e = marks[k + 1].start() - 8 if k + 1 < len(marks) else min(end, i + 600)
        a, rid = struct.unpack_from('<2i', d, s - 8)
        R = i + 47
        tag = struct.unpack_from('<H', d, R)[0]
        if tag == 0x1E:
            x, y = struct.unpack_from('<2d', d, R + 2)
            points.append({'rec_id': rid, 'x': x, 'y': y, 'ext': False, 'pos': s})
            continue
        if d[R + 8:R + 16] == NEG1:
            st, en, fl = struct.unpack_from('<3H', d, R)
            kind = struct.unpack_from('<H', d, R + 16)[0]
            cen = struct.unpack_from('<H', d, R + 20)[0]
            segs.append({'rec_id': rid, 'start': st, 'end': en, 'flag': fl, 'kind': kind,
                         'centre': cen if kind == 1 else None, 'pos': s})
            continue
        j = d.find(PT_PAT, i, e)
        if j > 0:
            x, y = struct.unpack_from('<2d', d, j + len(PT_PAT))
            points.append({'rec_id': rid, 'x': x, 'y': y, 'ext': True, 'pos': s})
        else:
            points.append({'rec_id': rid, 'x': None, 'y': None, 'ext': True, 'pos': s})
            other.append(s)
    return points, segs, other


def _p(points, i):
    if i is None or i >= len(points) or points[i]['x'] is None:
        return None
    return (points[i]['x'], points[i]['y'])


def build_entities(points, segs):
    ents = []
    for g in segs:
        A, B = _p(points, g['start']), _p(points, g['end'])
        e = {'rec_id': g['rec_id'], 'start_idx': g['start'], 'end_idx': g['end'], 'flag': g['flag'], 'kind_code': g['kind']}
        if g['kind'] == 0:
            e['type'] = 'line'
            if A and B:
                e.update(start=A, end=B, length=math.hypot(B[0] - A[0], B[1] - A[1]))
        elif g['kind'] == 1:
            C = _p(points, g['centre'])
            e['centre_idx'] = g['centre']
            full = g['start'] == g['end']
            e['type'] = 'circle' if full else 'arc'
            if A and C:
                r1 = math.hypot(A[0] - C[0], A[1] - C[1])
                e.update(centre=C, start=A, radius=r1)
                if B and not full:
                    r2 = math.hypot(B[0] - C[0], B[1] - C[1])
                    e['end'] = B
                    e['radius_mismatch'] = abs(r1 - r2)
                    a1 = math.atan2(A[1] - C[1], A[0] - C[0])
                    a2 = math.atan2(B[1] - C[1], B[0] - C[0])
                    e['sweep_ccw_deg'] = math.degrees((a2 - a1) % (2 * math.pi))
        else:
            e['type'] = 'unknown_kind_%d' % g['kind']
            if A:
                e['start'] = A
            if B:
                e['end'] = B
        ents.append(e)
    return ents


def match_dims(dims, points, ents, tol=1e-6):
    """Tie Keywords dimension values (mm / deg strings) to geometry by value."""
    out = []
    pts = [(i, (p['x'], p['y'])) for i, p in enumerate(points) if p['x'] is not None]
    for name, raw in dims:
        m = re.search(r'(-?\d+(?:\.\d+)?)\s*(°)?\s*$', raw)
        rec = {'dim': name, 'value': raw, 'matches': []}
        if not m:
            out.append(rec)
            continue
        v = float(m.group(1))
        if m.group(2):
            rec['note'] = 'angular: not matched'
            out.append(rec)
            continue
        vm = v / 1000.0
        diam = 'DIAM' in raw.upper() or 'Ø' in raw
        for k, e in enumerate(ents):
            if 'radius' in e:
                if abs(2 * e['radius'] - vm) < tol:
                    rec['matches'].append(('entity', k, e['type'], 'diameter'))
                if abs(e['radius'] - vm) < tol and not diam:
                    rec['matches'].append(('entity', k, e['type'], 'radius'))
            if e.get('length') is not None and abs(e['length'] - vm) < tol and not diam:
                rec['matches'].append(('entity', k, 'line', 'length'))
        if not diam and len(rec['matches']) == 0:
            for a in range(len(pts)):
                for b in range(a + 1, len(pts)):
                    (i, P), (j, Q) = pts[a], pts[b]
                    if abs(abs(P[0] - Q[0]) - vm) < tol and abs(P[1] - Q[1]) > tol:
                        rec['matches'].append(('points', i, j, 'dx'))
                    if abs(abs(P[1] - Q[1]) - vm) < tol and abs(P[0] - Q[0]) > tol:
                        rec['matches'].append(('points', i, j, 'dy'))
                    if abs(math.hypot(P[0] - Q[0], P[1] - Q[1]) - vm) < tol:
                        rec['matches'].append(('points', i, j, 'dist'))
            rec['matches'] = rec['matches'][:12]
        out.append(rec)
    return out


def to_world(T, x, y):
    R0, R1, t = T[0:3], T[3:6], T[9:12]
    return tuple(t[k] + x * R0[k] + y * R1[k] for k in range(3))


def score_transform(T, points, ents, surfaces, tol=1e-6):
    """How well a candidate sketch->model transform agrees with the XT B-rep."""
    s = 0
    planes = [v['params'] for v in surfaces if v['type'] == 'plane' and 'params' in v]
    cyls = [v['params'] for v in surfaces if v['type'] in ('cylinder', 'cone') and 'params' in v]
    for p in points:
        if p['x'] is None:
            continue
        w = to_world(T, p['x'], p['y'])
        if any(abs(sum(w[k] * pl['normal'][k] for k in range(3)) - pl['offset_along_normal']) < tol for pl in planes):
            s += 1
    for e in ents:
        if 'radius' in e and 'centre' in e:
            c = to_world(T, *e['centre'])
            for cy in cyls:
                d = [c[k] - cy['point'][k] for k in range(3)]
                ax = cy['axis']
                along = sum(d[k] * ax[k] for k in range(3))
                perp = math.sqrt(max(0.0, sum(x * x for x in d) - along * along))
                if perp < tol and abs(cy['radius'] - e['radius']) < tol:
                    s += 5
                    break
    return s


def arc_hits(T, ents, surfaces, tol=1e-6):
    return score_transform(T, [], ents, surfaces, tol) // 5


IDENTITY = (1.0, 0, 0, 0, 1.0, 0, 0, 0, 1.0, 0, 0, 0)


def decode_sketches(d, sketch_names, surfaces=None):
    res = []
    for name, start, end in sketch_regions(d, sketch_names):
        points, segs, other = parse_records(d, start, end)
        ents = build_entities(points, segs)
        sk = {'name': name, 'stream_offset': start, 'points': points, 'entities': ents}
        cands = [(None, IDENTITY)] + _orth_blocks(d, start, end)
        if surfaces is not None and (points or ents):
            def prio(c):
                pos, T = c
                facepln = pos is not None and d[pos - 9:pos] == NEG1 + b'\x01'
                return (facepln, pos is not None and T != IDENTITY and tuple(T[:9]) != IDENTITY[:9], pos is not None)
            scored = []
            for k, c in enumerate(cands):
                scored.append((score_transform(c[1], points, ents, surfaces), prio(c), -k, c))
            scored.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
            best = scored[0]
            ties = [x[3][1] for x in scored if x[0] == best[0]]
            sk['placement'] = {'transform_rows_x_y_z_t': best[3][1], 'stream_offset': best[3][0],
                               'face_plane_signature': best[1][0], 'score': best[0],
                               'n_candidates': len(cands), 'n_tied': len(set(ties)),
                               'tied_alternatives': list(dict.fromkeys(ties))[1:4]}
            ah = arc_hits(best[3][1], ents, surfaces)
            narcs = sum(1 for e in ents if 'radius' in e)
            sk['placement']['arcs_matching_xt_cylinders'] = '%d/%d' % (ah, narcs)
            sk['placement']['confidence'] = ('high' if ah and len(set(ties)) == 1 else
                                             'medium' if len(set(ties)) == 1 and best[0] > 0 else 'low')
        res.append(sk)
    return res
