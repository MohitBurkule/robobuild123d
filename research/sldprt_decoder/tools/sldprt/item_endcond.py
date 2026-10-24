"""Extrude end-condition classification by measured extent (works off <part>.json).

For each Extrude/Cut feature F with an end_spec:
  n  = sketch normal (row z of sketch placement), s0 = sketch plane offset along n.
  side faces = faces carrying F's ATOM_ID whose surface is parallel to n
     (plane with normal _|_ n, cylinder/cone with axis || n).
  extent [a,b] = span of their edge-loop vertices along n (relative to s0).
  body [lo,hi] = span of all vertices along n.
Classes: blind (|b|or|a| == D, other end at 0), midplane (a == -b, b-a == D),
through_all (reaches body extreme on the far side, no D), up_to_surface (far end lies on a
planar face of another feature), offset_from_surface (far end = some plane +/- D).
"""
import json, os, sys, collections
import numpy as np
from .item_pattern import face_pts
from .mo_classes import num

TOL = 2e-5
# SolidWorks API swEndConditions_e (public enum) - the hypothesis tested here
SW_ENUM = {0: 'Blind', 1: 'ThroughAll', 2: 'UpToNext', 3: 'UpToVertex', 4: 'UpToSurface', 5: 'OffsetFromSurface', 6: 'MidPlane', 7: 'UpToBody', 9: 'ThroughAllBoth'}

def _dir_side(f, n):
    p = f.get('params') or {}
    if f['surface_type'] == 'plane' and 'normal' in p: return abs(np.dot(p['normal'], n)) < 1e-4
    if f['surface_type'] in ('cylinder', 'cone') and 'axis' in p: return abs(abs(np.dot(p['axis'], n)) - 1) < 1e-4
    return False

