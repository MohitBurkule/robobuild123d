"""Sketch-plane transform (item SKETCH-PLANE TRANSFORM).

Findings (RV17, RV01, RV23, RV09):
* The sketch plane is stored as a 12-double LE block (3x3 orthonormal rows +
  translation, metres) followed by f64 1.0 (scale).  The block is the
  MODEL->SKETCH transform: q = R (p - t).  The sketch->model map is therefore
  p = t + x*R[:,0] + y*R[:,1]  (columns of R; normal = R[:,2]), i.e. the
  inverse of how sketch.py reads it.  For the symmetric rotations common on
  Front-plane parts (identity, diag(-1,1,-1)) the two readings coincide, which
  is why the old reading looked right on RV17; RV01 side-plane sketches
  (rotations about Y) only reproduce XT cylinders with the inverse.
* Record classes, by the bytes just before the block:
    plane_rec     ... <f64 s> 01 [block] 1.0 00 <4 f64>   (s = -1.0/0: plane on a face)
    refplane_rec  ... 68 42 00 00 <u32 id> <u32 stamp> 00*6 01 [block] 1.0
                  (reference-plane object; precedes moContour)
    annotation    ... 01 00 01 [block]   (dimension/annotation planes; NOT the sketch plane)
    view_identity ... 39 C0 01 00*5 [identity]   (display transform; NOT the plane)
    identity_default: no record -> Front plane / model frame.
* The face reference (which XT face the plane_rec came from) is not decoded.
"""
import json
import math
import os
import pickle
import sys

import numpy as np

from . import streams as S
from . import sketch as SK
from .xt import XT

TOL = 2e-6
GOOD = ('plane_rec', 'refplane_rec', 'identity_default')


def classify(f, o):
    if o is None:
        return 'identity_default'
    if f[o - 3:o] == b'\x01\x00\x01':
        return 'annotation'
    if f[o - 1] == 1:
        return 'refplane_rec' if b'\x68\x42' in f[o - 26:o - 8] else 'plane_rec'
    if b'\x39\xc0\x01' in f[o - 8:o]:
        return 'view_identity'
    return 'other'


def stored_to_sketch2model(T):
    """Stored block (model->sketch, rows R, t) -> sketch->model in sketch.py's row form."""
    R = np.array(T[:9], float).reshape(3, 3)
    t = np.array(T[9:12], float)
    return tuple(float(v) + 0.0 for v in R.T.ravel()) + tuple(float(v) + 0.0 for v in -(R @ t))


def surf_lists(surfs):
    pl = [s['params'] for s in surfs if s['type'] == 'plane' and s.get('params')]
    cy = [s['params'] for s in surfs if s['type'] == 'cylinder' and s.get('params')]
    return pl, cy


def check(T, sk, pl, cy):
    """T in sketch->model row form. Returns dict of hit counts."""
    R = np.array(T[:9]).reshape(3, 3)
    t = np.array(T[9:12])
    n = R[2]
    w = lambda p: t + p[0] * R[0] + p[1] * R[1]
    radii = [q['radius'] for q in cy]
    r = dict(arcs=0, arcs_hit=0, arcs_with_radius_in_xt=0, lines=0, lines_hit=0)
    for e in sk['entities']:
        if e.get('type') in ('circle', 'arc') and e.get('radius') and e.get('centre') and None not in e['centre']:
            r['arcs'] += 1
            r['arcs_with_radius_in_xt'] += any(abs(x - e['radius']) < TOL for x in radii)
            c = w(e['centre'])
            for q in cy:
                ax = np.array(q['axis'])
                d = c - np.array(q['point'])
                if (abs(abs(ax @ n) - 1) < 1e-6 and np.linalg.norm(d - (d @ ax) * ax) < TOL
                        and abs(q['radius'] - e['radius']) < TOL):
                    r['arcs_hit'] += 1
                    break
        elif e.get('type') == 'line' and e.get('start') and e.get('end') and None not in e['start'] + e['end']:
            a, b = w(e['start']), w(e['end'])
            if np.linalg.norm(a - b) < 1e-7:
                continue
            r['lines'] += 1
            for q in pl:
                nn = np.array(q['normal'])
                o = q['offset_along_normal']
                if abs(nn @ n) < 1e-6 and abs(a @ nn - o) < TOL and abs(b @ nn - o) < TOL:
                    r['lines_hit'] += 1
                    break
    return r


def load_part(path):
    data = open(path, 'rb').read()
    feat, xts = None, []
    for s in S.all_streams(data):
        c = S.classify(s)
        if c == 'parasolid':
            xts.append(XT(s['data']))
        elif c == 'features' and (feat is None or len(s['data']) > len(feat)):
            feat = s['data']
    main = max(xts, key=lambda x: len(x.faces)) if xts else None
    return feat, (list(main.surfaces.values()) if main else [])


def decode_part(sldprt, decoded_json):
    j = json.load(open(decoded_json))
    f, surfs = load_part(sldprt)
    pl, cy = surf_lists(surfs)
    regs = {r[0]: r for r in SK.sketch_regions(f, [s['name'] for s in j['sketches']])}
    out, tot = [], dict(arcs=0, arcs_hit=0, arcs_with_radius_in_xt=0, lines=0, lines_hit=0)
    for sk in j['sketches']:
        if sk['name'] not in regs:
            continue
        _, a, b = regs[sk['name']]
        rows = []
        for o, T in [(None, SK.IDENTITY)] + SK._orth_blocks(f, max(0, a - 1600), b):
            k = classify(f, o)
            if k not in GOOD:
                continue
            M = stored_to_sketch2model(T)
            c = check(M, sk, pl, cy)
            lenient = SK.score_transform(M, sk['points'], sk['entities'], surfs)
            rows.append(((c['arcs_hit'], c['lines_hit'], lenient, GOOD[::-1].index(k), -(abs(o - a) if o else 0)), o, k, T, M, c))
        rows.sort(key=lambda r: r[0], reverse=True)
        key, o, k, T, M, c = rows[0]
        ties = sum(1 for r in rows if r[0][:3] == key[:3] and r[4][6:9] != M[6:9])
        R = np.array(M[:9]).reshape(3, 3)
        conf = ('high' if c['arcs_hit'] and ties == 0 else
                'medium' if (c['arcs_hit'] or c['lines_hit']) and ties == 0 else 'low')
        for kk in tot:
            tot[kk] += c[kk]
        out.append({'sketch': sk['name'], 'record_class': k,
                    'record_offset': o, 'record_rel_to_sketch_name': (o - a) if o is not None else None,
                    'stored_block_model_to_sketch': [round(v, 12) for v in T],
                    'origin_m': [round(v, 12) for v in M[9:12]], 'x_axis': [round(v, 12) for v in R[0]],
                    'y_axis': [round(v, 12) for v in R[1]], 'normal': [round(v, 12) for v in R[2]],
                    'validation': c, 'n_alternatives_tied_other_normal': ties, 'confidence': conf})
    return {'part': j['file'], 'convention': 'p_model = origin + x*x_axis + y*y_axis (stored block is its inverse)',
            'totals': tot, 'sketches': out}


def main(argv):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for name in argv:
        res = decode_part(os.path.join(root, 'revdev', name + '.SLDPRT'), os.path.join(root, 'decoded', name + '.json'))
        p = os.path.join(root, 'decoded', name + '.sketchplane.json')
        with open(p, 'w') as fh:
            json.dump(res, fh, indent=1)
        print(name, res['totals'])


if __name__ == '__main__':
    main(sys.argv[1:])
