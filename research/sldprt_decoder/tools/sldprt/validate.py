"""Train / validate the feature-stream layouts (fstream.py) against the API dumps.

    python3 -I -m sldprt.validate <revdev_dir> <dumps_dir> <out.json>

Split: parts sorted by name; even positions = train, odd = validation.
Training re-derives the free layout constants from the train half only (by
searching for the byte offset / flag value that best reproduces the dump), then
checks they equal the constants hard-coded in fstream.  Accuracy is reported
per class and split, field by field; coverage per part.
"""
from . import item_structs as IS
import glob
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

from . import answer_key as AK
from . import fstream as FS
from . import objnum as ON
from . import classrec as CR
from . import streams as ST


def feature_stream(path):
    best = None
    for s in ST.all_streams(open(path, 'rb').read()):
        if ST.classify(s) == 'features' and (best is None or len(s['data']) > len(best)):
            best = s['data']
    return best


def _close(a, b, tol=1e-9):
    return a is not None and b is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


class Acc:
    def __init__(self):
        self.c = defaultdict(Counter)

    def add(self, cls, fld, ok):
        self.c[(cls, fld)]['n'] += 1
        self.c[(cls, fld)]['ok'] += bool(ok)

    def table(self):
        return {f'{c}.{f}': {'ok': v['ok'], 'n': v['n'], 'pct': round(100 * v['ok'] / v['n'], 2) if v['n'] else None}
                for (c, f), v in sorted(self.c.items())}


# ------------------------------------------------------------------ face evidence (region selection truth)
def _xf(T, p):
    R, t = T[:9], T[9:12]
    x, y, z = p
    return (x * R[0] + y * R[3] + z * R[6] + t[0], x * R[1] + y * R[4] + z * R[7] + t[1],
            x * R[2] + y * R[5] + z * R[8] + t[2])


def _sub(a, b): return tuple(i - j for i, j in zip(a, b))
def _dot(a, b): return sum(i * j for i, j in zip(a, b))


def _unit(a):
    n = math.sqrt(_dot(a, a))
    return tuple(i / n for i in a) if n > 1e-15 else a


def seg_has_face(sg, T, faces):
    """a sketch segment produced a side face of an extrusion (plane through a line,
    cylinder of the arc's radius on the arc's axis)."""
    if sg['type'] == 0:
        a, b = _xf(T, sg['p0']), _xf(T, sg['p1'])
        zn = _unit(_sub(_xf(T, (0, 0, 1)), _xf(T, (0, 0, 0))))
        m = tuple((x + y) / 2 for x, y in zip(a, b))
        for f in faces:
            if f['kind'] == 'plane' and 'n' in f:
                n = _unit(f['n'])
                if abs(_dot(n, zn)) > 1e-6:
                    continue     # round 9: a cap face (parallel to the sketch) is no evidence
                bx = f.get('box')
                if bx and len(bx) >= 6 and not all(bx[k] - 1e-7 <= m[k] <= bx[k + 3] + 1e-7 for k in range(3) if abs(zn[k]) < 0.5):
                    continue     # round 9: the segment's midpoint must lie on the face
                if abs(_dot(_sub(a, f['o']), n)) < 1e-7 and abs(_dot(_sub(b, f['o']), n)) < 1e-7 \
                        and abs(_dot(_unit(_sub(b, a)), n)) < 1e-6:
                    return True
    elif sg['type'] == 1 and 'c' in sg and sg.get('r'):
        c = _xf(T, sg['c'])
        for f in faces:
            if f['kind'] == 'cyl' and 'ax' in f and abs(f['r'] - sg['r']) < 1e-8:
                ax, v = _unit(f['ax']), _sub(c, f['o'])
                w = (v[1] * ax[2] - v[2] * ax[1], v[2] * ax[0] - v[0] * ax[2], v[0] * ax[1] - v[1] * ax[0])
                if math.sqrt(_dot(w, w)) < 1e-7:
                    return True
    return False