def classify(d, planes=None):
    """planes: optional <part>.sketchplane.json content (item_sketchplane, the corrected
    model->sketch inverse reading); it overrides sketch.py's placement, which is wrong for
    rotations about Y (RV01 side-plane sketches)."""
    faces = d['faces']; feats = {f['name']: f for f in d['features']}
    sk = {s['name']: dict(s) for s in d['sketches']}; kid = {f['id']: f['name'] for f in d['features']}
    for e in (planes or {}).get('sketches', []):
        if e['sketch'] in sk:
            sk[e['sketch']]['placement'] = {'transform_rows_x_y_z_t': list(e['x_axis']) + list(e['y_axis']) + list(e['normal']) + list(e['origin_m']),
                                            'confidence': e['confidence'], 'source': 'sketchplane.json'}
            if e.get('record_class') == 'identity_default':
                # no stored block: orientation = Front, but the sketch usually sits on a face whose
                # offset is not decoded -> do not trust s0 = 0 (RV01 Sketch18/20/23/26 lie at z=-8.5)
                sk[e['sketch']]['placement']['confidence'] = 'orientation_only'; kid = {f['id']: f['name'] for f in d['features']}
    L0 = [P for f in faces if len(P := face_pts(f))]
    if not L0:
        # no edge loops decoded: use planar cap offsets along cylinder axes (single-body parts)
        out = {}
        for name, specs in d.get('end_specs', {}).items():
            F = feats.get(name); D = [x / 1e3 for v in (F or {}).get('dims', []) if (x := num(v[1]))]
            ax = next((np.array(f['params']['axis']) for f in faces if 'axis' in (f.get('params') or {})), np.array([0, 0, 1.]))
            offs = sorted(np.dot(f['params']['point'], ax) for f in faces if f['surface_type'] == 'plane' and abs(abs(np.dot(f['params']['normal'], ax)) - 1) < 1e-6)
            L = offs[-1] - offs[0] if len(offs) > 1 else None
            out[name] = {'end_code_dir1': specs[0]['end_code'], 'D_mm': [x * 1e3 for x in D], 'cap_span_mm': L and abs(L) * 1e3,
                         'class': ['blind(cap span == D, no loops)'] if L and any(abs(abs(L) - x) < TOL for x in D) else ['unresolved(no loops)']}
        return out
    allP = np.vstack(L0)
    planes = [(np.array(f['params']['normal']), f['params']['point'], f['feature_first_name']) for f in faces
              if f['surface_type'] == 'plane' and 'normal' in (f.get('params') or {})]
    out = {}
    todo = dict(d.get('end_specs', {}))
    # zero-block extrudes (Through All / Up To ...) have no end_spec but are still extrudes
    for f in d['features']:
        if f['name'] not in todo and f['type'] in ('Boss-Extrude', 'Cut-Extrude', 'Extrusion') and 'Extrude' in f['name']:
            todo[f['name']] = []
    fid = {f['name']: f['id'] for f in d['features']}
    todo = dict(sorted(todo.items(), key=lambda kv: fid.get(kv[0], 0)))
    used = {c for f in d['features'] for c in f.get('children', [])}
    for name, specs in todo.items():
        F = feats.get(name)
        if not F: continue
        codes = [s['end_code'] for s in specs if not s['dir2']]; codes2 = [s['end_code'] for s in specs if s['dir2']]
        D = [num(v) for _, v in F['dims']]; D = [x / 1e3 for x in D if x]
        c1 = codes[0] if codes else None
        r = {'sw_enum_guess': SW_ENUM.get(c1), 'end_code_dir1': codes[0] if codes else None, 'end_code_dir2': codes2[0] if codes2 else None,
             'form': specs[0]['form'] if specs else 'none(no_end_spec)', 'D_mm': [x * 1e3 for x in D], 'depth_m_spec': specs[0]['depth_m'] if specs else None}
        skn = next((kid.get(c) for c in F.get('children', []) if kid.get(c) in sk), None)
        if not skn:
            # Keywords lists no child sketch: candidates = unconsumed sketches before F (nearest first);
            # the measured direction below picks the first whose normal is parallel to it
            cand = [s for s in sorted(sk.values(), key=lambda s: -(s.get('keywords_id') or 0))
                    if (s.get('keywords_id') or 0) < F['id'] and s.get('keywords_id') not in used and s.get('placement')]
            r['sketch_candidates'] = [s['name'] for s in cand[:3]]
        else: cand = []
        pl = sk.get(skn, {}).get('placement') if skn else None
        if not pl: pl = {'transform_rows_x_y_z_t': [1,0,0,0,1,0,0,0,1,0,0,0], 'confidence': 'none'}
        T = pl['transform_rows_x_y_z_t']; nsk = np.array(T[6:9]); s0sk = float(np.dot(T[9:12], nsk))
        r['sketch'] = skn; r['placement_conf'] = pl['confidence']
        own = [f for f in faces if F['id'] in f['feature_ids_by_time'] and len(face_pts(f))]
        own = [f for f in own if f.get('params')]
        if not own and len(d.get('end_specs', {})) == 1:
            own = [f for f in faces if f.get('params') and len(face_pts(f))]; r['faces_fallback'] = 'single-extrude part: all faces'
        if not own:
            if cand: r['sketch'] = cand[0]['name']; r['sketch_inferred'] = True; used.add(cand[0]['keywords_id'])
            r['class'] = 'no_faces_with_feature_id'; out[name] = r; continue
        # extrusion direction: candidate (sketch normal, cyl axes, plane normals) with most side faces
        cands = [nsk] + [np.array(f['params']['axis']) for f in own if 'axis' in (f.get('params') or {})] \
                + [np.array(f['params']['normal']) for f in own if 'normal' in (f.get('params') or {})]
        if cand:
            # nearest candidate whose normal explains the most side faces (ties -> nearest)
            sc = [(sum(_dir_side(f, np.array(c['placement']['transform_rows_x_y_z_t'][6:9])) for f in own), -i, c) for i, c in enumerate(cand)]
            top = max([sum(_dir_side(f, c) for f in own) for c in cands[1:]] or [0])
            hit = next((c for k, _, c in sc if top and k == top), cand[0] if cand else None)
            if hit:
                skn = hit['name']; pl = hit['placement']; used.add(hit['keywords_id'])
                T = pl['transform_rows_x_y_z_t']; nsk = np.array(T[6:9]); s0sk = float(np.dot(T[9:12], nsk))
                r['sketch'] = skn; r['placement_conf'] = pl['confidence']; r['sketch_inferred'] = True; cands[0] = nsk
        n = max(cands, key=lambda c: (sum(_dir_side(f, c) for f in own), c is nsk))
        side = [f for f in own if _dir_side(f, n) and len(face_pts(f))]
        if not side: r['class'] = 'no_side_faces'; out[name] = r; continue
        ident = list(map(float, pl['transform_rows_x_y_z_t'])) == [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        sk_ok = abs(abs(np.dot(n, nsk)) - 1) < 1e-6 and pl['confidence'] in ('high', 'medium') and not ident
        if np.dot(n, nsk) < 0: n = -n
        s0 = s0sk if sk_ok else None
        r['dir'] = list(np.round(n, 6)); r['sketch_plane_used'] = sk_ok
        P = np.vstack([face_pts(f) for f in side]); pr = P @ n; ap = allP @ n
        lo_abs, hi_abs = float(ap.min()), float(ap.max())
        caps = [float(np.dot(pp, n)) for pv, pp, pn in planes if abs(abs(np.dot(pv, n)) - 1) < 1e-6]
        if s0 is None:
            # assume sketch plane at the end that lies on a cap plane of another feature/ the body side
            s0 = float(pr.min())
            if abs(pr.min() + pr.max()) < TOL and pr.max() > TOL: r['symmetric_about_origin_plane'] = True
        a, b = float(pr.min()) - s0, float(pr.max()) - s0
        lo, hi = lo_abs - s0, hi_abs - s0
        r.update(extent_mm=[a * 1e3, b * 1e3], body_mm=[lo * 1e3, hi * 1e3], n_side_faces=len(side),
                 s0_mm=s0 * 1e3, extent_abs_mm=[(a + s0) * 1e3, (b + s0) * 1e3])
        L = b - a; cls = []
        near0 = abs(a) < TOL or abs(b) < TOL
        far = b if abs(a) < TOL else a
        if any(abs(L - x) < TOL for x in D) and near0: cls.append('blind')
        if abs(a + b) < TOL and any(abs(L - x) < TOL for x in D): cls.append('midplane')
        if abs(a + b) < TOL and any(abs(L - 2 * x) < TOL for x in D): cls.append('midplane(D=half?)')
        if near0 and (abs(far - lo) < TOL or abs(far - hi) < TOL): cls.append('reaches_body_extreme(through_all/up_to)')
        if near0 and not cls:
            hits = [pn for pv, pp, pn in planes if abs(abs(np.dot(pv, n)) - 1) < 1e-6 and abs(np.dot(pp, n) - s0 - far) < TOL and pn != name and True]
            if hits: cls.append('up_to_surface:' + hits[0])
            for x in D:
                h = [pn for pv, pp, pn in planes if abs(abs(np.dot(pv, n)) - 1) < 1e-6 and min(abs(np.dot(pp, n) - s0 - far - x), abs(np.dot(pp, n) - s0 - far + x)) < TOL]
                if h: cls.append(f'offset_from_surface({x*1e3:g}mm):' + h[0]); break
        if not near0: cls.append('starts_off_sketch_plane(offset start / consumed)')
        if not sk_ok and cls and cls[0] == 'blind': cls[0] = 'blind_or_midplane(length==D, sketch plane unknown)'
        if not any(abs(L - x) < TOL for x in D) and D and near0 and not cls: cls.append('length!=D(consumed/offset)')
        if r.get('symmetric_about_origin_plane') and any(abs(L - x) < TOL for x in D): cls.insert(0, 'midplane(about default plane)')
        r['class'] = cls or ['unresolved']
        out[name] = r
    return out

def tally(results):
    t = collections.defaultdict(collections.Counter)
    for part, res in results.items():
        for r in res.values():
            c = r.get('class'); c = c if isinstance(c, list) else [c]
            t[r['end_code_dir1']][c[0].split(':')[0].split('(')[0]] += 1
    return {k: dict(v) for k, v in t.items()}

if __name__ == '__main__':
    allr = {}
    for p in sys.argv[1:]:
        sp = p[:-5] + '.sketchplane.json'
        r = classify(json.load(open(p)), json.load(open(sp)) if os.path.exists(sp) else None); allr[p] = r
        json.dump(r, open(p[:-5] + '.endcond.json', 'w'), indent=1, default=float)
        for k, v in r.items(): print(p.split('/')[-1][:5], k, v.get('end_code_dir1'), v.get('D_mm'), v.get('extent_mm'), v.get('body_mm'), v['class'])
    print(json.dumps(tally(allr), default=str))
