"""build123d replay of a plan (validation without SolidWorks).

For every emitted body feature it computes the body the macro should produce, so the macro can log
'expected' volumes per step, and it resolves what the dump leaves implicit:
    * fillet/chamfer edges  -> EDGE ops (type, start, end, mid in model metres) for the live-edge matcher
    * up-to / offset faces  -> UPTO PLANE ops (the planar face the extent ends on)
    * revolve direction     -> picked by the feature's FACE bounding boxes
Units: build123d works in mm here; ops stay in metres.
"""
from __future__ import annotations
import math, time, traceback

import numpy as np

from .plan import Op, _unit, _par, cap_offsets, sketch_frame
from . import sketch as S

MM = 1000.0
BIG = 400.0
_B = None


def _b():
    global _B
    if _B is None:
        import build123d as b
        _B = b
    return _B


def vol(s):
    try:
        return float(s.volume) if s is not None else 0.0
    except Exception:
        return 0.0


def _solid(x):
    b = _b()
    if x is None:
        return None
    try:
        sols = x.solids()
    except Exception:
        return x
    if not sols:
        return None
    if len(sols) == 1:
        return sols[0]
    return b.Compound(list(sols))


def bop(a, t, op):
    if a is None:
        return _solid(t) if op == 'fuse' else None
    if t is None:
        return a
    r = {'fuse': a.fuse, 'cut': a.cut, 'common': a.intersect}[op](t)
    try:
        r = r.clean()
    except Exception:
        pass
    return _solid(r)


def ent_edge(e: S.Ent, sk):
    """sketch entity -> build123d Edge in model space (mm)."""
    b = _b()
    P = lambda uv: b.Vector(*(S.to_model(sk, uv) * MM))
    if e.kind == 'line':
        return b.Edge.make_line(P(e.p0), P(e.p1))
    if e.kind == 'arc':
        return b.Edge.make_three_point_arc(P(e.p0), P(e.mid()), P(e.p1))
    if e.kind == 'circle':
        n = np.array(sk.rot[2], float)
        c = S.to_model(sk, e.c) * MM
        x = np.array(sk.rot[0], float)
        return b.Edge.make_circle(e.r * MM, b.Plane(origin=tuple(c), x_dir=tuple(x), z_dir=tuple(n)))
    if e.kind == 'spline' and e.through:
        return b.Edge.make_spline([P(q) for q in e.through])
    return None


def contour_face(sp, keys, sk):
    b = _b()
    edges = [ent_edge(sp.ent(k), sk) for k in keys if sp.ent(k) is not None]
    edges = [e for e in edges if e is not None]
    if not edges:
        return None
    try:
        ws = list(b.Wire.combine(edges))
        w = max(ws, key=lambda x: len(x.edges()))
        return b.Face(w)
    except Exception:
        try:
            return b.Face(b.Wire(edges))
        except Exception:
            return None


def region(sp, sk, contour_idx=None):
    """even-odd region of the selected closed contours (None = all closed contours)."""
    faces = []
    for c in sp.contours:
        if not c['closed'] or not c['keys']:
            continue
        if contour_idx is not None and c['index'] not in contour_idx:
            continue
        f = contour_face(sp, c['keys'], sk)
        if f is not None and f.area > 1e-9:
            faces.append(f)
    if not faces:
        return None
    R = faces[0]
    for f in faces[1:]:
        try:
            a = R.cut(f); bb = f.cut(R)
            R = a.fuse(bb) if a is not None and len(a.faces()) else bb
        except Exception:
            R = R.fuse(f)
    return R


def sketch_cells_mm(sp, sk):
    """bounded planar cells of all non-construction entities (model space, mm)."""
    b = _b()
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Splitter
    from OCP.collections import List_TopoDS_Shape as TopTools_ListOfShape
    edges = [ent_edge(e, sk) for e in sp.ents if not e.constr and e.kind in ('line', 'arc', 'circle', 'spline')]
    edges = [e for e in edges if e is not None]
    if not edges:
        return []
    o, x, y, n = sketch_frame(sk)
    uv = np.array([S.model_to_uv(sk, np.array(tuple(v)) / MM)[:2] for E in edges for v in (E.position_at(0), E.position_at(0.5), E.position_at(1))])
    lo = uv.min(0) * MM - 5; hi = uv.max(0) * MM + 5
    c = (lo + hi) / 2
    pl = b.Plane(origin=tuple(o * MM + x * c[0] + y * c[1]), x_dir=tuple(x), z_dir=tuple(n))
    big = b.Face.make_rect(hi[0] - lo[0], hi[1] - lo[1], pl)
    sp_ = BRepAlgoAPI_Splitter(); a = TopTools_ListOfShape(); a.Append(big.wrapped); t = TopTools_ListOfShape()
    for e in edges: t.Append(e.wrapped)
    sp_.SetArguments(a); sp_.SetTools(t); sp_.Build()
    cells = []
    bb_area = (hi[0] - lo[0]) * (hi[1] - lo[1])
    for fc in b.Compound(sp_.Shape()).faces():
        q = np.array([S.model_to_uv(sk, np.array(tuple(v)) / MM)[:2] * MM for v in fc.vertices()]) if fc.vertices() else None
        touches = False
        if q is not None and len(q):
            touches = bool(np.any(q[:, 0] < lo[0] + 1e-6) or np.any(q[:, 1] < lo[1] + 1e-6) or
                           np.any(q[:, 0] > hi[0] - 1e-6) or np.any(q[:, 1] > hi[1] - 1e-6))
        if touches or fc.area < 1e-6 or fc.area > 0.999 * bb_area:
            continue
        cells.append(fc)
    return cells


def _on_face(p, F, tol=2e-3):
    """point p (mm) on dumped FACE F (metres) and inside its box."""
    if F.box is not None:
        lo = np.array(F.box[:3]) * MM - 0.05; hi = np.array(F.box[3:6]) * MM + 0.05
        if np.any(p < lo) or np.any(p > hi):
            return False
    if F.kind == 'plane':
        nn = _unit(F.params['n']); o = np.array(F.params['o']) * MM
        return abs(np.dot(p - o, nn)) < tol
    if F.kind == 'cyl':
        ax = _unit(F.params['ax']); o = np.array(F.params['o']) * MM
        v = p - o; v = v - ax * np.dot(v, ax)
        return abs(np.linalg.norm(v) - F.params['r'] * MM) < tol
    if F.kind == 'cone' and len(F.params.get('values', [])) >= 8:
        vv = F.params['values']; c = np.array(vv[0:3]) * MM; ax = _unit(vv[3:6]); r0 = vv[6] * MM; ha = vv[7]
        w = p - c; h = w @ ax; rad = np.linalg.norm(w - ax * h)
        return abs(rad - (r0 + h * math.tan(ha))) < tol or abs(rad - (r0 - h * math.tan(ha))) < tol
    return False