# ------------------------------------------------------------------ per part evaluation
EXTRUDE_TYPES = ('Extrusion', 'ICE')
FACES = True
DEBUG = None
PATTERN_TYPES = ('MirrorPattern', 'CirPattern', 'LPattern')


_TM = None


def _templates():
    """whole-object layouts learned on the train half (wip_r8/train_templates.py)"""
    global _TM
    if _TM is None:
        p = os.path.join(os.path.dirname(__file__), 'templates_round8.json')
        _TM = json.load(open(p)) if os.path.exists(p) else {}
    return _TM


_TM2 = None


def _templates2():
    """round 10: string-aware (class, CString gap signature) templates, train half only
    (wip_r10/train_templates2.py)"""
    global _TM2
    if _TM2 is None:
        p = os.path.join(os.path.dirname(__file__), 'templates_round10.json')
        _TM2 = json.load(open(p)) if os.path.exists(p) else {}
    return _TM2


_TM3 = None


def _templates3():
    """round 13: string-aware templates keyed by ABSOLUTE external class index, trained on
    the train halves of dumps_v2 + corpus + dumps_ab (wip_r13/train_templates3.py)"""
    global _TM3
    if _TM3 is None:
        p = os.path.join(os.path.dirname(__file__), 'templates_round13.json')
        _TM3 = json.load(open(p)) if os.path.exists(p) else {}
    return _TM3


_TM4 = None


def _templates4():
    """round 14: same learner, min_n 2 / min_const 0.4 / const_share 0.9, trained on the train halves
    of dumps_v2 + corpus + dumps_ab (wip_r14/train_templates4.py)"""
    global _TM4
    if _TM4 is None:
        p = os.path.join(os.path.dirname(__file__), 'templates_round14.json')
        _TM4 = json.load(open(p)) if os.path.exists(p) else {}
    return _TM4


