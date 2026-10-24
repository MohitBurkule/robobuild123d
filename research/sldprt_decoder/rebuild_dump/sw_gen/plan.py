"""Feature list -> ops. Kernel-free: everything is decided from the dump (sketch geometry, PARENT,
DIM, EXTRUDE, FACE lines). The optional build123d replay (replay.py) later fills in expected volumes,
fillet/chamfer edges and up-to faces.

An Op is one interpreter line for the VBA side (see interp.bas for the exact field meaning).
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field

import numpy as np

from .model import STD_PLANES, STD_NORMAL, STD_FRAME
from . import sketch as S

SILENT_TYPES = {'OriginProfileFeature', 'DetailCabinet', 'MaterialFolder', 'EnvFolder', 'AmbientLight',
                'DirectionLight', 'SpotLight', 'PointLight', 'CameraFolder'}
EXTRUDE_TYPES = {'Extrusion', 'ICE', 'Boss', 'Cut', 'BossThin', 'CutThin', 'ExtrusionThin', 'ICEThin'}
REVOLVE_TYPES = {'Revolution', 'RevCut', 'RevolutionThin', 'RevCutThin'}
BODY_PARENT_SKIP = {'RefPlane', 'ProfileFeature', '3DProfileFeature', 'OriginProfileFeature', 'RefAxis',
                    'RefPoint', 'CoordSys', 'MaterialFolder'}


def fmt(x) -> str:
    if isinstance(x, bool):
        return '1' if x else '0'
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        x = float(x)
        if abs(x) < 1e-15:
            return '0'
        return f'{x:.12g}'
    return str(x).replace('|', '/').replace('\n', ' ')


@dataclass
class Op:
    kind: str
    args: list = field(default_factory=list)
    feat: str = ''
    meta: dict = field(default_factory=dict)

    def line(self) -> str:
        return '|'.join([self.kind] + [fmt(a) for a in self.args])


@dataclass
class FeatPlan:
    name: str
    type: str
    status: str            # EMIT | SKIP | SILENT
    reason: str = ''
    ops: list = field(default_factory=list)
    meta: dict = field(default_factory=dict)


def _unit(v):
    v = np.array(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def _par(a, b, tol=1e-6):
    return abs(abs(float(np.dot(_unit(a), _unit(b)))) - 1.0) < tol


# ----------------------------------------------------------------------------- geometry helpers
def plane_of(f):
    """(origin, x, y, normal) of a RefPlane feature (PLANE line) or None."""
    a = f.plane
    if a is None or len(a) < 12:
        return None
    return (np.array(a[9:12], float), np.array(a[0:3], float), np.array(a[3:6], float), np.array(a[6:9], float))


def sketch_frame(sk):
    R = np.array(sk.rot, float)
    return np.array(sk.trans, float), R[0], R[1], R[2]


def coplanar(o1, n1, o2, n2, tol=1e-7):
    return _par(n1, n2) and abs(float(np.dot(np.array(o2) - np.array(o1), _unit(n1)))) < tol


def face_matches_seg(F, e: S.Ent, sk, n, tol=2e-6):
    """does dumped FACE F look like the side face swept by sketch entity e along n?"""
    if F.kind == 'plane' and e.kind == 'line':
        fn = _unit(F.params['n'])
        if abs(fn @ n) > 1e-5:
            return False
        a = S.to_model(sk, e.p0); b = S.to_model(sk, e.p1)
        o = np.array(F.params['o'])
        if abs(fn @ (a - o)) > tol or abs(fn @ (b - o)) > tol:
            return False
        return _box_hits(F.box, (a + b) / 2, n)
    if F.kind == 'cyl' and e.kind in ('arc', 'circle'):
        if abs(F.params['r'] - e.r) > tol:
            return False
        ax = _unit(F.params['ax'])
        if not _par(ax, n, 1e-5):
            return False
        c = S.to_model(sk, e.c); w = c - np.array(F.params['o'])
        if np.linalg.norm(w - ax * (w @ ax)) > tol:
            return False
        return _box_hits(F.box, c, n, slack=e.r * 1.01)
    return False


def _box_hits(box, p, n, slack=1e-6):
    """p projected along n hits the face box (box ignored along n)."""
    if box is None:
        return True
    lo = np.array(box[:3]) - slack - 1e-6; hi = np.array(box[3:6]) + slack + 1e-6
    for i in range(3):
        if abs(n[i]) > 0.999:
            continue
        if abs(n[i]) > 1e-6:
            return True          # oblique: do not filter
        if p[i] < lo[i] or p[i] > hi[i]:
            return False
    return True


def used_contours(feat, skf, sp: S.SketchPlan, n):
    """which closed contours the feature consumed, from its own FACE lines.
    -> (list of contour dicts, how) ; how in ALL | SUBSET | NOEVIDENCE"""
    closed = [c for c in sp.contours if c['closed'] and c['keys']]
    if not closed:
        return [], 'NOCONTOUR'
    faces = feat.faces or []
    scores = []
    for c in closed:
        hit = 0
        for k in c['keys']:
            e = sp.ent(k)
            if e is None or e.constr:
                continue
            if any(face_matches_seg(F, e, skf.sketch, n) for F in faces):
                hit += 1
        scores.append(hit)
    if not any(scores):
        return closed, 'NOEVIDENCE'
    used = [c for c, s in zip(closed, scores) if s > 0]
    # a contour nested inside a used contour whose own faces are all gone (later features) is ambiguous;
    # we keep evidence-only semantics: only contours with surviving side faces are selected
    if len(used) == len(closed):
        return used, 'ALL'
    return used, 'SUBSET'


def cap_offsets(feat, origin, n):
    """signed offsets along n of the feature's planar FACEs normal to n (end caps)."""
    out = []
    for F in feat.faces or []:
        if F.kind == 'plane' and _par(F.params['n'], n, 1e-6):
            out.append(float(np.dot(np.array(F.params['o']) - origin, n)))
    return sorted(set(round(x, 9) for x in out))


