"""Round-2 feature parameter inference.

Most feature parameters are *inferred* by combining three decoded sources
rather than read from the (undecoded) moExtrusion_c / moEndSpec_c layouts:
  * Keywords dims (values),
  * the number of dimension-driven end-spec blocks in the feature's stream
    region (marker FF FF 00 00 03 FF*4 00*4 00 00 80 BF, one per blind/offset
    direction; zero for Through-All / Up-To-* end conditions),
  * the B-rep: cap faces created by the feature, measured along the sketch
    normal from the sketch origin -> blind / mid-plane / direction sign.
"""
import math
import re

from . import sketch as SK

ENDSPEC = re.compile(re.escape(b'\xff\xff\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x80\xbf'))


def _mm(raw):
    m = re.search(r'(-?\d+(?:\.\d+)?)\s*$', raw)
    return float(m.group(1)) / 1000 if m and '°' not in raw else None


def feature_regions(d, features):
    pos = []
    for f in features:
        if not f['name']:
            continue
        p = SK.cstring_positions(d, f['name'])
        if p:
            pos.append((p[0], f))
    pos.sort(key=lambda x: x[0])
    return [(f, p, pos[k + 1][0] if k + 1 < len(pos) else len(d)) for k, (p, f) in enumerate(pos)]


def infer(d, result):
    feats = result['features']
    sk_by_name = {s['name']: s for s in result['sketches']}
    faces = result['faces']
    out = {}
    for f, p, e in feature_regions(d, feats):
        t = (f['type'] + ' ' + f['name']).lower()
        rec = {}
        if 'extru' in t:
            n = len(ENDSPEC.findall(d, p, e))
            depth_dims = [(k, _mm(v)) for k, v in f['dims'] if _mm(v) is not None]
            rec['dimensioned_end_specs'] = n
            rec['end_condition_class'] = ('dimensioned (Blind / Offset / Mid-Plane)' if n else
                                          'non-dimensioned (Through All / Up To Next / Up To Vertex|Surface)')
            rec['two_directions'] = n >= 2
            sk = None
            for c in f['children']:
                for s in result['sketches']:
                    if s.get('keywords_id') == c:
                        sk = s
            if sk is None:
                sk = next((s for s in result['sketches'] if f['name'] in s['used_by']), None)
            if sk and sk.get('placement'):
                T = sk['placement']['transform_rows_x_y_z_t']
                N, O = T[6:9], T[9:12]
                caps = []
                for fc in faces:
                    if f['id'] in fc['feature_ids_by_time'] and fc['surface_type'] == 'plane' and fc['params']:
                        nn = fc['params']['normal']
                        if abs(abs(sum(a * b for a, b in zip(nn, N))) - 1) < 1e-6:
                            pt = fc['params']['point']
                            caps.append(round(sum((pt[k] - O[k]) * N[k] for k in range(3)), 7))
                caps = sorted(set(caps))
                rec['sketch'] = sk['name']
                rec['cap_offsets_along_sketch_normal_mm'] = [round(c * 1000, 4) for c in caps]
                if depth_dims:
                    dd = depth_dims[0][1]
                    guess = []
                    for c in caps:
                        if abs(abs(c) - dd) < 1e-6:
                            guess.append('blind %s' % ('+N' if c > 0 else '-N'))
                        elif abs(abs(c) - dd / 2) < 1e-6:
                            guess.append('mid-plane')
                    rec['depth_check'] = guess or ['caps do not match D (offset / up-to / consumed)']
                rec['placement_confidence'] = sk['placement']['confidence']
        if 'fillet' in t or 'chamfer' in t:
            own = [k for k, fc in enumerate(faces) if fc['feature_first'] == f['id']]
            radii = sorted({round(fc['params']['radius'] * 1000, 4) for k, fc in enumerate(faces)
                            if k in own and fc['params'] and 'radius' in fc['params']})
            rec['created_faces'] = own
            rec['created_face_radii_mm'] = radii
            rec['adjacent_faces'] = sorted({a for k in own for a in faces[k].get('adjacent_faces', []) if a not in own})
            rec['note'] = 'edge set ~= edges between created_faces and adjacent_faces (the original edges are consumed)'
        if 'pattern' in t or 'mirror' in t:
            rec['dims'] = f['dims']
            rec['note'] = 'count/spacing from Keywords dims only; seed features/mirror plane not decoded'
        if rec:
            out[f['id']] = dict(name=f['name'], type=f['type'], **rec)
    return out


def ref_planes(d, features):
    """First non-identity orthonormal block in each Plane feature's region (low confidence)."""
    out = []
    for f, p, e in feature_regions(d, features):
        if f['type'].lower() not in ('plane', 'refplane') or f['name'] in ('Front Plane', 'Top Plane', 'Right Plane'):
            continue
        blocks = [b for b in SK._orth_blocks(d, p, min(e, p + 20000)) if tuple(b[1][:9]) != SK.IDENTITY[:9] or any(b[1][9:])]
        out.append({'name': f['name'], 'dims': f['dims'],
                    'transform_rows_x_y_n_t': blocks[0][1] if blocks else None,
                    'n_candidates': len(blocks), 'confidence': 'low'})
    return out