def evaluate(d, D, acc):
    top = D.top()
    allf = D.features + [c for f in D.features for c in f.children]
    hidx = FS.header_index(d)
    ex_ids = {f.id for f in top if f.extrude}
    dec = FS.decode(d, ex_ids)
    byname = {f.name: f for f in top}
    # FEATURE
    hs = {(h.name, h.feature_id) for h in dec.headers}
    for f in allf:
        if f.type in ('AmbientLight', 'DirectionLight', 'EnvFolder'):
            continue  # stored in another stream
        acc.add('FeatureHeader', 'id', (f.name, f.id) in hs)
    # DIM (own dims of each feature)
    for f in top:
        if f.id not in dec.dims:
            continue
        mine = dict(dec.dims[f.id])
        for full, v in f.dims:
            parts = full.split('@')
            if len(parts) >= 2 and parts[1] == f.name:
                got = mine.get(parts[0])
                acc.add('DimValue', 'value', got is not None and abs(got - v) <= 1e-9 * max(1, abs(v)) + 1e-12)
    # SKETCHES
    for f in top:
        if f.type != 'ProfileFeature' or f.id not in dec.sketches:
            if f.type == 'ProfileFeature' and (f.pts or f.segs):
                acc.add('Sketch', 'found', False)
            continue
        acc.add('Sketch', 'found', True)
        X = dec.sketches[f.id]
        sk = X['sketch']
        for (i, pid), xyz in f.pts.items():
            p = sk.points[i] if i < len(sk.points) else None
            acc.add('SketchPoint', 'id', p is not None and p.pid == pid)
            acc.add('SketchPoint', 'xy', p is not None and p.pid == pid and _close(p.xy, xyz[:2]))
        pxy = {i: xyz[:2] for (i, _), xyz in f.pts.items()}
        for sg in f.segs:
            if sg['type'] not in (0, 1):
                acc.add('SketchSegment', 'id', False)
                continue
            r = sk.seg(sg['type'], sg['id'])
            acc.add('SketchSegment', 'id', r is not None)
            if r is None or r.start is None:
                for k in ('type', 'endpoints', 'construction'):
                    acc.add('SketchSegment', k, False)
                continue
            acc.add('SketchSegment', 'type', r.type in ((0,) if sg['type'] == 0 else (1, 0xFFFF)))

            def P(i):
                if i < len(sk.points) and sk.points[i].xy is not None:
                    return sk.points[i].xy
                return pxy.get(i)
            a, b = P(r.start), P(r.end)
            ok = (_close(a, sg['p0'][:2], 1e-8) and _close(b, sg['p1'][:2], 1e-8)) or \
                 (_close(a, sg['p1'][:2], 1e-8) and _close(b, sg['p0'][:2], 1e-8))
            acc.add('SketchSegment', 'endpoints', ok)
            acc.add('SketchSegment', 'construction', r.construction == sg['constr'])
            if sg['type'] == 1 and 'c' in sg:
                acc.add('SketchSegment', 'arc_centre', _close(P(r.centre), sg['c'][:2], 1e-8))
        # REL
        got = Counter((r.type, tuple(sorted(x[1] for x in r.ents))) for r in FS.api_relations(X['relations']))
        want = Counter((t, tuple(sorted(es))) for t, es in f.rels)
        for k, v in want.items():
            h = min(v, got.get(k, 0))
            for _ in range(h):
                acc.add('Relation', 'type+entities (recall)', True)
            for _ in range(v - h):
                acc.add('Relation', 'type+entities (recall)', False)
        for k, v in got.items():
            h = min(v, want.get(k, 0))
            for _ in range(h):
                acc.add('Relation', 'type+entities (precision)', True)
            for _ in range(v - h):
                acc.add('Relation', 'type+entities (precision)', False)
        # CONTOUR (chains)
        ser = {}
        for s_ in sk.lines:
            ser[(0, s_.index, s_.pid)] = s_.serial
        for s_ in sk.arcs:
            ser[(1, s_.index, s_.pid)] = s_.serial
        stored = bool(X['chains'])
        chs = X['chains'] if stored else FS.computed_contours(sk)
        chain_sets = [sorted(c.serials) for c in chs]
        tag = 'stored moSketchChain_c' if stored else 'computed (sketch has no chains)'
        for closed, ids in f.contours:
            segs = AK.resolve_contour(f, ids)
            want_s = sorted(ser.get((s_['type'],) + s_['id'], -1) for s_ in segs if s_)
            acc.add('Contour', 'segment set, ' + tag, want_s in chain_sets)
            m = [c for c in chs if sorted(c.serials) == want_s]
            if m:
                acc.add('Contour', 'closed, ' + tag, (m[0].closed == 1) == closed)
    # EXTRUDE
    ids_ = {x.name: x.id for x in top}
    for f in top:
        if not f.extrude:
            continue
        es = dec.endspecs.get(f.id)
        x = f.extrude
        for k, v in (('end1', es and es.end1 == x['end1']), ('end2', es and es.end2 == x['end2']),
                     ('reverse', es and es.reverse == int(x['reverse'])),
                     ('both', es and es.both == x['both'])):
            acc.add('EndSpec', k, v)
        if x['d1']:
            acc.add('EndSpec', 'depth1', es is not None and es.depth1 is not None and abs(es.depth1 - x['d1']) < 1e-12)
        if int(x['end1']) in FS.UPTO_ENDS:
            nonsk = {ids_.get(p) for p, t in f.parents if t not in ('ProfileFeature', 'OriginProfileFeature')}
            acc.add('EndSpec', 'up-to reference owner is a parent feature',
                    es is not None and es.upto_ref is not None and es.upto_ref[0] in nonsk)
        if x['both'] and x['d2']:
            acc.add('EndSpec', 'depth2', es is not None and es.depth2 is not None and abs(es.depth2 - x['d2']) < 1e-12)
    # REGION SELECTION (face evidence)
    for f in top:
        if f.type not in EXTRUDE_TYPES:
            continue
        skn = [p for p, t in f.parents if t == 'ProfileFeature']
        S = byname.get(skn[0]) if skn else None
        if S is None or S.id not in dec.sketches or not S.sketch_to_model:
            continue
        X = dec.sketches[S.id]
        sk = X['sketch']
        sel, has = FS.selected_serials(X['choosers'], X['regions'], sk, X['chains'] or None, faces=FACES)
        ser = {}
        for s_ in sk.lines:
            ser[(0,) + s_.api_id] = s_.serial
        for s_ in sk.arcs:
            ser[(1,) + s_.api_id] = s_.serial
        region_serials = set(x for r in X['regions'] for x in r.serials)
        evid, allnc = set(), set()
        for sg in S.segs:
            a = ser.get((sg['type'],) + sg['id'])
            if a is None:
                continue
            if not sg['constr']:
                allnc.add(a)
            if not sg['constr'] and seg_has_face(sg, S.sketch_to_model, f.faces):
                # construction geometry never bounds a region; a construction line lying
                # on a face plane is coincidence, not evidence
                evid.add(a)
        mode = 'chooser' if has else 'all-regions'
        for a in evid:
            acc.add('RegionSelection', f'face-evidenced segment selected ({mode})', a in sel or a == 0)
        if DEBUG is not None and has and evid - sel - {0}:
            DEBUG.append((f.name, S.name, sorted(evid - sel - {0}), [[ct.serials for ct in c.contours] for c in X['choosers']],
                          [(r.rid, r.serials) for r in X['regions']], sorted(sel)))
        if has:
            for a in (allnc & region_serials) - sel:
                acc.add('RegionSelection', 'excluded segment has no face', a not in evid)
            for ct in [ct for c in X['choosers'] for ct in c.contours]:
                acc.add('RegionSelection', 'chooser contour matched to sketch region', ct.rid is not None)
                acc.add('RegionSelection', 'chooser contour matched by serial set', ct.how == 'serials')
    # FILLET / CHAMFER
    for f in top:
        if f.fillet is None and f.chamfer is None:
            continue
        dims = dict(dec.dims.get(f.id, []))
        if f.fillet is not None:
            acc.add('Fillet', 'radius', abs(dims.get('D1', 1e9) - f.fillet['r']) < 1e-12)
        else:
            acc.add('Chamfer', 'distance', abs(dims.get('D1', 1e9) - f.chamfer['d']) < 1e-12)
            acc.add('Chamfer', 'angle', abs(dims.get('D2', 1e9) - f.chamfer['angle']) < 1e-9)
    # PATTERN / MIRROR
    ids = {x.name: x.id for x in top}
    ev, _ = ON.numbering(d)
    heads = FS.feature_headers(d)
    fobj = ON.feature_objects(d, heads, ev)
    fids = {h.feature_id for h in heads}
    recs = CR.decode(d, ev, fids)
    dec.spans += CR.spans(recs) + [(e.offset, e.end) for e in ev]
    srecs = IS.decode(d, list(CR._obj_spans(d, ev)), fids)       # round 11b struct readers
    dec.spans += IS.spans(srecs)
    for cls, _, _, f in srecs:
        if cls == 'ext_hist_display' and 'feature_id' in f:
            acc.add('ext_hist_display', 'feature_id is a feature header id', f['feature_id'] in fids)
        if cls == 'ext_named_item' and f['id'] > 0:
            acc.add('ext_named_item', 'id is a feature header id', f['id'] in fids)
    tm = _templates()
    if tm:
        trs = CR.decode_templates(d, ev, tm)
        dec.spans += CR.spans(trs)
        got = {r.offset for r in trs}
        for e in ev:
            if e.kind == 'new' and e.name in tm:
                acc.add('Template', 'object matches its learned whole-object layout', e.offset in got)
    tm2 = _templates2()
    if tm2:
        dec.spans += CR.spans(CR.decode_templates2(d, ev, tm2))
    tm3 = _templates3()
    if tm3:
        dec.spans += CR.spans(CR.decode_templates2(d, ev, tm3, ext_abs=True))
    tm4 = _templates4()
    if tm4:
        dec.spans += CR.spans(CR.decode_templates2(d, ev, tm4, ext_abs=True))
    blobs = CR.ps_blobs(d)
    dec.spans += [(a, b) for a, b, _ in blobs]
    acc.add('Numbering', 'self-consistent (residual 0)', ON.numbering.residual == 0)
    for a, b, raw in blobs:
        acc.add('ParasolidBlob', 'inflates to a Parasolid transmit file of the stored size', raw > 0 and a < b - 20)
    dimvals = {round(abs(v), 9) for f in top for _, v in f.dims}
    for r in recs:
        if r.cls == 'moFavoriteHandle_c':
            acc.add('moFavoriteHandle_c', 'value is a dimension value of the part', round(abs(r.fields['value']), 9) in dimvals)
    nfr = sum(1 for e in ev if e.name == 'moFR_c' and e.kind == 'new')
    for r in recs:
        if r.cls == 'moFR_c':
            acc.add('moFR_c', 'feature_id is a feature header id', True)
    for _ in range(nfr - sum(1 for r in recs if r.cls == 'moFR_c')):
        acc.add('moFR_c', 'feature_id is a feature header id', False)
    pts = set()
    for X in dec.sketches.values():
        for p_ in X['sketch'].points:
            if p_.xy:
                pts.add((round(p_.xy[0], 7), round(p_.xy[1], 7)))
    for r in recs:
        if r.cls == 'moPointBackedUpData_c':
            acc.add('moPointBackedUpData_c', 'xy is a stored sketch point', (round(r.fields['x'], 7), round(r.fields['y'], 7)) in pts)
    for f in top:
        if f.type not in PATTERN_TYPES:
            continue
        h = hidx.get(f.id)
        if h is None:
            continue
        seeds = ON.resolve_objects(ON.seed_list(d, h), fobj, h.offset)
        sids = {x[0] for x in seeds if x}
        parents = {ids.get(pn) for pn, pt in f.parents if pt != 'RefPlane'}
        acc.add('Pattern', 'seed list (object refs) non-empty and all seeds are parents', bool(sids) and sids <= parents)
        for x in seeds:
            if x:
                acc.add('Pattern', 'seed object ref exact (numbering drift 0)', x[1] == 0)
    for f in top:
        if f.type not in PATTERN_TYPES:
            continue
        h = hidx.get(f.id)
        if h is None:
            continue
        refs = FS.referenced_feature_ids(d, h.offset, h.region_end, set(ids.values()))
        dims = dict(dec.dims.get(f.id, []))
        for full, v in f.dims:
            p = full.split('@')
            if p[1] == f.name:
                acc.add('Pattern', 'count/spacing dim', abs(dims.get(p[0], 1e9) - v) < 1e-9)
        if f.type == 'MirrorPattern':
            mp = FS.mirror_plane_ref(d, h, set(ids.values()))
            for pn, pt in f.parents:
                if pt == 'RefPlane':
                    acc.add('Mirror', 'plane reference', mp is not None and mp[0] == ids.get(pn))
        sids = {x[0] for x in ON.resolve_objects(ON.seed_list(d, h), fobj, h.offset) if x}
        for pn, pt in f.parents:
            if pt == 'RefPlane':
                continue
            acc.add('Pattern', 'parent referenced (feature-id ref or seed object ref)', ids.get(pn) in refs or ids.get(pn) in sids)
            acc.add('Pattern', 'seed feature referenced', ids.get(pn) in refs)
    return dec