def axis_from_faces(faces):
    """dominant (origin, axis) among cyl/cone/torus FACEs."""
    axes = []
    for F in faces or []:
        if F.kind == 'cyl':
            axes.append((np.array(F.params['o'], float), _unit(F.params['ax'])))
        elif F.kind in ('cone', 'torus') and len(F.params.get('values', [])) >= 6:
            v = F.params['values']
            axes.append((np.array(v[0:3], float), _unit(v[3:6])))
    if not axes:
        return None
    best, bc = None, -1
    for o, a in axes:
        cnt = sum(1 for o2, a2 in axes if _par(a, a2, 1e-6) and np.linalg.norm(np.cross(o2 - o, a)) < 1e-7)
        if cnt > bc:
            best, bc = (o, a), cnt
    return best


def box_centers(faces, kinds=None):
    out = []
    for F in faces or []:
        if F.box is None or (kinds and F.kind not in kinds):
            continue
        b = np.array(F.box[:6], float)
        out.append(((b[:3] + b[3:]) / 2, F))
    return out


def rot(v, axis, ang):
    k = _unit(axis); v = np.array(v, float)
    return v * math.cos(ang) + np.cross(k, v) * math.sin(ang) + k * (k @ v) * (1 - math.cos(ang))


def pattern_axis_score(o, a, centers, step):
    """how well rotating the instance face centres by +-step maps the set onto itself."""
    if len(centers) < 2:
        return 1e9
    P = np.array(centers)
    tot = 0.0
    for p in P:
        q1 = o + rot(p - o, a, step); q2 = o + rot(p - o, a, -step)
        d = min(np.min(np.linalg.norm(P - q1, axis=1)), np.min(np.linalg.norm(P - q2, axis=1)))
        tot += d
    return tot / len(P)