def label_cells(cells, faces, dvec, ivs):
    """choose the cells whose union's boundary best explains the feature's side FACEs.
    -> (list of chosen indices, score info)"""
    if not cells:
        return [], {}
    zs = []
    for lo, hi in ivs:
        lo2, hi2 = max(lo, -60.0), min(hi, 60.0)
        if hi2 - lo2 > 1e-6:
            zs += [lo2 + u * (hi2 - lo2) for u in (0.2, 0.5, 0.8)]
    side = [F for F in faces if not (F.kind == 'plane' and _par(F.params['n'], dvec, 1e-6))]
    # edges keyed by midpoint
    emap = {}
    for i, c in enumerate(cells):
        for E in c.edges():
            m = np.array(tuple(E.position_at(0.5)))
            k = tuple(np.round(m, 4))
            ent = emap.setdefault(k, dict(m=m, L=E.length, cells=set(), face=None,
                                          ps=[np.array(tuple(E.position_at(t))) for t in (0.1, 0.3, 0.5, 0.7, 0.9)]))
            ent['cells'].add(i)
    def zs_for(F, m):
        out = list(zs)
        if F.box is not None:
            bx = np.array(F.box[:6], float) * MM
            corners = np.array([[bx[i], bx[1 + j], bx[2 + k]] for i in (0, 3) for j in (0, 3) for k in (0, 3)])
            pr = (corners - m) @ dvec
            for u in (0.25, 0.5, 0.75):
                z = pr.min() + u * (pr.max() - pr.min())
                if any(lo - 1e-6 <= z <= hi + 1e-6 for lo, hi in ivs):
                    out.append(z)
        return out
    for k, ent in emap.items():
        ent['face'] = any(_on_face(p + dvec * z, F) for F in side for p in ent['ps'] for z in zs_for(F, p))
    E = list(emap.values())
    n = len(cells)
    def score(U):
        s = 0.0
        for ent in E:
            inside = sum(1 for i in ent['cells'] if i in U)
            bnd = (inside == 1 and len(ent['cells']) == 2) or (inside == 1 and len(ent['cells']) == 1)
            if ent['face'] and bnd: s += ent['L']
            elif ent['face'] and not bnd: s -= 1.0 * ent['L']
            elif bnd: s -= 0.3 * ent['L']
        return s
    best = None
    if n <= 14:
        import itertools
        for r in range(1, n + 1):
            for U in itertools.combinations(range(n), r):
                sc = score(set(U))
                if best is None or sc > best[0] + 1e-9:
                    best = (sc, set(U))
    else:
        U = {i for i, c in enumerate(cells)}
        sc = score(U); improved = True
        while improved:
            improved = False
            for i in range(n):
                V = U ^ {i}
                if not V: continue
                s2 = score(V)
                if s2 > sc + 1e-9:
                    U, sc, improved = V, s2, True
        best = (sc, U)
    nf = sum(1 for e in E if e['face'])
    return sorted(best[1]), dict(score=round(best[0], 3), edges=len(E), face_edges=nf)


def outline_ops(R, sk, name, sketch_op):
    """ops for a profile sketch drawing only the boundary of region R (build123d face(s), mm)."""
    ops = [Op('SKETCH', [name] + list(sketch_op.args[1:]), name, dict(profile=True)),
           Op('SKFRAME', [name] + list(np.array(sk.rot[0])) + list(np.array(sk.rot[1])) + list(np.array(sk.rot[2])) + list(np.array(sk.trans)), name)]
    k = 0
    ends = []
    uv = lambda v: S.model_to_uv(sk, np.array(tuple(v)) / MM)[:2]
    for E in R.edges():
        gt = str(E.geom_type).split('.')[-1]
        a, m, c = uv(E.position_at(0)), uv(E.position_at(0.5)), uv(E.position_at(1))
        if gt == 'LINE':
            ops.append(Op('LINE', [f'p{k}', False, *a, *c], name)); ends += [tuple(a), tuple(c)]
        elif gt == 'CIRCLE':
            cc = uv(E.arc_center); r = E.radius / MM
            if np.linalg.norm(a - c) < 1e-9:
                ops.append(Op('CIRCLE', [f'p{k}', False, *cc, r], name))
            else:
                # SolidWorks CreateArc direction: +1 counter-clockwise. a -> m -> c is CCW when m lies to the
                # right of the chord a -> c (cross(m - a, c - a) > 0). (Was inverted: every outline arc took the
                # long way round and the profile sketch was invalid.)
                cr = (m[0] - a[0]) * (c[1] - a[1]) - (m[1] - a[1]) * (c[0] - a[0])
                d = 1 if cr > 0 else -1
                ops.append(Op('ARC', [f'p{k}', False, *cc, *a, *c, d], name)); ends += [tuple(a), tuple(c)]
        else:
            # never approximate curves: an outline needing a non line/arc edge is not emitted
            raise RuntimeError(f'outline edge type {gt} cannot be drawn exactly')
        k += 1
    groups = []
    for p in ends:
        for g in groups:
            if abs(g[0][0] - p[0]) < 1e-9 and abs(g[0][1] - p[1]) < 1e-9:
                g.append(p); break
        else:
            groups.append([p])
    ops += [Op('MERGE', [*g[0]], name) for g in groups if len(g) > 1]
    ops.append(Op('ENDSKETCH', [name, k, 0, 0], name))
    return ops


def _area(x):
    try:
        return float(x.area) if x is not None else 0.0
    except Exception:
        return 0.0


def same_region(A, B, tol=1e-3):
    if A is None or B is None:
        return False
    try:
        d = _area(A.cut(B)) + _area(B.cut(A))
    except Exception:
        return False
    return d < tol * max(_area(A), 1e-9) + 1e-6