def train(parts):
    """re-derive the free constants on the training parts only."""
    out = {}
    # EndSpec field offsets: best offset for end1 / reverse / end2
    samples = []
    for d, D in parts:
        ex = {f.id: f for f in D.top() if f.extrude}
        dec = FS.decode(d, set(ex))
        for fid, es in dec.endspecs.items():
            samples.append((d, es.offset, ex[fid].extrude))
    for fld in ('end1', 'reverse', 'end2'):
        best = max(range(0, 64), key=lambda k: sum(d[S + k] == int(x[fld]) for d, S, x in samples))
        out[f'endspec.{fld}_offset'] = best
    # construction flag value
    c = Counter()
    for d, D in parts:
        dec = FS.decode(d, set())
        for f in D.sketches():
            X = dec.sketches.get(f.id)
            if not X:
                continue
            for sg in f.segs:
                r = X['sketch'].seg(sg['type'], sg['id'])
                if r and r.real is not None:
                    c[(r.real, sg['constr'])] += 1
    out['segment.real_flag_value_for_construction'] = max((0, 1), key=lambda v: c[(v, True)] - c[(v, False)])
    # relation visibility rule: flag value most associated with API-listed records
    vis = Counter()
    for d, D in parts:
        dec = FS.decode(d, set())
        for f in D.sketches():
            X = dec.sketches.get(f.id)
            if not X:
                continue
            want = Counter((t, tuple(sorted(es))) for t, es in f.rels)
            for r in X['relations']:
                k = (r.type, tuple(sorted(x[1] for x in r.ents)))
                hit = want[k] > 0
                if hit:
                    want[k] -= 1
                vis[(r.dimension, r.flag, hit)] += 1
    out['relation.geometric_visible_flag'] = max((0, 1), key=lambda v: vis[(False, v, True)] - vis[(False, v, False)])
    out['relation.dimension_visible_flag'] = max((0, 1), key=lambda v: vis[(True, v, True)] - vis[(True, v, False)])
    expected = {'endspec.end1_offset': 18, 'endspec.reverse_offset': 12, 'endspec.end2_offset': 22,
                'segment.real_flag_value_for_construction': 0, 'relation.geometric_visible_flag': 0,
                'relation.dimension_visible_flag': 1}
    return {'derived': out, 'hard_coded': expected, 'agree': all(out[k] == v for k, v in expected.items())}