# ----------------------------------------------------------------------------- planner
class Planner:
    def __init__(self, part, refs=None, log=None, edges=None, curves=None):
        self.part = part
        self.exact_edges = edges or {}
        self.curves = curves or []      # dumps_v4_edges bcurve EdgeRecs (spline recovery)
        self.refs = refs or {}
        self.plans: list[FeatPlan] = []
        self.sketches = {}           # name -> (feature, SketchPlan)
        self.planes = {n: None for n in STD_PLANES}   # name -> (o, x, y, n) of emitted planes
        for n in STD_PLANES:
            o = np.zeros(3); fr = STD_FRAME[n]
            self.planes[n] = (o, np.array(fr[0], float), np.array(fr[1], float), np.array(fr[2], float))
        self.emitted = []            # body feature names emitted (in order)
        self.kinds = {}              # feature -> boss|cut|blend|pattern|mirror|revolve
        self.order = [f.name for f in part.features]

    # --- helpers
    def faces_of(self, f):
        if f.faces:
            return f.faces
        rf = self.refs.get(f.name)
        return [x.surface for x in rf.faces] if rf else []

    def run(self):
        for f in self.part.features:
            if f.idx < 0:
                continue
            fp = self.plan_feature(f)
            if fp is not None:
                if f.suppressed and fp.status == 'EMIT':
                    fp.ops.append(Op('SUPPRESS', [f.name], f.name))
                self.plans.append(fp)
        return self.plans

    def plan_feature(self, f):
        t = f.type
        if t in SILENT_TYPES or t.endswith('Folder'):
            return None
        if t == 'RefPlane':
            if f.name in STD_PLANES:
                return None
            return self.plan_refplane(f)
        if t == 'ProfileFeature':
            return self.plan_sketch(f)
        if t in EXTRUDE_TYPES and f.extrude is not None:
            return self.plan_extrude(f)
        if t in REVOLVE_TYPES:
            return self.plan_revolve(f)
        if t == 'Fillet' or t.startswith('Chamfer'):
            return self.plan_blend(f)
        if t in ('MirrorPattern', 'MirrorSolid'):
            return self.plan_mirror(f)
        if t == 'CirPattern':
            return self.plan_cpattern(f)
        if t == 'LPattern':
            return self.plan_lpattern(f)
        if t in ('Blend', 'BlendCut'):
            return self.plan_loft(f)
        reasons = {'3DProfileFeature': '3D sketch not supported', 'SweepThread': 'thread feature: no definition in dump',
                   'Emboss': 'wrap/emboss: no definition in dump', 'MirrorStock': 'derived mirror part (Insert > Mirror Part): source part file needed',
                   'BaseBody': 'imported body: no feature history', 'Shell': 'shell: removed faces not in dump',
                   'Sweep': 'sweep: path/profile marks not in dump', 'MBimport': 'imported body'}
        return FeatPlan(f.name, t, 'SKIP', reasons.get(t, f'unsupported feature type {t}'),
                        [Op('SKIP', [f.name, t, reasons.get(t, f'unsupported feature type {t}')], f.name)])

    # --- reference planes
    def plan_refplane(self, f):
        g = plane_of(f)
        if g is None:
            return FeatPlan(f.name, f.type, 'SKIP', 'no PLANE line', [Op('SKIP', [f.name, f.type, 'no PLANE line'], f.name)])
        o, x, y, n = g
        own = f.own_dims()
        par = [nm for nm, tp in f.parents if tp == 'RefPlane' and nm in self.planes]
        cands = par + [p for p in STD_PLANES if p not in par] + [p for p in self.planes if p not in par and p not in STD_PLANES]
        op = None
        for pn in cands:
            po, px, py, pnrm = self.planes[pn]
            if not _par(pnrm, n):
                continue
            d = float(np.dot(o - po, _unit(pnrm)))
            dd = abs(d)
            for v in own.values():          # exact dim value when it matches
                if abs(abs(v) - dd) < 1e-9:
                    dd = abs(v)
            if dd < 1e-10:
                op = Op('REFPLANE', [f.name, 'COINCIDENT', pn, 0, 0] + list(n) + list(o), f.name)
            else:
                op = Op('REFPLANE', [f.name, 'OFFSET', pn, dd, d < 0] + list(n) + list(o), f.name)
            op.meta = dict(parent=pn, d=d, intent='parent' if pn in par else 'std')
            break
        if op is None:
            op = Op('REFPLANE', [f.name, '3PT', '', 0, 0] + list(n) + list(o) + list(x) + list(y), f.name)
            op.meta = dict(intent='3pt', angle_dims=own)
        self.planes[f.name] = (o, x, y, n)
        return FeatPlan(f.name, f.type, 'EMIT', op.meta.get('intent', ''), [op], dict(plane=g))

    # --- sketches
    def plan_sketch(self, f):
        if f.sketch is None:
            return FeatPlan(f.name, f.type, 'SKIP', 'no sketch data', [Op('SKIP', [f.name, f.type, 'no sketch data'], f.name)])
        sk = f.sketch
        o, x, y, n = sketch_frame(sk)
        ouv = S.model_to_uv(sk, (0, 0, 0))
        sp = S.analyze(f, (float(ouv[0]), float(ouv[1])) if abs(ouv[2]) < 1e-9 else None, self.curves)
        self.sketches[f.name] = (f, sp)
        ops = []
        # support: coplanar RefPlane parent first, then any known plane, else a model face
        par = [nm for nm, tp in f.parents if tp == 'RefPlane']
        support = None
        for pn in par + [p for p in self.planes if p not in par]:
            if pn in self.planes and coplanar(self.planes[pn][0], self.planes[pn][3], o, n):
                support = ('PLANE', pn); break
        if support is None:
            pts = [S.to_model(sk, e.mid()) for e in sp.ents if e.kind != 'point' and not e.constr] or [o]
            c = np.mean(np.array(pts), 0)
            support = ('FACE', None)
            sup_args = ['FACE', ''] + list(n) + list(o) + list(c)
        else:
            sup_args = ['PLANE', support[1]] + list(n) + list(o) + [0, 0, 0]
        ops.append(Op('SKETCH', [f.name] + sup_args, f.name, dict(support=support)))
        ops.append(Op('SKFRAME', [f.name] + list(x) + list(y) + list(n) + list(o), f.name))
        for e in sp.ents:
            if e.kind == 'line':
                ops.append(Op('LINE', [e.key, e.constr, *e.p0, *e.p1], f.name))
            elif e.kind == 'arc':
                ops.append(Op('ARC', [e.key, e.constr, *e.c, *e.p0, *e.p1, e.dir], f.name))
            elif e.kind == 'circle':
                ops.append(Op('CIRCLE', [e.key, e.constr, *e.c, e.r], f.name))
            elif e.kind == 'spline':
                ops.append(Op('SPLINE', [e.key, e.constr, len(e.through)] + [c for q in e.through for c in q], f.name,
                              dict(src=e.src)))
            elif e.kind == 'point':
                ops.append(Op('POINT', [e.key, *e.p0], f.name))
        for p in sp.merges:
            ops.append(Op('MERGE', [*p], f.name))
        for sg, refs in sp.rels:
            ops.append(Op('REL', [sg, ';'.join(refs)], f.name))
        for d in sp.dims:
            ops.append(Op('DIM', [d['kind'], ';'.join(d['refs']), d['value'], *d['at'], d['name']], f.name))
        for c in sp.contours:
            if c['closed'] and c['keys']:
                ops.append(Op('CONTOUR', [c['index'], ';'.join(c['keys'])], f.name))
        ops.append(Op('ENDSKETCH', [f.name, len(sp.ents), len(sp.rels), len(sp.dims)], f.name))
        st = sp.stats
        reason = (f"ents {st['ents']} (+{st['ents_skipped']} skipped) rels {st['rels_emitted']}/{st['rels_total'] - st['dims_total']}"
                  f" dims {st['dims_emitted']}/{st['dims_in_dump']}")
        return FeatPlan(f.name, f.type, 'EMIT', reason, ops, dict(stats=st, support=support))

    # --- extrudes
    def _sketch_for(self, f):
        skf = self.part.sketch_of(f)
        if skf is None or skf.name not in self.sketches:
            # absorbed sketch only present as a sub-feature: plan it now
            if skf is not None and skf.sketch is not None:
                sp_plan = self.plan_sketch(skf)
                return skf, sp_plan
            return None, None
        return skf, None

    def plan_extrude(self, f):
        e = f.extrude
        skf, extra = self._sketch_for(f)
        if skf is None:
            return FeatPlan(f.name, f.type, 'SKIP', 'sketch not found', [Op('SKIP', [f.name, f.type, 'sketch not found'], f.name)])
        ops = list(extra.ops) if extra else []
        sk = skf.sketch
        _, sp = self.sketches[skf.name]
        o, x, y, n = sketch_frame(sk)
        cut = ('cut' in f.name.lower() and f.type != 'Boss') or f.type in ('Cut', 'CutThin')
        used, how = used_contours(f, skf, sp, n)
        sel = 'ALL' if how in ('ALL', 'NOEVIDENCE', 'NOCONTOUR') else ';'.join(str(c['index']) for c in used)
        sd = not e.both
        t1, t2 = e.end1, e.end2
        d1, d2 = e.d1, e.d2
        if t1 == 9:                         # through all - both (single call, both dirs through all)
            sd, t1, t2 = False, 1, 1
        if t1 == 6:                         # mid plane: SolidWorks takes the full depth in d1
            sd = True
        own = f.own_dims()
        upto = []
        caps = cap_offsets(f, o, _unit(n))
        for which, cond in ((1, t1), (2, t2 if not sd else None)):
            if cond in (3, 4, 5, 7):
                ref = e.upto1 if which == 1 else e.upto2
                if ref is not None and ref.kind == 'plane':
                    upto.append(Op('UPTO', [which, 'PLANE', *ref.params['n'], *ref.params['o']], f.name))
                else:
                    upto.append(Op('UPTO', [which, 'CAPS', ';'.join(fmt(c) for c in caps) or 'none'], f.name,
                                   dict(caps=caps)))
        thin = bool(e.thin)
        thk = 0.0
        if thin:
            others = [v for k, v in own.items() if abs(v - d1) > 1e-12 and abs(v - d2) > 1e-12]
            thk = others[0] if others else 0.0
        draft = e.draft1 or 0.0
        args = [f.name, cut, skf.name, sd, False, e.reverse, t1, t2, d1, d2, abs(draft) > 1e-12, False,
                abs(draft), 0.0, e.merge, thin, thk, sel]
        ops += upto
        ops.append(Op('EXTRUDE', args, f.name, dict(kind='cut' if cut else 'boss', sketch=skf.name, contours=how,
                                                    used=[c['index'] for c in used], caps=caps, n=n)))
        self.emitted.append(f.name); self.kinds[f.name] = 'cut' if cut else 'boss'
        reason = f"{'cut' if cut else 'boss'} end1={e.end1_name} contours={how}"
        if thin and thk == 0.0:
            reason += ' thin thickness unknown'
        return FeatPlan(f.name, f.type, 'EMIT', reason, ops, dict(contours=how, sketch=skf.name))

    # --- revolve
    def plan_revolve(self, f):
        skf, extra = self._sketch_for(f)
        if skf is None:
            return FeatPlan(f.name, f.type, 'SKIP', 'sketch not found', [Op('SKIP', [f.name, f.type, 'sketch not found'], f.name)])
        ops = list(extra.ops) if extra else []
        sk = skf.sketch
        _, sp = self.sketches[skf.name]
        cut = f.type.startswith('RevCut')
        ax = axis_from_faces(f.faces)
        lines = [e for e in sp.ents if e.kind == 'line']
        best = None
        if ax is not None:
            for e in lines:
                a = S.to_model(sk, e.p0); b = S.to_model(sk, e.p1); d = _unit(b - a)
                if _par(d, ax[1], 1e-6) and np.linalg.norm(np.cross(a - ax[0], ax[1])) < 1e-7:
                    if best is None or (e.constr and not best.constr):
                        best = e
        how = 'faces'
        if best is None:
            cl = [e for e in lines if e.constr]
            best = cl[0] if len(cl) == 1 else None
            how = 'single centerline'
        if best is None:
            return FeatPlan(f.name, f.type, 'SKIP', 'revolve axis not found',
                            [Op('SKIP', [f.name, f.type, 'revolve axis not found'], f.name)])
        own = f.own_dims()
        angs = [own[k] for k in sorted(own) if 0 < own[k] <= 2 * math.pi + 1e-9]
        a1 = angs[0] if angs else 2 * math.pi
        a2 = angs[1] if len(angs) > 1 else 0.0
        single = a2 == 0.0
        used, uhow = used_contours_revolve(f, skf, sp)
        sel = 'ALL' if uhow != 'SUBSET' else ';'.join(str(c['index']) for c in used)
        args = [f.name, cut, skf.name, best.key, single, a1, a2, False, True, sel]
        ops.append(Op('REVOLVE', args, f.name, dict(kind='cut' if cut else 'boss', sketch=skf.name, axis_key=best.key,
                                                    a1=a1, a2=a2, used=[c['index'] for c in used])))
        self.emitted.append(f.name); self.kinds[f.name] = 'cut' if cut else 'boss'
        return FeatPlan(f.name, f.type, 'EMIT', f"revolve axis by {how} angle={math.degrees(a1):.1f}", ops)

    # --- fillet / chamfer
    def plan_blend(self, f):
        from dump_parser import blend_params
        bp = blend_params(f)
        if bp is None or bp[1] is None:
            return FeatPlan(f.name, f.type, 'SKIP', 'no blend size', [Op('SKIP', [f.name, f.type, 'no blend size'], f.name)])
        faces = self.faces_of(f)
        boxes = [F.box for F in faces if F.box is not None]
        ex = self.exact_edges.get(f.name)
        if ex:
            # dumps_v4_edges: the blend's own items (exact) or sharp edges derived from its face rails
            # (hints: matched with a blend-size tolerance; rails further apart than the size allows are
            # another feature's edges and dropped)
            lim = 2.5 * bp[1] + 1e-6
            ex = [x for x in ex if not x[0].startswith('derived') or x[5] <= lim]
        if ex:
            tolh = 1.5 * bp[1] + 5e-5
            ops = [Op('EDGE', [k.split(':')[-1].upper(), *s_, *e_, *m_] + ([tolh] if k.startswith('derived') else []), f.name,
                      dict(exact=not k.startswith('derived'), hint=k.startswith('derived')))
                   for k, s_, e_, m_, L, sep in ex]
            ops += [Op('EDGEBOX', [*b[:6]], f.name) for b in boxes[:60]]
        else:
            ops = [Op('EDGEBOX', [*b[:6]], f.name) for b in boxes[:60]]
        own = f.own_dims()
        if bp[0] == 'fillet':
            radii = sorted(set(round(v, 10) for k, v in own.items()))
            note = '' if len(radii) <= 1 else f' multi-radius {radii} -> D1'
            ops.append(Op('FILLET', [f.name, bp[1], len(boxes)], f.name, dict(kind='fillet', size=bp[1])))
            reason = f'fillet r={bp[1] * 1e3:g}mm' + note
        else:
            typ = (f.chamfer or {}).get('type', 1)
            ang = bp[2] if bp[2] is not None else math.pi / 4
            if typ == 2:
                ops.append(Op('CHAMFER', [f.name, 2, bp[1], 0, ang, len(boxes)], f.name, dict(kind='chamfer', size=bp[1])))
            else:
                ops.append(Op('CHAMFER', [f.name, 1, bp[1], ang, 0, len(boxes)], f.name,
                              dict(kind='chamfer', size=bp[1], angle=ang)))
            reason = f'chamfer d={bp[1] * 1e3:g}mm'
        self.emitted.append(f.name); self.kinds[f.name] = 'blend'
        nh = sum(1 for x in (ex or []) if x[0].startswith('derived'))
        src = (f'{len(ex) - nh} exact + {nh} derived edges (dumps_v4_edges)' if ex else 'edges from replay, else face boxes')
        return FeatPlan(f.name, f.type, 'EMIT', reason + f' ({src})', ops, dict(faces=len(faces), exact=bool(ex), v4_edges=len(ex or []), v4_derived=nh))

    # --- mirror
    def plan_mirror(self, f):
        pl = [nm for nm, tp in f.parents if tp == 'RefPlane']
        seeds = [nm for nm, tp in f.parents if tp not in BODY_PARENT_SKIP and nm != f.name and nm in self.emitted]
        seeds.sort(key=lambda s: self.order.index(s) if s in self.order else 0)
        body = f.type == 'MirrorSolid' or not seeds
        if not pl:
            return FeatPlan(f.name, f.type, 'SKIP', 'mirror plane is a face (not dumped)',
                            [Op('SKIP', [f.name, f.type, 'mirror plane is a face (not dumped)'], f.name)])
        g = self.planes.get(pl[0])
        geo = list(g[3]) + list(g[0]) if g is not None else [0, 0, 0, 0, 0, 0]
        ops = [Op('MIRROR', [f.name, pl[0], body, ';'.join(seeds), *geo], f.name,
                  dict(plane=pl[0], seeds=seeds, body=body))]
        self.emitted.append(f.name); self.kinds[f.name] = 'mirror'
        return FeatPlan(f.name, f.type, 'EMIT', f"mirror {'body' if body else 'of ' + ','.join(seeds)} about {pl[0]}", ops)

    # --- patterns
    def _seed_parents(self, f):
        return [nm for nm, tp in f.parents if tp not in BODY_PARENT_SKIP and nm != f.name and nm in self.emitted]

    def plan_cpattern(self, f):
        own = f.own_dims()
        ints = [v for v in own.values() if abs(v - round(v)) < 1e-9 and v >= 2]
        angs = [v for v in own.values() if 0 < v <= 2 * math.pi + 1e-9 and abs(v - round(v)) > 1e-9]
        n = int(round(ints[0])) if ints else None
        ang = angs[0] if angs else 2 * math.pi
        seeds = self._seed_parents(f)
        if not n or not seeds:
            return FeatPlan(f.name, f.type, 'SKIP', 'pattern count/seeds unknown',
                            [Op('SKIP', [f.name, f.type, 'pattern count/seeds unknown'], f.name)])
        eq = abs(ang - 2 * math.pi) < 1e-9
        step = ang / n if eq else ang
        # candidate axes: cyl/cone axes of parents and of the pattern faces, plus std axes
        cands = []
        for nm in seeds:
            a = axis_from_faces(self.part.by_name[nm].faces) if nm in self.part.by_name else None
            if a is not None: cands.append((a, nm))
        a = axis_from_faces(f.faces)
        if a is not None: cands.append((a, None))
        for v in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            cands.append(((np.zeros(3), np.array(v, float)), None))
        centers = [c for c, F in box_centers(f.faces)]
        best = min(cands, key=lambda c: pattern_axis_score(c[0][0], c[0][1], centers, step)) if centers else cands[0]
        (ao, aa), provider = best
        score = pattern_axis_score(ao, aa, centers, step) if centers else float('nan')
        if provider and len(seeds) > 1:
            seeds = [s for s in seeds if s != provider]
        ops = [Op('CPATTERN', [f.name, n, step if not eq else ang, eq, ';'.join(seeds), *ao, *aa], f.name,
                  dict(n=n, ang=ang, eq=eq, seeds=seeds, axis=(ao, aa), score=score))]
        self.emitted.append(f.name); self.kinds[f.name] = 'pattern'
        return FeatPlan(f.name, f.type, 'EMIT', f'circular x{n} {math.degrees(ang):.0f}deg axis fit {score:.2e} m', ops)

    def plan_lpattern(self, f):
        own = f.own_dims()
        items = sorted(own.items())
        ints = [v for k, v in items if abs(v - round(v)) < 1e-9 and v >= 1]
        lens = [v for k, v in items if not (abs(v - round(v)) < 1e-9 and v >= 1)]
        seeds = self._seed_parents(f)
        if not ints or not lens or not seeds:
            return FeatPlan(f.name, f.type, 'SKIP', 'pattern count/spacing/seeds unknown',
                            [Op('SKIP', [f.name, f.type, 'pattern count/spacing/seeds unknown'], f.name)])
        n1 = int(round(ints[0])); n2 = int(round(ints[1])) if len(ints) > 1 else 1
        s1 = lens[0]; s2 = lens[1] if len(lens) > 1 else 0.0
        seedc = [c for nm in seeds if nm in self.part.by_name for c, F in box_centers(self.part.by_name[nm].faces)]
        inst = [c for c, F in box_centers(f.faces)]
        dirs = []
        for s in (s1, s2):
            best = None
            for p in inst:
                for q in seedc:
                    d = p - q; L = np.linalg.norm(d)
                    for kk in range(1, max(n1, n2)):
                        if abs(L - kk * s) < 1e-7:
                            u = d / L
                            if all(not _par(u, x, 1e-6) for x in dirs):
                                best = u; break
                    if best is not None: break
                if best is not None: break
            dirs.append(best)
        if dirs[0] is None:
            return FeatPlan(f.name, f.type, 'SKIP', 'pattern direction not recovered',
                            [Op('SKIP', [f.name, f.type, 'pattern direction not recovered'], f.name)])
        d2 = dirs[1] if (n2 > 1 and dirs[1] is not None) else np.zeros(3)
        if n2 > 1 and dirs[1] is None:
            n2 = 1
        ops = [Op('LPATTERN', [f.name, n1, s1, *dirs[0], n2, s2, *d2, ';'.join(seeds)], f.name,
                  dict(n1=n1, s1=s1, d1=dirs[0], n2=n2, s2=s2, d2=d2, seeds=seeds))]
        self.emitted.append(f.name); self.kinds[f.name] = 'pattern'
        return FeatPlan(f.name, f.type, 'EMIT', f'linear {n1}x{n2}', ops)

    # --- loft
    def plan_loft(self, f):
        profs = [nm for nm, tp in f.parents if tp == 'ProfileFeature']
        profs.sort(key=lambda s: self.order.index(s) if s in self.order else 0)
        profs = [p for p in profs if p in self.sketches]
        if len(profs) < 2:
            return FeatPlan(f.name, f.type, 'SKIP', 'loft profiles not found',
                            [Op('SKIP', [f.name, f.type, 'loft profiles not found'], f.name)])
        cut = f.type == 'BlendCut'
        ops = [Op('LOFT', [f.name, cut, ';'.join(profs)], f.name, dict(kind='cut' if cut else 'boss', profiles=profs))]
        self.emitted.append(f.name); self.kinds[f.name] = 'cut' if cut else 'boss'
        return FeatPlan(f.name, f.type, 'EMIT', f"loft through {len(profs)} profiles (no guides)", ops)


def used_contours_revolve(f, skf, sp):
    closed = [c for c in sp.contours if c['closed'] and c['keys']]
    if len(closed) <= 1:
        return closed, 'ALL'
    return closed, 'ALL'


def plan_part(part, refs=None, edges=None, curves=None):
    pl = Planner(part, refs, edges=edges, curves=curves)
    pl.run()
    return pl
