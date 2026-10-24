"""Sketch analysis (no CAD kernel): turns a dumped sketch into creatable entities with unique keys,
endpoint merges, geometrically verified relations, dimensions matched to the DIM values, and contours.

Everything is in the dump's sketch space (metres, z=0). The VBA side maps (u, v) into the live sketch
through the live ModelToSketchTransform, so the coordinates stay valid even if SolidWorks picks a
different sketch frame on the recreated plane.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

TOL = 1e-8          # metres: coincidence in sketch space
VTOL = 1e-8         # metres / radians: dimension value match

# swConstraintType_e -> SketchAddConstraints string (relations) ; dims handled separately
REL_SG = {4: 'sgHORIZONTAL2D', 5: 'sgVERTICAL2D', 6: 'sgTANGENT', 7: 'sgPARALLEL', 8: 'sgPERPENDICULAR',
          9: 'sgCOINCIDENT', 10: 'sgCONCENTRIC', 11: 'sgSYMMETRIC', 12: 'sgATMIDDLE', 14: 'sgSAMELENGTH',
          17: 'sgFIXED', 25: 'sgHORIZONTALPOINTS2D', 26: 'sgVERTICALPOINTS2D', 27: 'sgCOLINEAR',
          28: 'sgCORADIAL'}
DIM_TYPES = {1: 'distance', 2: 'angle', 3: 'radius', 15: 'diameter'}
REL_NAMES = {0: 'invalid', 13: 'atintersect', 16: 'offsetedge', 32: 'useedge(converted)', 18: 'arcang90',
             19: 'arcang180', 20: 'arcang270', 21: 'arcangtop', 22: 'arcangbottom', 23: 'arcangleft',
             24: 'arcangright', 29: 'snapgrid', 30: 'snaplength', 31: 'snapangle'}


@dataclass
class Ent:
    key: str                 # unique key used in ops ('k0', 'k1', ...)
    kind: str                # line | arc | circle | point | spline | ellipse
    constr: bool
    did: str                 # dump id (not unique in the dumps!)
    p0: Optional[tuple] = None
    p1: Optional[tuple] = None
    c: Optional[tuple] = None
    r: Optional[float] = None
    dir: int = 1
    through: Optional[list] = None   # spline: (u, v) through points, p0 .. p1
    src: str = ''                    # spline: where the geometry came from (v4 bcurve | G1 length fit)

    def pts(self):
        """end points (and centre) usable as sketch points."""
        out = []
        if self.kind in ('line', 'arc', 'spline'):
            out += [self.p0, self.p1]
        if self.kind in ('arc', 'circle'):
            out.append(self.c)
        if self.kind == 'point':
            out.append(self.p0)
        return out

    def length(self):
        if self.kind == 'line':
            return float(np.hypot(self.p1[0] - self.p0[0], self.p1[1] - self.p0[1]))
        if self.kind == 'circle':
            return 2 * math.pi * self.r
        if self.kind == 'arc':
            return self.r * arc_sweep(self)
        if self.kind == 'spline' and self.through:
            q = np.array(self.through)
            return float(np.sum(np.hypot(*np.diff(q, axis=0).T)))
        return 0.0

    def mid(self):
        if self.kind == 'line':
            return ((self.p0[0] + self.p1[0]) / 2, (self.p0[1] + self.p1[1]) / 2)
        if self.kind == 'circle':
            return (self.c[0] + self.r, self.c[1])
        if self.kind == 'arc':
            a0 = math.atan2(self.p0[1] - self.c[1], self.p0[0] - self.c[0])
            am = a0 + self.dir * arc_sweep(self) / 2
            return (self.c[0] + self.r * math.cos(am), self.c[1] + self.r * math.sin(am))
        if self.kind == 'spline' and self.through:
            return tuple(self.through[len(self.through) // 2])
        return tuple(self.p0[:2]) if self.p0 else (0.0, 0.0)


def arc_sweep(e: Ent) -> float:
    a0 = math.atan2(e.p0[1] - e.c[1], e.p0[0] - e.c[0])
    a1 = math.atan2(e.p1[1] - e.c[1], e.p1[0] - e.c[0])
    if e.dir >= 0:
        s = (a1 - a0) % (2 * math.pi)
    else:
        s = (a0 - a1) % (2 * math.pi)
    return s if s > 1e-12 else 2 * math.pi


@dataclass
class SketchPlan:
    name: str
    ents: list = field(default_factory=list)          # Ent, creation order
    merges: list = field(default_factory=list)        # (u, v) locations with >1 end point
    rels: list = field(default_factory=list)          # (sg string, [ref, ...])  ref: 'S:k3' | 'P:u:v' | 'O'
    dims: list = field(default_factory=list)          # dict(kind, refs, value, at=(u,v), name)
    contours: list = field(default_factory=list)      # dict(index, closed, keys)
    stats: dict = field(default_factory=dict)
    skipped_ents: list = field(default_factory=list)  # (did, reason)

    def ent(self, key):
        for e in self.ents:
            if e.key == key:
                return e
        return None


def _p2(p):
    return (float(p[0]), float(p[1]))


def _same(a, b, tol=TOL):
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


def build_entities(sk, name='', curves=None) -> SketchPlan:
    sp = SketchPlan(name)
    k = 0
    for sg in sk.segs:
        kind = sg.kind
        e = None
        if sg.type == 0 and sg.p0 is not None and sg.p1 is not None:
            if np.hypot(sg.p1[0] - sg.p0[0], sg.p1[1] - sg.p0[1]) < 1e-10:
                sp.skipped_ents.append((sg.id, 'zero-length line'))
                continue
            e = Ent(f'k{k}', 'line', sg.construction, sg.id, _p2(sg.p0), _p2(sg.p1))
        elif sg.type == 1 and sg.c is not None and sg.r:
            if sg.is_circle:
                e = Ent(f'k{k}', 'circle', sg.construction, sg.id, c=_p2(sg.c), r=float(sg.r))
            else:
                e = Ent(f'k{k}', 'arc', sg.construction, sg.id, _p2(sg.p0), _p2(sg.p1), _p2(sg.c), float(sg.r),
                        1 if (sg.dir or 1) >= 0 else -1)
        else:
            sp.skipped_ents.append((sg.id, f'{kind}: geometry not in dump'))
            continue
        sp.ents.append(e)
        k += 1
    # splines: the dump has only their length; recover end points from the contour neighbours and the
    # shape from a dumped bcurve with those end points (dumps_v4_edges), else a G1 length fit
    for sg in sk.segs:
        if sg.type != 3 or sg.construction:
            continue
        e = recover_spline(sp, sk, sg, f'k{k}', curves)
        if e is None:
            continue
        sp.skipped_ents[:] = [x for x in sp.skipped_ents if not (x[0] == sg.id and x[1].startswith('spline'))]
        sp.ents.append(e)
        k += 1
    # standalone points: PT lines that are not an end point / centre of a created entity
    allp = [p for e in sp.ents for p in e.pts()]
    for pid, p in sk.points.items():
        q = _p2(p)
        if not any(_same(q, a) for a in allp):
            sp.ents.append(Ent(f'k{k}', 'point', False, pid, q))
            allp.append(q)
            k += 1
    # merges: end points of lines/arcs that coincide
    ends = []
    for e in sp.ents:
        if e.kind in ('line', 'arc', 'spline'):
            ends += [e.p0, e.p1]
    groups = []
    for p in ends:
        for g in groups:
            if _same(g[0], p):
                g.append(p); break
        else:
            groups.append([p])
    sp.merges = [g[0] for g in groups if len(g) > 1]
    return sp


# ----------------------------------------------------------------------------- id resolution
def _cands(sp: SketchPlan, sk, did: str):
    out = [('S', e) for e in sp.ents if e.did == did and e.kind != 'point']
    if did in sk.points:
        out.append(('P', _p2(sk.points[did])))
    for e in sp.ents:
        if e.kind == 'point' and e.did == did:
            out.append(('P', e.p0))
    return out


def _ref(c):
    t, x = c
    if t == 'S':
        return f'S:{x.key}'
    return f'P:{x[0]:.12g}:{x[1]:.12g}'


def _line_dir(e):
    d = np.array(e.p1) - np.array(e.p0)
    return d / np.linalg.norm(d)


def _pt_on(p, e, tol=1e-7):
    p = np.array(p)
    if e.kind == 'line':
        a = np.array(e.p0); d = _line_dir(e)
        v = p - a
        return abs(v[0] * d[1] - v[1] * d[0]) < tol
    if e.kind in ('arc', 'circle'):
        return abs(np.linalg.norm(p - np.array(e.c)) - e.r) < tol
    if e.kind == 'point':
        return _same(p, e.p0, tol)
    return False


def _ptof(c):
    return c[1] if c[0] == 'P' else (c[1].p0 if c[1].kind == 'point' else None)


def verify_rel(t: int, cs: list) -> bool:
    """True when relation type t holds for the resolved candidates cs (so adding it moves nothing)."""
    ss = [x for k, x in cs if k == 'S']
    ps = [x for k, x in cs if k == 'P']
    tol = 1e-7
    try:
        if t == 4:   # horizontal: one line, or two points
            if len(ss) == 1 and ss[0].kind == 'line' and not ps:
                return abs(ss[0].p1[1] - ss[0].p0[1]) < tol
            if len(ps) == 2 and not ss:
                return abs(ps[0][1] - ps[1][1]) < tol
            return False
        if t == 5:
            if len(ss) == 1 and ss[0].kind == 'line' and not ps:
                return abs(ss[0].p1[0] - ss[0].p0[0]) < tol
            if len(ps) == 2 and not ss:
                return abs(ps[0][0] - ps[1][0]) < tol
            return False
        if t == 25:
            return len(ps) == 2 and abs(ps[0][1] - ps[1][1]) < tol
        if t == 26:
            return len(ps) == 2 and abs(ps[0][0] - ps[1][0]) < tol
        if t in (7, 8, 27):
            if len(ss) != 2 or any(s.kind != 'line' for s in ss):
                return False
            a, b = _line_dir(ss[0]), _line_dir(ss[1])
            cr = abs(a[0] * b[1] - a[1] * b[0]); dt = abs(a @ b)
            if t == 7: return cr < 1e-7
            if t == 8: return dt < 1e-7
            return cr < 1e-7 and _pt_on(ss[1].p0, ss[0], tol)
        if t == 9:
            if len(ps) == 2: return _same(ps[0], ps[1], tol)
            if len(ps) == 1 and len(ss) == 1: return _pt_on(ps[0], ss[0], tol)
            return False
        if t == 10:
            if len(ss) == 2 and all(s.kind in ('arc', 'circle') for s in ss):
                return _same(ss[0].c, ss[1].c, tol)
            if len(ss) == 1 and len(ps) == 1 and ss[0].kind in ('arc', 'circle'):
                return _same(ss[0].c, ps[0], tol)
            return False
        if t == 28:
            return len(ss) == 2 and all(s.kind in ('arc', 'circle') for s in ss) and \
                _same(ss[0].c, ss[1].c, tol) and abs(ss[0].r - ss[1].r) < tol
        if t == 14:
            return len(ss) == 2 and abs(_size(ss[0]) - _size(ss[1])) < tol
        if t == 12:
            if len(ps) == 1 and len(ss) == 1 and ss[0].kind == 'line':
                return _same(ps[0], ss[0].mid(), tol)
            return False
        if t == 6:
            if len(ss) != 2: return False
            a, b = ss
            if a.kind == 'line' and b.kind in ('arc', 'circle'): a, b = b, a
            if a.kind in ('arc', 'circle') and b.kind == 'line':
                d = _line_dir(b); v = np.array(a.c) - np.array(b.p0)
                return abs(abs(v[0] * d[1] - v[1] * d[0]) - a.r) < tol
            if a.kind in ('arc', 'circle') and b.kind in ('arc', 'circle'):
                dd = np.linalg.norm(np.array(a.c) - np.array(b.c))
                return abs(dd - (a.r + b.r)) < tol or abs(dd - abs(a.r - b.r)) < tol
            return False
        if t == 11:     # symmetric: two points (or two ents) about a line
            lines = [s for s in ss if s.kind == 'line']
            if len(ps) == 2 and len(lines) == 1:
                L = lines[0]; d = _line_dir(L); a = np.array(L.p0)
                m = (np.array(ps[0]) + np.array(ps[1])) / 2
                v = np.array(ps[1]) - np.array(ps[0])
                return _pt_on(m, L, tol) and abs(v @ d) < tol
            return False
        if t == 17:
            return True
    except Exception:
        return False
    return False


def _size(e):
    if e.kind == 'line': return e.length()
    if e.kind in ('arc', 'circle'): return e.r
    return 0.0


def _choose(t, cand_lists):
    """pick one candidate per entity id such that the relation holds (ids collide between arcs/lines)."""
    import itertools
    if any(not c for c in cand_lists):
        return None
    if np.prod([len(c) for c in cand_lists]) > 64:
        return None
    for combo in itertools.product(*cand_lists):
        if verify_rel(t, list(combo)):
            return list(combo)
    return None


# ----------------------------------------------------------------------------- dimensions
def _dim_candidates(t, cs):
    """[(kind, value)] the dimension could be: kind in AUTO, H, V, RAD, DIA, ANG."""
    ss = [x for k, x in cs if k == 'S']
    ps = [x for k, x in cs if k == 'P']
    out = []
    if t == 3:
        if len(ss) == 1 and ss[0].kind in ('arc', 'circle'): out.append(('RAD', ss[0].r))
    elif t == 15:
        if len(ss) == 1 and ss[0].kind in ('arc', 'circle'): out.append(('DIA', 2 * ss[0].r))
    elif t == 2:
        if len(ss) == 2 and all(s.kind == 'line' for s in ss):
            a, b = _line_dir(ss[0]), _line_dir(ss[1])
            ang = math.acos(max(-1.0, min(1.0, abs(a @ b))))
            out += [('ANG', ang), ('ANG', math.pi - ang)]
    elif t == 1:
        if len(ps) == 2:
            d = np.array(ps[1]) - np.array(ps[0])
            out += [('AUTO', float(np.hypot(*d))), ('H', abs(d[0])), ('V', abs(d[1]))]
        elif len(ss) == 1 and ss[0].kind == 'line' and not ps:
            e = ss[0]; d = np.array(e.p1) - np.array(e.p0)
            out += [('AUTO', e.length()), ('H', abs(d[0])), ('V', abs(d[1]))]
        elif len(ps) == 1 and len(ss) == 1 and ss[0].kind == 'line':
            e = ss[0]; dd = _line_dir(e); v = np.array(ps[0]) - np.array(e.p0)
            out.append(('AUTO', abs(v[0] * dd[1] - v[1] * dd[0])))
        elif len(ss) == 2 and all(s.kind == 'line' for s in ss):
            a, b = ss; da = _line_dir(a)
            if abs(da[0] * _line_dir(b)[1] - da[1] * _line_dir(b)[0]) < 1e-9:
                v = np.array(b.p0) - np.array(a.p0)
                out.append(('AUTO', abs(v[0] * da[1] - v[1] * da[0])))
        elif len(ps) == 1 and len(ss) == 1 and ss[0].kind in ('arc', 'circle'):
            out.append(('AUTO', float(np.linalg.norm(np.array(ps[0]) - np.array(ss[0].c)))))
            d = np.array(ps[0]) - np.array(ss[0].c)
            out += [('H', abs(d[0])), ('V', abs(d[1]))]
        elif len(ss) == 2 and all(s.kind in ('arc', 'circle') for s in ss):
            d = np.array(ss[1].c) - np.array(ss[0].c)
            out += [('AUTO', float(np.hypot(*d))), ('H', abs(d[0])), ('V', abs(d[1]))]
        elif len(ss) == 2:
            L = [s for s in ss if s.kind == 'line']; C = [s for s in ss if s.kind in ('arc', 'circle')]
            if L and C:
                dd = _line_dir(L[0]); v = np.array(C[0].c) - np.array(L[0].p0)
                out.append(('AUTO', abs(v[0] * dd[1] - v[1] * dd[0])))
    return out


def _text_pos(kind, cs, off=0.002):
    ss = [x for k, x in cs if k == 'S']
    ps = [x for k, x in cs if k == 'P']
    if kind in ('RAD', 'DIA') and ss:
        e = ss[0]
        return (e.c[0] + (e.r + off) * 0.7071, e.c[1] + (e.r + off) * 0.7071)
    pts = list(ps) + [s.mid() if s.kind == 'line' else s.c for s in ss if s.kind != 'point']
    if not pts:
        return (0.0, 0.0)
    m = np.mean(np.array(pts, float), 0)
    if kind == 'H':
        return (float(m[0]), float(m[1] + off))
    if kind == 'V':
        return (float(m[0] + off), float(m[1]))
    if len(ss) == 1 and ss[0].kind == 'line' and not ps:
        d = _line_dir(ss[0])
        return (float(m[0] - d[1] * off), float(m[1] + d[0] * off))
    if len(ps) == 2:
        d = np.array(ps[1]) - np.array(ps[0]); n = np.linalg.norm(d)
        if n > 1e-12:
            d = d / n
            return (float(m[0] - d[1] * off), float(m[1] + d[0] * off))
    return (float(m[0] + off), float(m[1] + off))


def analyze(feat, origin_uv=None, curves=None) -> SketchPlan:
    """full analysis of a ProfileFeature (dump_parser.Feature with .sketch). curves: model-space bcurve
    EdgeRecs from dumps_v4_edges (spline recovery)."""
    sk = feat.sketch
    sp = build_entities(sk, feat.name, curves)
    st = dict(rels_total=0, rels_emitted=0, rels_unverified=0, rels_unresolved=0, rels_unsupported=0,
              rels_merged=0, dims_total=0, dims_emitted=0, dims_unmatched=0, origin_rels=0)
    unsupported = {}
    own = {k: v for k, v in feat.own_dims().items()}
    used_dims = set()
    seen = set()
    for t, ids in sk.rels:
        st['rels_total'] += 1
        cl = [_cands(sp, sk, i) for i in ids]
        if t in DIM_TYPES:
            st['dims_total'] += 1
            if any(not c for c in cl):
                st['dims_unmatched'] += 1; continue
            best = None
            import itertools
            combos = list(itertools.product(*cl))[:64]
            for combo in combos:
                for kind, val in _dim_candidates(t, list(combo)):
                    for nm, dv in own.items():
                        if nm in used_dims: continue
                        if abs(dv - val) < max(VTOL, 1e-7 * abs(dv)):
                            best = (kind, val, nm, list(combo)); break
                    if best: break
                if best: break
            if best is None:
                st['dims_unmatched'] += 1; continue
            kind, val, nm, combo = best
            key = ('D', kind, tuple(_ref(c) for c in combo))
            if key in seen:
                continue
            seen.add(key); used_dims.add(nm)
            sp.dims.append(dict(kind=kind, refs=[_ref(c) for c in combo], value=float(own[nm]),
                                at=_text_pos(kind, combo), name=nm))
            st['dims_emitted'] += 1
            continue
        if t not in REL_SG:
            st['rels_unsupported'] += 1
            nm = REL_NAMES.get(t, f'type{t}')
            unsupported[nm] = unsupported.get(nm, 0) + 1
            continue
        # origin coincidence: an unknown point id coincident with a resolved point at the origin
        if t == 9 and origin_uv is not None and sum(1 for c in cl if not c) == 1 and len(ids) == 2:
            known = [c for c in cl if c]
            pts = [x for k, x in known[0] if k == 'P']
            if pts and _same(pts[0], origin_uv, 1e-9):
                sp.rels.append(('sgCOINCIDENT', [_ref(('P', pts[0])), 'O']))
                st['rels_emitted'] += 1; st['origin_rels'] += 1
                continue
        if any(not c for c in cl):
            st['rels_unresolved'] += 1; continue
        combo = _choose(t, cl)
        if combo is None:
            st['rels_unverified'] += 1; continue
        if t == 9 and all(k == 'P' for k, _ in combo):
            st['rels_merged'] += 1; continue          # coincident end points: handled by MERGE ops
        refs = [_ref(c) for c in combo]
        key = (REL_SG[t], tuple(sorted(refs)))
        if key in seen:
            continue
        seen.add(key)
        sp.rels.append((REL_SG[t], refs))
        st['rels_emitted'] += 1
    st['unsupported_kinds'] = unsupported
    st['ents'] = len(sp.ents)
    st['ents_skipped'] = len(sp.skipped_ents)
    st['dims_in_dump'] = len(own)
    # contours
    for c in sk.contours:
        keys = resolve_contour(sp, c.segs)
        sp.contours.append(dict(index=c.index, closed=c.closed, keys=keys))
    sp.stats = st
    return sp


def resolve_contour(sp: SketchPlan, ids: list) -> list:
    """dump seg ids -> entity keys, preferring candidates that chain end to end (ids collide)."""
    cand = [[e for e in sp.ents if e.did == i and e.kind != 'point' and not e.constr] or
            [e for e in sp.ents if e.did == i and e.kind != 'point'] for i in ids]
    if len(ids) == 1:
        c = cand[0]
        closed = [e for e in c if e.kind == 'circle']
        pick = closed or c
        return [pick[0].key] if pick else []
    out = []
    for i, c in enumerate(cand):
        opts = [e for e in c if e.kind != 'circle'] or c
        if not opts:
            continue
        if len(opts) == 1:
            out.append(opts[0]); continue
        nb = [x for j, x in enumerate(cand) if j != i for x in x]
        def score(e):
            return sum(1 for q in (e.p0, e.p1) if q and any(n.kind in ('line', 'arc', 'spline') and
                                                             (_same(q, n.p0, 1e-7) or _same(q, n.p1, 1e-7)) for n in nb))
        out.append(max(opts, key=score))
    return [e.key for e in out]


def to_model(sk, uv):
    R = sk.rot
    return np.array(sk.trans) + sk.scale * (uv[0] * np.array(R[0]) + uv[1] * np.array(R[1]))


def model_to_uv(sk, p):
    """model point -> (u, v, w) in dump sketch space (w = distance from the sketch plane)."""
    R = np.array(sk.rot, float)
    q = (np.array(p, float) - np.array(sk.trans)) / (sk.scale or 1.0)
    return R @ q


# ----------------------------------------------------------------------------- splines
def _free_end(n: Ent, others: list):
    """end point of contour neighbour n that no other contour entity touches (-> (point, other end))."""
    for q, r in ((n.p0, n.p1), (n.p1, n.p0)):
        if not any(o is not n and o.kind in ('line', 'arc') and (_same(q, o.p0, 1e-7) or _same(q, o.p1, 1e-7)) for o in others):
            return q, r
    return None


def _out_dir(n: Ent, q):
    """unit direction leaving neighbour n at its end point q (G1 continuation)."""
    if n.kind == 'line':
        o = n.p1 if _same(q, n.p0, 1e-9) else n.p0
        d = np.subtract(q, o)
    else:
        rad = np.subtract(q, n.c)
        d = np.array([-rad[1], rad[0]])
        if np.dot(d, np.subtract(q, n.mid())) < 0:
            d = -d
    L = np.linalg.norm(d)
    return d / L if L > 0 else None


def _hermite(P0, P1, T0, T1, n=41):
    t = np.linspace(0, 1, n)[:, None]
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1; h10 = t ** 3 - 2 * t ** 2 + t
    h01 = -2 * t ** 3 + 3 * t ** 2; h11 = t ** 3 - t ** 2
    return h00 * P0 + h10 * T0 + h01 * P1 + h11 * T1


def _plen(q):
    return float(np.sum(np.hypot(*np.diff(q, axis=0).T)))


def recover_spline(sp: SketchPlan, sk, sg, key, curves=None):
    """non-construction spline seg -> Ent(kind='spline') or None.
    End points: free end points of its two contour neighbours. Shape: a dumped bcurve (v4 EDGE/BEDGE,
    in the sketch plane, same end points) gives exact through points (start, mid, end); otherwise a cubic
    leaving each neighbour tangentially (G1) whose tangent length is fitted to the dumped spline length,
    sampled at 7 through points (approximation: the dump has no spline control points)."""
    cont = next((c for c in sk.contours if sg.id in c.segs), None)
    if cont is None or len(cont.segs) < 3:
        return None
    i = cont.segs.index(sg.id)
    ids = cont.segs
    def pick(did):
        c = [e for e in sp.ents if e.did == did and e.kind in ('line', 'arc') and not e.constr]
        return c
    others = [x for j, d in enumerate(ids) if j != i for x in pick(d)]
    ends = []
    for did in (ids[i - 1], ids[(i + 1) % len(ids)]):
        got = None
        for n in pick(did):
            fe = _free_end(n, others)
            if fe:
                got = (n, fe[0]); break
        if got is None:
            return None
        ends.append(got)
    (n0, P0), (n1, P1) = ends
    P0 = np.array(P0, float); P1 = np.array(P1, float)
    chord = float(np.linalg.norm(P1 - P0))
    if chord < 1e-9:
        return None
    Ltar = sg.length or 0.0
    # 1) a dumped bcurve with these end points in this sketch plane
    for c in curves or []:
        a = model_to_uv(sk, c.s); b = model_to_uv(sk, c.e); m = model_to_uv(sk, c.m)
        if max(abs(a[2]), abs(b[2]), abs(m[2])) > 1e-7:
            continue
        for A, B_ in ((a, b), (b, a)):
            if np.linalg.norm(A[:2] - P0) < 1e-6 and np.linalg.norm(B_[:2] - P1) < 1e-6:
                if Ltar and c.L and abs(c.L - Ltar) > 1e-6 * max(1.0, Ltar * 1e3):
                    continue
                if not c.mid_ok:
                    continue
                if getattr(c, 'samples', ()) and len(c.samples) >= 3:
                    q = [model_to_uv(sk, x)[:2] for x in c.samples]
                    if np.linalg.norm(q[0] - P0) > np.linalg.norm(q[-1] - P0):
                        q = q[::-1]
                    th = [tuple(P0)] + [tuple(map(float, x)) for x in q[1:-1]] + [tuple(P1)]
                    return Ent(key, 'spline', False, sg.id, tuple(P0), tuple(P1), through=th,
                               src=f'v4 bcurve samples ({len(th)} pts)')
                th = [tuple(P0), tuple(m[:2]), tuple(P1)]
                return Ent(key, 'spline', False, sg.id, tuple(P0), tuple(P1), through=th, src='v4 bcurve s/m/e')
    # 2) G1 length fit
    T0 = _out_dir(n0, tuple(P0)); T1 = _out_dir(n1, tuple(P1))
    if T0 is None or T1 is None:
        return None
    T1 = -T1              # arriving direction at P1
    if not Ltar or Ltar <= chord * (1 + 1e-9):
        k_ = 0.0
    else:
        lo, hi = 0.0, 4.0
        if _plen(_hermite(P0, P1, hi * chord * T0, hi * chord * T1)) < Ltar:
            return None
        for _ in range(80):
            k_ = (lo + hi) / 2
            if _plen(_hermite(P0, P1, k_ * chord * T0, k_ * chord * T1, 201)) < Ltar:
                lo = k_
            else:
                hi = k_
        k_ = (lo + hi) / 2
    q = _hermite(P0, P1, k_ * chord * T0, k_ * chord * T1, 7)
    th = [tuple(map(float, x)) for x in q]
    th[0] = tuple(P0); th[-1] = tuple(P1)
    return Ent(key, 'spline', False, sg.id, tuple(P0), tuple(P1), through=th,
               src=f'G1 length fit (k={k_:.3f}, len {Ltar * 1e3:.4f} mm; approx: no spline points in dump)')