def run(revdev, dumps):
    names = sorted(os.path.basename(p)[:-9] for p in glob.glob(os.path.join(dumps, '*.dump.txt')))
    data = []
    for n in names:
        src = os.path.join(revdev, n + '.SLDPRT')
        d = feature_stream(src) if os.path.exists(src) else None
        if d is None:   # round 11b: some corpus parts have no feature stream / no file
            continue
        data.append((n, d, AK.parse(os.path.join(dumps, n + '.dump.txt'))))
    tr = [x for k, x in enumerate(data) if k % 2 == 0]
    va = [x for k, x in enumerate(data) if k % 2 == 1]
    res = {'train_parts': [n for n, _, _ in tr], 'validation_parts': [n for n, _, _ in va],
           'training': train([(d, D) for _, d, D in tr])}
    cov = {}
    for split, items in (('train', tr), ('validation', va)):
        acc = Acc()
        for n, d, D in items:
            dec = evaluate(d, D, acc)
            old = __import__('sldprt.mfc', fromlist=['scan']).scan(d)['coverage_pct']
            cov[n] = {'split': split, 'bytes': len(d), 'coverage_pct': round(FS.coverage(d, dec.spans), 2),
                      'previous_round_pct': old}
        res[split] = acc.table()
    res['coverage'] = cov
    return res


def main(argv):
    revdev, dumps, out = argv
    res = run(revdev, dumps)
    json.dump(res, open(out, 'w'), indent=1)
    for split in ('train', 'validation'):
        print('==', split)
        for k, v in res[split].items():
            print(f'  {k:60s} {v["ok"]:5d}/{v["n"]:<5d} {v["pct"]}')
    print('training', res['training'])
    c = res['coverage']
    print('coverage mean', round(sum(v['coverage_pct'] for v in c.values()) / len(c), 2),
          'previous', round(sum(v['previous_round_pct'] for v in c.values()) / len(c), 2))


if __name__ == '__main__':
    main(sys.argv[1:])