class Replay:
    def __init__(self, part, planner, log=print, oracle=None, ref=None, dsel=None):
        self.part = part
        self.oracle = oracle or {}      # feature -> dict(body=, tools=) from a reference-driven run (ckpt)
        self.ref = ref                  # refmesh.RefMesh of the final part (choice only, never geometry)
        self.dsel = dsel or {}          # chooser.selections(): decoder region choice per sketch id
        self.pl = planner
        self.body = None
        self.tools = {}            # feature -> (kind, solid) for patterns/mirrors
        self.vols = {}             # feature -> m3 after the feature
        self.status = {}           # feature -> OK | FAIL:... | SKIP
        self.edges = {}            # blend feature -> [(type, start, end, mid)] metres
        self.log = log
        self.t0 = time.time()

    # ------------------------------------------------------------------ driver
    def run(self, time_budget=600.0):
        for fp in self.pl.plans:
            if fp.status != 'EMIT':
                continue
            f = self.part.by_name.get(fp.name)
            if f is None or f.suppressed:
                continue
            main = [o for o in fp.ops if o.kind in ('EXTRUDE', 'REVOLVE', 'FILLET', 'CHAMFER', 'MIRROR',
                                                     'CPATTERN', 'LPATTERN', 'LOFT')]
            if not main:
                continue
            if time.time() - self.t0 > time_budget:
                self.status[fp.name] = 'SKIP:time budget'
                continue
            op = main[-1]
            prev = self.body
            pv = vol(prev) if prev is not None else 0.0
            try:
                getattr(self, 'do_' + op.kind.lower())(f, fp, op)
                if fp.name not in self.status:
                    self.status[fp.name] = 'OK'
            except Exception as ex:
                self.status[fp.name] = f'FAIL:{type(ex).__name__}: {ex}'[:160]
            # boolean sanity: an add that loses material, or a cut/blend that wipes the body, is an OCC
            # boolean failure in the replay, not the design intent -> keep the previous body
            if prev is not None:
                nv = vol(self.body) if self.body is not None else 0.0
                adds = op.kind in ('EXTRUDE', 'REVOLVE', 'LOFT') and op.meta.get('kind', 'boss') != 'cut'
                if (adds and nv < pv - 1e-3 * max(pv, 1)) or nv < 0.05 * pv:
                    self.status[fp.name] = f'FAIL:replay boolean sanity ({pv:.0f}->{nv:.0f} mm3), previous body kept'
                    self.body = prev
            if fp.name in self.oracle and self.oracle[fp.name].get('body') is not None:
                ob = self.oracle[fp.name]['body']
                d = abs(vol(ob) - vol(self.body))
                if d > 1e-3 * max(vol(ob), 1):
                    self.status[fp.name] = (self.status.get(fp.name, 'OK') + f' |oracle diff {d:.1f}mm3, synced')[:200]
                self.body = ob
            self.vols[fp.name] = vol(self.body) / MM ** 3
        return self

    # ------------------------------------------------------------------ extrude
    def do_extrude(self, f, fp, op):
        b = _b()
        e = f.extrude
        m = op.meta
        skf = self.part.by_name.get(m['sketch']) or self.part.sketch_of(f)
        _, sp = self.pl.sketches[m['sketch']]
        sk = skf.sketch
        o, x, y, n = sketch_frame(sk)
        n = _unit(n)
        sel = None if op.args[-1] == 'ALL' else [int(i) for i in str(op.args[-1]).split(';')]
        cut = m['kind'] == 'cut'
        s = (-1 if cut else 1) * (-1 if e.reverse else 1)
        dvec = n * s
        caps = [c * s for c in m.get('caps', [])]      # plan caps are along the sketch normal
        omm = o * MM

        def plane_offs():
            out = []
            if self.body is None:
                return out
            for fc in self.body.faces():
                try:
                    if fc.geom_type.name != 'PLANE' and str(fc.geom_type).split('.')[-1] != 'PLANE':
                        continue
                    nn = np.array(tuple(fc.normal_at()))
                    if abs(abs(nn @ dvec) - 1) > 1e-6:
                        continue
                    out.append(float((np.array(tuple(fc.center())) - omm) @ dvec))
                except Exception:
                    pass
            return sorted(set(round(v, 6) for v in out))

        def side(cond, d, sign):
            """(lo, hi) in mm along sign*dvec, plus chosen target plane offset (mm along dvec) or None."""
            dd = d * MM
            if cond == 0: return (0.0, dd), None
            if cond in (1, 9):
                if not cut and self.body is not None:
                    # Through All on a boss: through the existing body only (its far extent)
                    bb = self.body.bounding_box()
                    C = np.array([[x, y, z] for x in (bb.min.X, bb.max.X) for y in (bb.min.Y, bb.max.Y) for z in (bb.min.Z, bb.max.Z)])
                    far = float(((C - omm) @ (sign * dvec)).max())
                    if far > 1e-6:
                        return (0.0, far), None
                return (0.0, BIG), None
            if cond == 6: return (-dd / 2, dd / 2), None
            cs = sorted({sign * c * MM for c in caps if sign * c * MM > 1e-6})
            offs = sorted({sign * v for v in plane_offs() if sign * v > 1e-6})
            if cond in (3, 4, 7) and self.ref is not None:
                tgt = ref_extent(sorted(set(cs) | set(offs)), sign)
                if tgt is not None:
                    m.setdefault('ref_extent', []).append(round(sign * tgt, 3))
                    return (0.0, tgt), sign * tgt
            if cond == 2:
                h = next_hit(sign)
                if h is not None:
                    m.setdefault('next_hit', []).append(round(sign * h, 3))
                    return (0.0, h), sign * h
                tgt = offs[0] if offs else (cs[0] if cs else dd)
                return (0.0, tgt), sign * tgt
            if cond in (3, 4, 7):
                tgt = cs[-1] if cs else (offs[0] if offs else dd)
                return (0.0, tgt), sign * tgt
            if cond == 5:
                if cs:
                    tgt = cs[-1]
                    face = min(offs, key=lambda v: min(abs(v - (tgt + dd)), abs(v - (tgt - dd)))) if offs else tgt + dd
                    return (0.0, tgt), sign * face
                if offs:
                    return (0.0, max(offs[0] - dd, 1e-3)), sign * offs[0]
                return (0.0, dd), None
            return (0.0, dd), None

        def next_hit(sign):
            """Up To Next: first body face met by rays from the profile along sign*dvec (largest of the
            per-ray first hits, so the whole profile reaches the next surface)."""
            if self.body is None:
                return None
            try:
                from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
                from OCP.gp import gp_Lin, gp_Pnt, gp_Dir
                R0 = region(sp, sk, sel)
                P = _cell_points(R0, 16) if R0 is not None else None
                if P is None or not len(P):
                    return None
                it = IntCurvesFace_ShapeIntersector(); it.Load(self.body.wrapped, 1e-6)
                d = sign * dvec
                firsts = []
                for p in P:
                    it.Perform(gp_Lin(gp_Pnt(*p), gp_Dir(*d)), 1e-6, 1e4)
                    ws = sorted(it.WParameter(k) for k in range(1, it.NbPnt() + 1) if it.WParameter(k) > 1e-6)
                    if ws:
                        firsts.append(ws[0])
                if len(firsts) < max(1, len(P) // 2):
                    return None
                return float(max(firsts))
            except Exception:
                return None

        def ref_extent(cands, sign):
            """reference choice of an up-to extent: walk the candidate stop planes outward and stop
            where the swept profile stops being material (boss) / void (cut) in the reference."""
            if not cands:
                return None
            try:
                R0 = region(sp, sk, sel)
                P = _cell_points(R0, 12) if R0 is not None else None
            except Exception:
                P = None
            if P is None or not len(P):
                return None
            best, z0 = None, 0.0
            for c in cands:
                zs = np.linspace(z0, c, 5)[1:-1]
                Q = (P[:, None, :] + (sign * dvec)[None, None, :] * zs[None, :, None]).reshape(-1, 3)
                fin = float(self.ref.inside(Q).mean())
                good = fin >= 0.5 if not cut else fin <= 0.5
                if not good:
                    break
                best, z0 = c, c
            return best

        ivs = []
        targets = []
        t1 = e.end1
        if t1 == 9:
            ivs = [(-BIG, BIG)]
        else:
            (lo, hi), tg = side(t1, e.d1, 1)
            if t1 in (2, 3, 4, 5, 7) and hi - lo < 1e-9 and not e.both:
                # nothing to reach on this side: the up-to reference lies the other way (SolidWorks
                # resolves the side itself; only the replay needs the flip)
                dvec = -dvec
                caps = [-c for c in caps]
                (lo, hi), tg = side(t1, e.d1, 1)
                m['replay_dir_flipped'] = True
            ivs.append((lo, hi)); targets.append((1, tg))
            if e.both and t1 != 6:
                (lo2, hi2), tg2 = side(e.end2, e.d2, -1)
                ivs.append((-hi2, -lo2)); targets.append((2, tg2))
        R = self.choose_region(f, fp, op, sp, sk, skf, sel, dvec, ivs)
        if R is None:
            raise RuntimeError('no profile region')
        tool = None
        for lo, hi in ivs:
            if hi - lo < 1e-9:
                continue
            fc = R.moved(b.Location(tuple(dvec * lo)))
            T = b.extrude(fc, amount=hi - lo, dir=tuple(dvec))
            tool = T if tool is None else tool.fuse(T)
        if tool is None:
            raise RuntimeError('empty extent')
        tool = _solid(tool)
        self.tools[f.name] = ('cut' if cut else 'boss', tool)
        self.body = bop(self.body, tool, 'cut' if cut else 'fuse')
        # resolved up-to target planes -> rewrite the UPTO ops
        new = []
        for o2 in fp.ops:
            if o2.kind == 'UPTO':
                which = int(o2.args[0])
                tg = dict(targets).get(which)
                if tg is not None and o2.args[1] == 'CAPS':
                    p = o + dvec * (tg / MM)
                    sgn = 1 if which == 1 else -1
                    o2 = Op('UPTO', [which, 'PLANE', *(dvec * sgn), *p], o2.feat, dict(replay=True))
            new.append(o2)
        fp.ops[:] = new
        op.meta['ivs'] = ivs

    def choose_region(self, f, fp, op, sp, sk, skf, sel, dvec, ivs):
        """profile region: whole sketch / contour subset / outline of evidence-chosen cells."""
        b = _b()
        R_all = region(sp, sk, None)
        R_sel = region(sp, sk, sel) if sel is not None else R_all
        try:
            cells = sketch_cells_mm(sp, sk)
        except Exception:
            cells = []
        if not cells:
            op.meta['profile'] = 'contours'
            return R_sel
        # evidence: the feature's own faces plus every surviving face of the final part (a sketch edge that
        # sweeps onto a surviving face must bound the new material, else that face would be consumed)
        allf = list(f.faces or [])
        if op.meta.get('kind') == 'boss':
            allf += [F for g in self.part.features if g.idx >= 0 and g.name != f.name for F in (g.faces or [])]
        ot = (self.oracle.get(f.name) or {}).get('tools', {}).get(f.name)
        if ot is not None:
            idx, info = oracle_cells(cells, ot[1], dvec, ivs)
        elif self.ref is not None:
            idx, info = ref_cells(cells, self.ref, dvec, ivs, op.meta.get('kind'))
            if info.get('ambiguous'):
                # undecided cells take the face-evidence label
                fidx, finfo = label_cells(cells, allf, dvec, ivs)
                idx = sorted(set(idx) | (set(fidx) & set(info['ambiguous'])))
        elif skf.id in self.dsel:
            # decoder chooser only breaks ties: used when the faces give no evidence
            idx, info = label_cells(cells, allf, dvec, ivs)
            if not info.get('face_edges'):
                R = decoder_region(sp, sk, self.dsel[skf.id], op)
                if R is not None:
                    return R
        else:
            idx, info = label_cells(cells, allf, dvec, ivs)
        if not idx:
            idx, info = label_cells(cells, allf, dvec, ivs)
        op.meta['cells'] = dict(total=len(cells), used=len(idx), **info)
        if not info.get('face_edges'):
            # no side-face evidence: whole sketch (SolidWorks default) when it has closed contours
            if R_all is not None:
                op.meta['profile'] = 'ALL(no evidence)'
                return R_all
            idx = list(range(len(cells)))
        Rc = cells[idx[0]]
        for i in idx[1:]:
            Rc = Rc.fuse(cells[i])
        try:
            Rc = Rc.clean()
        except Exception:
            pass
        if same_region(Rc, R_all):
            if op.args[-1] != 'ALL':
                op.args[-1] = 'ALL'
            op.meta['profile'] = 'ALL'
            return R_all
        if sel is not None and same_region(Rc, R_sel):
            op.meta['profile'] = 'SUBSET'
            return R_sel
        # closed-contour subset that reproduces the chosen cells?
        closed = [c for c in sp.contours if c['closed'] and c['keys']]
        if 0 < len(closed) <= 10:
            import itertools
            for r in range(1, len(closed) + 1):
                for sub in itertools.combinations(closed, r):
                    ii = [c['index'] for c in sub]
                    Rs = region(sp, sk, ii)
                    if same_region(Rc, Rs):
                        op.args[-1] = ';'.join(str(i) for i in ii)
                        op.meta['profile'] = 'SUBSET'
                        return Rs
        # outline profile sketch (proven fallback from the RV01 generator)
        pname = f"{skf.name}-profile-{f.name}"
        sop = next((o for p in self.pl.plans for o in p.ops if o.kind == 'SKETCH' and o.args[0] == skf.name), None)
        if sop is None:
            op.meta['profile'] = 'ALL(no sketch op)'
            return R_all or Rc
        ol = outline_ops(Rc, sk, pname, sop)
        i = fp.ops.index(op)
        while i > 0 and fp.ops[i - 1].kind == 'UPTO':
            i -= 1
        fp.ops[i:i] = ol
        op.args[2] = pname
        op.args[-1] = 'ALL'
        op.meta['profile'] = f'OUTLINE({len(idx)}/{len(cells)} cells)'
        return Rc

    # ------------------------------------------------------------------ revolve
    def do_revolve(self, f, fp, op):
        b = _b()
        m = op.meta
        skf = self.part.by_name.get(m['sketch'])
        _, sp = self.pl.sketches[m['sketch']]
        sk = skf.sketch
        R = region(sp, sk, None)
        if R is None:
            # open contours: the profile closes through other segments -> faces of the sketch arrangement
            try:
                cells = sketch_cells_mm(sp, sk)
            except Exception:
                cells = []
            if cells:
                if self.ref is not None:
                    e0 = sp.ent(m['axis_key'])
                    a0 = S.to_model(sk, e0.p0) * MM; c0 = S.to_model(sk, e0.p1) * MM
                    keep = [c for c in cells if ref_cell_on_revolve(self.ref, c, a0, _unit(c0 - a0), m.get('kind') == 'cut')]
                    cells = keep or cells
                R = cells[0]
                for c in cells[1:]:
                    R = R.fuse(c)
                try:
                    R = R.clean()
                except Exception:
                    pass
                op.meta['profile'] = f'cells({len(cells)})'
        if R is None:
            raise RuntimeError('no profile region')
        e = sp.ent(m['axis_key'])
        nclosed = sum(1 for c in sp.contours if c['closed'] and c['keys'])
        if str(op.meta.get('profile', '')).startswith('cells') or nclosed > 1:
            # SolidWorks cannot revolve a whole sketch whose regions share edges / close through other
            # segments: draw the region outline + the axis in a profile sketch (as for extrudes)
            sop = next((o for p_ in self.pl.plans for o in p_.ops if o.kind == 'SKETCH' and o.args[0] == skf.name), None)
            if sop is not None:
                pname = f"{skf.name}-profile-{f.name}"
                try:
                    ol = outline_ops(R, sk, pname, sop)
                    ol.insert(-1, Op('LINE', ['ax', True, *e.p0, *e.p1], pname))
                    i = fp.ops.index(op)
                    fp.ops[i:i] = ol
                    op.args[2] = pname; op.args[3] = 'ax'; op.args[-1] = 'ALL'
                    op.meta['profile'] = f"OUTLINE({op.meta.get('profile', 'contours')})"
                except RuntimeError:
                    pass
        a = S.to_model(sk, e.p0) * MM; c = S.to_model(sk, e.p1) * MM
        ax = b.Axis(tuple(a), tuple(_unit(c - a)))
        a1 = math.degrees(m['a1']); a2 = math.degrees(m['a2'] or 0)
        cands = []
        for sgn in ((1,) if a1 >= 359.999 else (1, -1)):
            try:
                T = b.revolve(R, ax, sgn * min(a1, 360.0))
                if a2 > 0:
                    T = T.fuse(b.revolve(R, ax, -sgn * a2))
                cands.append((sgn, _solid(T)))
            except Exception:
                pass
        if not cands:
            raise RuntimeError('revolve failed')
        boxes = [F.box for F in f.faces if F.box is not None]
        if len(cands) > 1 and boxes:
            B = np.array(boxes, float) * MM
            lo, hi = B[:, :3].min(0), B[:, 3:6].max(0)
            def biou(T):
                bb = T.bounding_box(); l2 = np.array(tuple(bb.min)); h2 = np.array(tuple(bb.max))
                il = np.maximum(lo, l2); ih = np.minimum(hi, h2)
                inter = np.prod(np.clip(ih - il, 0, None)); u = np.prod(hi - lo) + np.prod(h2 - l2) - inter
                return inter / u if u > 0 else 0
            cands.sort(key=lambda c: -biou(c[1]))
        if len(cands) > 1 and self.ref is not None:
            # reference choice of the revolve side: the candidate whose material is final material
            sc = [ref_share(self.ref, T, m['kind'] == 'cut') for _, T in cands]
            if max(sc) - min(sc) > 0.1:
                cands = [c for _, c in sorted(zip(sc, cands), key=lambda z: -z[0])]
                op.meta['ref_side'] = [round(x, 2) for x in sc]
        sgn, T = cands[0]
        op.meta['dir'] = sgn
        cut = m['kind'] == 'cut'
        self.tools[f.name] = ('cut' if cut else 'boss', T)
        self.body = bop(self.body, T, 'cut' if cut else 'fuse')

    # ------------------------------------------------------------------ fillet / chamfer
    def _shim(self):
        import rv01_from_dump as R1
        obj = object.__new__(R1.Rebuild)
        obj.part = self.part; obj.ref = None; obj.bin = None; obj.tools = {}; obj.choice = {}; obj._ef = []
        obj.body = self.body
        return obj

    def _blend(self, f, fp, op, kind):
        from dump_parser import blend_params
        bp = blend_params(f)
        size = bp[1] * MM
        if self.body is None:
            raise RuntimeError('no body')
        sh = self._shim()
        exact = [o for o in fp.ops if o.kind == 'EDGE' and o.meta.get('exact')]
        prevname = self._prev_name(f.name)
        hints = [o for o in fp.ops if o.kind == 'EDGE' and o.meta.get('hint')]
        if exact:
            sel = match_edges(self.body, [(np.array(o.args[1:4]) * MM, np.array(o.args[4:7]) * MM, np.array(o.args[7:10]) * MM) for o in exact])
        elif hints:
            # rails-average hints from the blend's face edges -> nearest live sharp edges (size tolerance);
            # matched hint ops are replaced below by the matched edges' exact geometry, unmatched ones stay
            # (the VBA matches them with their own tolerance on the live SolidWorks body)
            mi = match_edges(self.body, [(np.array(o.args[1:4]) * MM, np.array(o.args[4:7]) * MM, np.array(o.args[7:10]) * MM) for o in hints], tol=max(size, 0.05), idx=True, on_edge=True)
            sel = [E for _, E in mi]
            got = {id(hints[i_]) for i_, _ in mi}
            op.meta['v4_hints'] = dict(total=len(hints), matched=len(got))
            fp.ops[:] = [o for o in fp.ops if not (o.kind == 'EDGE' and id(o) in got)]
        elif f.name in self.oracle and prevname in self.oracle:
            sel = removed_edges(self.oracle[prevname]['body'], self.oracle[f.name]['body'])
            sel = match_edges(self.body, [(np.array(tuple(E.position_at(0))), np.array(tuple(E.position_at(1))), np.array(tuple(E.position_at(0.5)))) for E in sel])
            sh._ef = []
        else:
            sel = sh.blend_edges(f, kind, size, f.faces)
            if self.ref is not None:
                rs = ref_blend_edges(self.body, self.ref, size, f.faces)
                op.meta['ref_blend'] = dict(REF_BLEND_STATS, hit=len(rs))
                if rs:
                    sel = rs
                    op.meta['edges_from'] = 'reference'
        if not sel:
            if not f.faces:
                # none of the blend's faces survive in the final part: later features consume it, so the
                # final shape does not depend on it (VBA still applies it by face boxes)
                self.status[f.name] = 'SKIP:no surviving faces (blend consumed later; no effect on final body)'
                return
            self.status[f.name] = 'FAIL:no matching edges (VBA falls back to face boxes)'
            return
        desc = []
        for E in sel:
            gt = str(E.geom_type).split('.')[-1]
            p0 = np.array(tuple(E.position_at(0))) / MM; p1 = np.array(tuple(E.position_at(1))) / MM
            pm = np.array(tuple(E.position_at(0.5))) / MM
            desc.append((gt, p0, p1, pm))
        self.edges[f.name] = desc
        # apply: all at once, else edge by edge
        b = self.body
        if not crash_safe(lambda: b.fillet(size, sel) if kind == 'fillet' else b.chamfer(size, None, sel)):
            # OCC segfaults on some blends: probe in a forked child first, skip the replay blend if it dies
            self.status[f.name] = 'FAIL:OCC crashes on this blend in replay (VBA applies it normally)'
            i = fp.ops.index(op)
            fp.ops[i:i] = [Op('EDGE', [gt, *p0, *p1, *pm], f.name) for gt, p0, p1, pm in desc]
            return
        try:
            nb = b.fillet(size, sel) if kind == 'fillet' else b.chamfer(size, None, sel)
            Ltot = sum(E.length for E in sel)
            if nb is not None and nb.is_valid and abs(vol(nb) - vol(b)) <= (0.3 if kind == "fillet" else 0.6) * size * size * Ltot + 1e-6:
                self.body = _solid(nb)
            else:
                raise RuntimeError('invalid')
        except Exception:
            done = 0
            cur = b
            for E in sel:
                try:
                    E2 = min(cur.edges(), key=lambda x: (x.center() - E.center()).length)
                    nb = cur.fillet(size, [E2]) if kind == 'fillet' else cur.chamfer(size, None, [E2])
                    if nb is not None and nb.is_valid and abs(vol(nb) - vol(cur)) <= (0.3 if kind == "fillet" else 0.6) * size * size * E2.length + 1e-6:
                        cur = _solid(nb); done += 1; continue
                except Exception:
                    pass
                try:   # explicit blend tool (rv01_from_dump): straight edges / chamfer tools
                    E2 = min(cur.edges(), key=lambda x: (x.center() - E.center()).length)
                    F = next((F for e_, F in sh._ef if e_ is E), None)
                    nb = None
                    if kind == 'chamfer':
                        T = sh.chamfer_tool(cur, E2, size)
                        nb = bop(cur, T, 'cut') if T is not None else None
                    if nb is None:
                        nb = sh.manual_blend_on(cur, E2, F, size, kind)
                    if nb is not None and nb.is_valid and abs(vol(nb) - vol(cur)) <= (0.3 if kind == "fillet" else 0.6) * size * size * E2.length + 1e-6:
                        cur = _solid(nb); done += 1
                except Exception:
                    pass
            self.body = cur
            if done < len(sel):
                self.status[f.name] = f'PART:{done}/{len(sel)} edges blended in replay'
                if hints and not exact and done < len(sel) / 2:
                    # OCC cannot blend the full v4 edge set (SolidWorks can: the VBA gets the full set).
                    # Replay volume only: fall back to the face-evidence edge choice if OCC manages more.
                    try:
                        alt = sh.blend_edges(f, kind, size, f.faces)
                        nb = b.fillet(size, alt) if kind == 'fillet' else b.chamfer(size, None, alt)
                        if alt and nb is not None and nb.is_valid and abs(vol(nb) - vol(b)) > abs(vol(cur) - vol(b)):
                            self.body = _solid(nb)
                            self.status[f.name] += f' (replay body: face-evidence subset {len(alt)} edges; VBA gets the v4 set)'
                    except Exception:
                        pass
        # EDGE ops before the blend op (VBA picks live edges by this geometry; EDGEBOX = fallback)
        if not exact:
            i = fp.ops.index(op)
            fp.ops[i:i] = [Op('EDGE', [gt, *p0, *p1, *pm], f.name) for gt, p0, p1, pm in desc]

    def _prev_name(self, name):
        names = [x.name for x in self.part.features if x.idx >= 0]
        i = names.index(name)
        for n in reversed(names[:i]):
            if n in self.oracle:
                return n
        return None

    def do_fillet(self, f, fp, op):
        self._blend(f, fp, op, 'fillet')

    def do_chamfer(self, f, fp, op):
        self._blend(f, fp, op, 'chamfer')

    # ------------------------------------------------------------------ mirror / patterns
    def do_mirror(self, f, fp, op):
        b = _b()
        m = op.meta
        g = self.pl.planes.get(m['plane'])
        if g is None:
            raise RuntimeError('plane unknown')
        pln = b.Plane(origin=tuple(g[0] * MM), z_dir=tuple(_unit(g[3])))
        if m['body'] or not m['seeds']:
            self.body = bop(self.body, self.body.mirror(pln), 'fuse')
            return
        miss = []
        for s in m['seeds']:
            if s in self.tools:
                kind, T = self.tools[s]
                self.body = bop(self.body, T.mirror(pln), 'fuse' if kind == 'boss' else 'cut')
            elif self.pl.kinds.get(s) == 'blend':
                sh = self._shim()
                sh.blend_feature(self.part.by_name[s], mirror=(np.array(_unit(g[3])), np.array(g[0])))
                self.body = _solid(sh.body)
            else:
                miss.append(s)
        if miss:
            self.status[f.name] = 'PART:seeds without replay tool ' + ','.join(miss)

    def _xform_seeds(self, f, seeds, xforms):
        miss = []
        made = []
        for s in seeds:
            if s not in self.tools:
                miss.append(s); continue
            kind, T = self.tools[s]
            for L in xforms:
                Tm = T.moved(L)
                made.append((kind, Tm))
                self.body = bop(self.body, Tm, 'fuse' if kind == 'boss' else 'cut')
        if made:
            # the instances become this feature's tool, so a later mirror/pattern of it can replay
            k0 = made[0][0]
            same = [T for k, T in made if k == k0]
            try:
                U = same[0]
                for T in same[1:]:
                    U = U.fuse(T)
                self.tools[f.name] = (k0, _solid(U))
            except Exception:
                pass
        if miss:
            self.status[f.name] = 'PART:seeds without replay tool ' + ','.join(miss)

    def do_cpattern(self, f, fp, op):
        b = _b()
        m = op.meta
        ao, aa = m['axis']
        n = m['n']; step = m['ang'] / n if m['eq'] else m['ang']
        ax = b.Axis(tuple(np.array(ao) * MM), tuple(_unit(aa)))
        xf = []
        for i in range(1, n):
            xf.append(_rot_loc(ax, math.degrees(step * i)))
        self._xform_seeds(f, m['seeds'], xf)

    def do_lpattern(self, f, fp, op):
        b = _b()
        m = op.meta
        xf = []
        for i in range(m['n1']):
            for j in range(m['n2']):
                if i == 0 and j == 0:
                    continue
                v = np.array(m['d1']) * m['s1'] * i + np.array(m['d2']) * m['s2'] * j
                xf.append(b.Location(tuple(v * MM)))
        self._xform_seeds(f, m['seeds'], xf)

    def do_loft(self, f, fp, op):
        b = _b()
        m = op.meta
        secs = []
        for p in m['profiles']:
            skf, sp = self.pl.sketches[p]
            R = region(sp, skf.sketch, None)
            if R is None:
                R = cells_union(sp, skf.sketch)
            if R is None:
                raise RuntimeError(f'profile {p} empty')
            fs = R.faces()
            secs.append(fs[0] if fs else R)
        T = _solid(b.loft(secs))
        kind = m['kind']
        self.tools[f.name] = (kind, T)
        self.body = bop(self.body, T, 'cut' if kind == 'cut' else 'fuse')


def _cell_points(c, n=9):
    """n points spread over a planar cell: area-weighted random points on its triangulation."""
    V, Tr = c.tessellate(0.05)
    V = np.array([tuple(v) for v in V]); Tr = np.array(Tr)
    if not len(Tr):
        return np.zeros((0, 3))
    A, B, C = V[Tr[:, 0]], V[Tr[:, 1]], V[Tr[:, 2]]
    ar = 0.5 * np.linalg.norm(np.cross(B - A, C - A), axis=1)
    if ar.sum() <= 0:
        return np.zeros((0, 3))
    rng = np.random.default_rng(11)
    k = max(n, 48)
    idx = rng.choice(len(Tr), size=k, p=ar / ar.sum())
    u, v = rng.random(k), rng.random(k)
    fl = u + v > 1; u[fl] = 1 - u[fl]; v[fl] = 1 - v[fl]
    return A[idx] + (B[idx] - A[idx]) * u[:, None] + (C[idx] - A[idx]) * v[:, None]


REF_BLEND_STATS = {}


def ref_blend_edges(body, ref, size, faces):
    """sharp edges the blend consumed, chosen with the reference: near the blend's dump faces, a convex
    edge whose corner material is missing in the reference (or a concave edge whose corner is filled)."""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN, TopAbs_EDGE, TopAbs_FACE
    from OCP.TopExp import TopExp
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.BRepLProp import BRepLProp_SLProps
    from OCP.ShapeAnalysis import ShapeAnalysis_Surface
    from OCP.gp import gp_Pnt
    from OCP.TopoDS import TopoDS
    from OCP.TopAbs import TopAbs_REVERSED
    B = [np.array(F.box, float) * MM for F in faces or [] if F.box is not None]
    if not B:
        return []
    pad = 1.5 * size + 0.05
    B = [(b[:3] - pad, b[3:] + pad) for b in B]
    adj = {}
    for fc in body.faces():
        for e in fc.edges():
            adj.setdefault(hash(e), []).append(fc.wrapped)
    cls = BRepClass3d_SolidClassifier(body.wrapped)
    inb = lambda q: (cls.Perform(gp_Pnt(*q), 1e-7), cls.State() == TopAbs_IN)[1]

    def normal(fc, p):
        S = BRepAdaptor_Surface(fc)
        uv = ShapeAnalysis_Surface(BRep_Tool_Surface(fc)).ValueOfUV(gp_Pnt(*p), 1e-6)
        pr = BRepLProp_SLProps(S, uv.X(), uv.Y(), 1, 1e-6)
        if not pr.IsNormalDefined():
            return None
        n = pr.Normal(); v = np.array([n.X(), n.Y(), n.Z()])
        return -v if fc.Orientation() == TopAbs_REVERSED else v

    out = []
    st = REF_BLEND_STATS
    st.clear()
    for E in body.edges():
        m = np.array(tuple(E.position_at(0.5)))
        st['edges'] = st.get('edges', 0) + 1
        if not any(np.all(m >= lo) and np.all(m <= hi) for lo, hi in B):
            continue
        try:
            fs = adj.get(hash(E), [])
            st['near'] = st.get('near', 0) + 1
            if len(fs) != 2:
                st['nf%d' % len(fs)] = st.get('nf%d' % len(fs), 0) + 1
                continue
            ns = [normal(fc, m) for fc in fs]
            if any(n is None for n in ns) or abs(ns[0] @ ns[1]) > 0.996:
                continue            # smooth (tangent) edge: nothing to blend
            bis = ns[0] + ns[1]; bis /= np.linalg.norm(bis)
            hit = True
            for t in (0.25, 0.5, 0.75):     # the whole edge must be blended in the reference
                pt = np.array(tuple(E.position_at(t)))
                q_in, q_out = pt - 0.2 * size * bis, pt + 0.2 * size * bis
                far_in = pt - 1.5 * size * bis
                if inb(q_in):           # convex: corner missing, but material further in present
                    h = (not ref.inside([q_in])[0]) and bool(ref.inside([far_in])[0])
                elif not inb(q_out):    # concave: a blend fills the corner
                    h = bool(ref.inside([q_out])[0])
                else:
                    h = False
                hit = hit and h
                if not hit:
                    break
            st['tested'] = st.get('tested', 0) + 1
            if hit:
                out.append(E)
        except Exception as ex:
            st['err'] = repr(ex)[:80]
            continue
    return out


def BRep_Tool_Surface(fc):
    from OCP.BRep import BRep_Tool
    return BRep_Tool.Surface_s(fc)


def crash_safe(fn, timeout=120):
    """True when fn() returns without killing the process (run in a forked child)."""
    import os, signal
    try:
        pid = os.fork()
    except Exception:
        return True
    if pid == 0:
        try:
            fn()
        except BaseException:
            pass
        os._exit(0)
    t0 = time.time()
    while True:
        r, st = os.waitpid(pid, os.WNOHANG)
        if r:
            return os.WIFEXITED(st) and os.WEXITSTATUS(st) == 0
        if time.time() - t0 > timeout:
            os.kill(pid, signal.SIGKILL); os.waitpid(pid, 0)
            return False
        time.sleep(0.05)


def cells_union(sp, sk):
    """whole sketch as faces of its segment arrangement (profiles whose contours are stored open)."""
    try:
        cells = sketch_cells_mm(sp, sk)
    except Exception:
        return None
    if not cells:
        return None
    R = cells[0]
    for c in cells[1:]:
        R = R.fuse(c)
    try:
        R = R.clean()
    except Exception:
        pass
    return R


def ref_cell_on_revolve(ref, cell, a, ax, cut):
    """a revolve profile cell is kept when its points, swept a few angles about the axis, are final
    material (boss) / void (cut) in the reference."""
    P = _cell_points(cell, 24)
    if not len(P):
        return False
    Q = []
    for ang in np.radians([0, 60, 120, 180, 240, 300]):
        c, s_ = math.cos(ang), math.sin(ang)
        for p in P:
            v = p - a; par = (v @ ax) * ax; perp = v - par
            Q.append(a + par + perp * c + np.cross(ax, perp) * s_)
    f = float(ref.inside(np.array(Q)).mean())
    return f <= 0.02 if cut else f >= 0.4


def ref_share(ref, T, cut=False, n=1500):
    """share of a tool solid that is final material (boss) / void (cut) in the reference."""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt
    bb = T.bounding_box()
    lo = np.array([bb.min.X, bb.min.Y, bb.min.Z]); hi = np.array([bb.max.X, bb.max.Y, bb.max.Z])
    P = np.random.default_rng(7).uniform(lo, hi, (n, 3))
    c = BRepClass3d_SolidClassifier(T.wrapped)
    keep = []
    for p in P:
        c.Perform(gp_Pnt(*p), 1e-6)
        keep.append(c.State() == TopAbs_IN)
    P = P[np.array(keep)][:300]
    if not len(P):
        return 0.0
    f = float(ref.inside(P).mean())
    return 1.0 - f if cut else f


def ref_cells(cells, ref, dvec, ivs, kind):
    """reference-mesh choice: boss cells whose swept interior is mostly inside the final part,
    cut cells whose swept interior is mostly outside it. Cells near 50% are returned as ambiguous."""
    lo, hi = ivs[0]
    pr = ref.tris.reshape(-1, 3) @ dvec
    out, amb, fr = [], [], []
    for i, c in enumerate(cells):
        P = _cell_points(c)
        if not len(P):
            continue
        # sample only where the reference exists along the sweep (through-all must not dilute the vote)
        p0 = float(P[0] @ dvec)
        lo2, hi2 = max(lo, pr.min() - p0), min(hi, pr.max() - p0)
        if hi2 - lo2 < 1e-6:
            fr.append(0.0)
            if kind == 'cut':
                out.append(i)
            continue
        zs = np.linspace(lo2, hi2, 9)[1:-1]
        Q = (P[:, None, :] + dvec[None, None, :] * zs[None, :, None]).reshape(-1, 3)
        f = float(ref.inside(Q).mean())       # fraction of the sweep that is final material
        fr.append(round(f, 2))
        # a cut may not remove final material at all; a boss may later be cut back, so it only needs a
        # clear share of final material
        lo_t, hi_t = (0.02, 0.06) if kind == 'cut' else (0.10, 0.40)
        keep = f <= lo_t if kind == 'cut' else f >= hi_t
        drop = f >= hi_t if kind == 'cut' else f <= lo_t
        if keep:
            out.append(i)
        elif not drop:
            amb.append(i)
    return out, dict(ref=True, face_edges=1, ambiguous=amb, frac=fr[:20])


def decoder_region(sp, sk, sel, op):
    """region from the decoder's chooser: ALL when every non-construction segment is selected, else
    the closed contours whose segments are all selected."""
    typ = lambda e: 0 if e.kind == 'line' else 1
    nc = [e for e in sp.ents if not e.constr and e.kind in ('line', 'arc', 'circle')]
    if not nc:
        return None
    if all((typ(e), e.did) in sel for e in nc):
        op.meta['profile'] = 'ALL(decoder)'
        return region(sp, sk, None)
    by = {e.key: e for e in sp.ents}
    ii = [c['index'] for c in sp.contours if c['closed'] and c['keys']
          and all(k in by and (typ(by[k]), by[k].did) in sel for k in c['keys'])]
    if not ii:
        return None
    R = region(sp, sk, ii)
    if R is None:
        return None
    op.args[-1] = ';'.join(str(i) for i in ii)
    op.meta['profile'] = 'SUBSET(decoder)'
    return R


def oracle_cells(cells, T, dvec, ivs):
    """cells whose swept interior lies inside the oracle tool solid (reference-driven run)."""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt
    cls = BRepClass3d_SolidClassifier(T.wrapped)
    lo, hi = ivs[0]; lo2, hi2 = max(lo, -50.0), min(hi, 50.0)
    out = []
    for i, c in enumerate(cells):
        V, Tr = c.tessellate(0.05)
        V = np.array([tuple(v) for v in V]); Tr = np.array(Tr)
        ar = 0.5 * np.linalg.norm(np.cross(V[Tr[:, 1]] - V[Tr[:, 0]], V[Tr[:, 2]] - V[Tr[:, 0]]), axis=1)
        p = V[Tr[np.argmax(ar)]].mean(0)
        hit = 0; tot = 0
        for z in np.linspace(lo2, hi2, 7)[1:-1]:
            cls.Perform(gp_Pnt(*(p + dvec * z)), 1e-6); tot += 1
            hit += cls.State() == TopAbs_IN
        if hit * 2 > tot:
            out.append(i)
    return out, dict(oracle=True, face_edges=1)


def removed_edges(prev, new, tol=0.02):
    """edges of prev that are not on new's boundary (the sharp edges a blend consumed)."""
    b = _b()
    keys = {tuple(np.round(tuple(E.position_at(0.5)), 4)) for E in new.edges()}
    shell = b.Compound(new.faces())
    out = []
    for E in prev.edges():
        m = E.position_at(0.5)
        if tuple(np.round(tuple(m), 4)) in keys:
            continue
        try:
            if shell.distance_to(m) > tol:
                out.append(E)
        except Exception:
            pass
    return out


def match_edges(body, wanted, tol=1e-3, idx=False, on_edge=False):
    """body edges matching (start, end, mid) in mm. Closed wanted edges (start == end: full circles,
    whose seam point differs between SolidWorks and OCC) are matched by point-to-edge distance of the
    start and mid points instead. on_edge=True (derived hints): the wanted points only have to lie on the
    edge (the sharp edge a blend consumed is often longer than the blend face rails).
    idx=True -> [(wanted index, edge)]."""
    b = _b()
    out = []
    es = body.edges()
    pre = []
    for E in es:
        a = np.array(tuple(E.position_at(0))); c = np.array(tuple(E.position_at(1))); mm = np.array(tuple(E.position_at(0.5)))
        pre.append((E, a, c, mm, np.linalg.norm(a - c) < 1e-6))
    for wi, (s_, e_, m_) in enumerate(wanted):
        s_, e_, m_ = np.asarray(s_, float), np.asarray(e_, float), np.asarray(m_, float)
        wclosed = np.linalg.norm(s_ - e_) < 1e-6
        best, bd = None, 1e30
        for E, a, c, mm, closed in pre:
            if wclosed:
                if not closed:
                    continue
                if min(np.linalg.norm(a - s_), np.linalg.norm(mm - m_), np.linalg.norm(a - m_)) > 4 * tol + np.linalg.norm(a - mm):
                    continue
                try:
                    d = 2 * E.distance_to(b.Vector(*s_)) + E.distance_to(b.Vector(*m_))
                except Exception:
                    continue
            elif on_edge:
                if closed:
                    continue
                half = np.linalg.norm(a - c) / 2 + np.linalg.norm(mm - (a + c) / 2)
                if np.linalg.norm(mm - m_) > half + 4 * tol:
                    continue
                try:
                    d = E.distance_to(b.Vector(*s_)) + E.distance_to(b.Vector(*e_)) + E.distance_to(b.Vector(*m_))
                except Exception:
                    continue
                L = np.linalg.norm(e_ - s_)
                if E.length < 0.5 * L:
                    continue
            else:
                d = min(np.linalg.norm(a - s_) + np.linalg.norm(c - e_), np.linalg.norm(a - e_) + np.linalg.norm(c - s_)) + np.linalg.norm(mm - m_)
            if d < bd:
                best, bd = E, d
        if best is not None and bd < tol * 3 and not any(best.is_same(x) for _, x in out):
            out.append((wi, best))
    return out if idx else [x for _, x in out]


def _rot_loc(ax, deg):
    b = _b()
    from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir
    t = gp_Trsf()
    o = ax.position; d = ax.direction
    t.SetRotation(gp_Ax1(gp_Pnt(o.X, o.Y, o.Z), gp_Dir(d.X, d.Y, d.Z)), math.radians(deg))
    return b.Location(t)


def iou(a, bshape):
    if a is None or bshape is None:
        return 0.0
    try:
        c = vol(a.intersect(bshape))
        return c / (vol(a) + vol(bshape) - c)
    except Exception:
        return float('nan')


def insert_expect(planner, rp):
    """add EXPECT ops (replay volume m3 after the feature) in front of each body feature's main op."""
    for fp in planner.plans:
        if fp.name in rp.vols:
            for i, o in enumerate(fp.ops):
                if o.kind in ('EXTRUDE', 'REVOLVE', 'FILLET', 'CHAMFER', 'MIRROR', 'CPATTERN', 'LPATTERN', 'LOFT'):
                    st = rp.status.get(fp.name, 'OK')
                    fp.ops.insert(i, Op('EXPECT', [rp.vols[fp.name], st.split(':')[0]], fp.name))
                    break
