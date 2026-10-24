"""Decode one SLDPRT into a dict (faces, sketches, metadata)."""
import os
import re
from collections import Counter

from . import streams as S
from .xt import XT
from . import meta as M
from . import sketch as SK


def _feature_name(items, fid):
    it = items.get(fid)
    return (it['name'], it['type']) if it else (None, None)


def x_is(xt, s):
    return xt.d is s['data']


def decode_file(path, step_ents=None):
    data = open(path, 'rb').read()
    st = S.all_streams(data)
    out = {'file': os.path.basename(path), 'size': len(data), 'streams': []}
    xts, feat = [], None
    for s in st:
        c = S.classify(s)
        out['streams'].append({'offset': s['offset'], 'nested': s['nested'], 'len': len(s['data']), 'class': c})
        if c == 'parasolid':
            xts.append(XT(s['data']))
        elif c == 'features' and (feat is None or len(s['data']) > len(feat)):
            feat = s['data']
    meta = M.collect_meta(st)
    items = M.parse_keywords(meta['keywords']) if meta['keywords'] else {}
    parents = M.sketch_parents(items)
    out['meta'] = {k: v for k, v in meta.items() if k != 'keywords'}
    out['features'] = [{'id': i, 'name': it['name'], 'type': it['type'], 'tag': it['tag'], 'dims': it['dims'],
                        'children': it['children']} for i, it in sorted(items.items())
                       if it['type'] not in M.SKIP_TYPES and it['tag'] != 'Keywords']
    # equations: look for '"X" = ...' text anywhere in the feature stream
    texts = []
    if feat:
        texts += [feat.decode('latin1'), feat.decode('utf-16-le', 'replace'), feat[1:].decode('utf-16-le', 'replace')]
    out['meta']['equations'] = M.equations_from_text(texts)

    # ---- faces -------------------------------------------------------------
    main = max(xts, key=lambda x: len(x.faces)) if xts else None
    out['parasolid'] = [{'version': x.version, 'schema': x.schema, 'faces': len(x.faces), 'surfaces': len(x.surfaces),
                         'attributes': len(x.attributes)} for x in xts]
    faces = []
    if main:
        for f in main.faces:
            srf = main.surfaces[f['surface']]
            atoms = main.face_features(f['index'])
            fids = []
            for a in sorted(atoms, key=lambda a: a['stamp']):
                if a['feature_id'] not in fids:
                    fids.append(a['feature_id'])
            first = fids[0] if fids else None
            last = max(atoms, key=lambda a: a['stamp'])['feature_id'] if atoms else None
            other = {a['name']: a['values'] for a in main.attrs_by_owner.get(f['index'], [])
                     if a['name'] not in ('ATOM_ID_2001', 'FACE_ID_2001')}
            loops = main.face_loops(f['index'])
            faces.append({'xt_index': f['index'], 'node_id': f['node_id'], 'shell': f['shell'], 'face_sense': f['sense'],
                          'surface_index': f['surface'], 'surface_type': srf['type'], 'surface_sense': srf['sense'],
                          'params': srf.get('params'),
                          'feature_ids_by_time': fids,
                          'feature_first': first, 'feature_first_name': _feature_name(items, first)[0],
                          'feature_last': last, 'feature_last_name': _feature_name(items, last)[0],
                          'atom_ids': [a['raw'] for a in atoms], 'other_attrs': other, 'loops': loops})
        # adjacency via edges shared by two faces' loops
        e2f = {}
        for k, fc in enumerate(faces):
            for L in fc['loops']:
                for e in L['edges']:
                    e2f.setdefault(e['edge'], set()).add(k)
        for k, fc in enumerate(faces):
            fc['adjacent_faces'] = sorted({j for L in fc['loops'] for e in L['edges'] for j in e2f.get(e['edge'], ()) if j != k})
        out['bodies'] = [{'attr': a['name'], 'owner': a['owner'], 'values': a['values']} for a in main.body_attrs()
                         if a['name'] != 'SDL/TYSA_COLOUR_2']
    out['faces'] = faces
    out['face_summary'] = dict(Counter(f['surface_type'] for f in faces))

    # ---- sketches ------------------------------------------------------------
    sk_names = [it['name'] for it in items.values() if (it['tag'] == 'Sketch' or 'Sketch' in it['type']) and it['name'] not in ('Origin', '')]
    sketches = []
    if feat and sk_names:
        surfs = list(main.surfaces.values()) if main else None
        for sk in SK.decode_sketches(feat, sk_names, surfs):
            sid = next((i for i, it in items.items() if it['name'] == sk['name']), None)
            dims = items[sid]['dims'] if sid is not None else []
            sk['keywords_id'] = sid
            sk['used_by'] = [items[parents[sid]]['name']] if sid in parents else []
            sk['dims'] = dims
            sk['dim_matches'] = SK.match_dims(dims, sk['points'], sk['entities'])
            for p in sk['points']:
                p.pop('pos', None)
            sketches.append(sk)
    out['sketches'] = sketches
    # ---- structural layer: coverage per stream ---------------------------------
    from . import container as C, xt_struct as XS, mfc
    secs, gaps = C.parse(data)
    out['structural'] = {'container': C.full_coverage(data),
                         'sections': [{'name': s.name, 'offset': s.offset, 'csize': s.csize, 'usize': s.usize,
                                       'inflated': s.inflated, 'crc_ok': s.crc_ok} for s in secs]}
    xs = []
    for s in st:
        if S.classify(s) == 'parasolid':
            nodes, g, cov, unk = XS.walk(s['data'])
            nf = {n.index for n in nodes if n.name == 'FACE'}
            xs.append({'offset': s['offset'], 'coverage_pct': cov, 'nodes': len(nodes), 'gaps': len(g),
                       'gap_start_types': dict(sorted(unk.items(), key=lambda x: -x[1])[:12]),
                       'faces_sequential': len(nf),
                       'faces_agree_with_pattern_reader': (len(nf & {f['xt_index'] for f in faces}), len(faces)) if main and len(main.faces) == len(faces) and x_is(main, s) else None})
    out['structural']['parasolid'] = xs
    if feat:
        m = mfc.scan(feat)
        m.pop('classes', None)
        out['structural']['feature_stream'] = m
    if feat:
        from . import features as FP
        out['feature_params'] = FP.infer(feat, out)
        out['ref_planes'] = FP.ref_planes(feat, out['features'])
        from . import mo_classes as MO
        es = {}
        for f, a, b in FP.feature_regions(feat, out['features']):
            if 'Extrude' not in f['name']: continue
            L = [x.json() for x in MO.endspecs(feat, a, b)]
            for x in L:
                x['depth_matches_dim'] = bool(x['depth_m']) and any(abs(MO.num(v) / 1000 - x['depth_m']) < 1e-9 for _, v in f['dims'] if MO.num(v) is not None)
            if L: es[f['name']] = L
        out['end_specs'] = es
    missing = [n for n in sk_names if n not in {s['name'] for s in sketches}]
    out['sketches_not_located'] = missing

    # ---- STEP cross-check ------------------------------------------------------
    if step_ents is not None and faces:
        from .stepcheck import best_match
        radii = [f['params']['radius'] * 1000 for f in faces if f['surface_type'] == 'cylinder' and f['params']]
        out['step_check'] = best_match(step_ents, radii, sum(1 for f in faces if f['surface_type'] == 'plane'))
    return out
