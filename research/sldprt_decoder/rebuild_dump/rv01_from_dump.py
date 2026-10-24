"""RV01 Chassis rebuilt in build123d from the SolidWorks API dump (dumps/RV01 Chassis.dump.txt).

    python3 rv01_from_dump.py [--compare] [--no-ref-select]

Exact from the dump: sketch geometry (lines/arcs in sketch space), sketch->model transforms, feature
order, end conditions, depths, direction flags, mirror planes, fillet/chamfer sizes.
Not in the v1 dump, inferred (each choice is logged in rv01_from_dump.log.json):
  * profile regions  : each sketch is split into its planar cells; a cell is used by a boss if most of
                       the new material lies inside the reference, by a cut if most of the removed
                       material lies outside it.            (v2 dump: CONTOUR/FACE lines would replace this)
  * up-to surfaces   : candidates are the planar faces of the current body that are normal to the
                       extrude direction, in front of the sketch; the one giving the best IoU is used.
                       (v2: UPTO_REF lines are used directly when present)
  * fillet / chamfer : model edges whose nearest reference face is a cylinder/torus of the feature's
                       radius (or an inclined plane for chamfers), at a blend-like distance.
                       (v2: EDGE lines are used directly when present)
The reference is only *queried* (volumes of intersections, point distances); no reference geometry is
ever added to the model.
"""
import json, math, os, sys, time
import numpy as np
from build123d import (Plane, Face, Edge, Solid, Compound, Vector, Location, extrude, fillet, chamfer,
                       export_step, import_brep, Axis)
from OCP.gp import gp_Trsf, gp_Pnt, gp_Ax2, gp_Dir
from OCP.BRepAlgoAPI import BRepAlgoAPI_Splitter

from OCP.collections import List_TopoDS_Shape as TopTools_ListOfShape
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Torus, GeomAbs_Cone
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_IN, TopAbs_OUT

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dump_parser import parse_dump, blend_params

DUMP = os.path.join(HERE, '..', 'dumps_v2', 'RV01 Chassis.dump.txt')
REF_BREP = os.path.join(HERE, '..', 'rebuild', 'ref_rv01_asmframe.brep')   # RV01_Chassis_1 from rvrn_2.0.step
# assembly placement of 'RV01 Chassis-1' (from rebuild/RV01_REPORT.md): p_asm = t + x*r0 + y*r1 + z*r2
ASM_ROWS = np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]], float)
ASM_T = np.array([0, 11, 0], float)
MM = 1000.0
BIG = 300.0
LOG = []


def log(feat, status, msg='', **kw):
    LOG.append(dict(feature=feat, status=status, msg=msg, **kw))
    print(f'[{status:5s}] {feat:16s} {msg} ' + ' '.join(f'{k}={v}' for k, v in kw.items()), flush=True)


def vol(s):
    try:
        return 0.0 if s is None else float(s.volume)
    except Exception:
        return 0.0


def solid_of(x):
    if x is None: return None
    if isinstance(x, (list, tuple)):
        x = [s for s in x if s is not None]
        return Compound(x) if x else None
    return x


def vcommon(a, b):
    """volume of a & b computed as vol(a) - vol(a - b) (BOP common is unreliable on these bodies)."""
    if a is None or b is None: return 0.0
    va = vol(a)
    c1 = va - vol(bop(a, b, 'cut'))
    return min(max(c1, 0.0), va)


def bop(a, b, op):
    if a is None: return None if op != 'fuse' else b
    if b is None: return None if op == 'common' else a
    r = {'fuse': a.fuse, 'cut': a.cut, 'common': a.intersect}[op](b)
    r = solid_of(r) if isinstance(r, (list, tuple)) else r
    if r is not None and op == 'fuse':
        try: r = r.clean()
        except Exception: pass
    return r


def _one(b):
    sl = b.solids()
    return sl[0] if len(sl) == 1 else b


def in_box_perp(q, box, ax, tol=0.05):
    """q inside the dumped face box, ignoring the coordinates mostly along ax (faces get trimmed later)."""
    if box is None: return True
    lo = np.array(box[:3]) * MM - tol; hi = np.array(box[3:6]) * MM + tol
    use = np.abs(np.asarray(ax)) < 0.5
    return bool(np.all((q[use] >= lo[use]) & (q[use] <= hi[use])))


def _clean(x):
    from build123d import Shape
    if isinstance(x, Shape): return type(x)(x.wrapped) if not isinstance(x, Compound) else Compound(x.wrapped)
    return x


def trsf_from(rows, t):
    T = gp_Trsf()
    M = np.array(rows, float).T
    T.SetValues(*M[0], t[0], *M[1], t[1], *M[2], t[2])
    return Location(T)


# ----------------------------------------------------------------------------- sketch -> cells
def seg_edge(sg):
    P = lambda p: Vector(p[0] * MM, p[1] * MM, 0)
    if sg.type == 0:
        if np.hypot(sg.p1[0] - sg.p0[0], sg.p1[1] - sg.p0[1]) < 1e-9: return None
        return Edge.make_line(P(sg.p0), P(sg.p1))
    if sg.type == 1:
        c = np.array(sg.c[:2]) * MM; r = sg.r * MM
        if sg.is_circle:
            return Edge.make_circle(r, Plane.XY.move(Location((c[0], c[1], 0))))
        a0 = math.atan2(sg.p0[1] * MM - c[1], sg.p0[0] * MM - c[0])
        a1 = math.atan2(sg.p1[1] * MM - c[1], sg.p1[0] * MM - c[0])
        sw = (a1 - a0) % (2 * math.pi) if (sg.dir or 1) > 0 else -((a0 - a1) % (2 * math.pi))
        am = a0 + sw / 2
        return Edge.make_three_point_arc(P(sg.p0), Vector(c[0] + r * math.cos(am), c[1] + r * math.sin(am), 0), P(sg.p1))
    return None


def sketch_cells(feat):
    """all bounded planar cells of the sketch's non-construction curves, in model space (mm)."""
    sk = feat.sketch
    edges = []
    for sg in sk.profile_segs():
        try:
            e = seg_edge(sg)
            if e is not None: edges.append(e)
        except Exception as ex:
            log(feat.name, 'WARN', f'seg {sg.id} skipped: {ex}')
    if not edges: return []
    bb = Compound(edges).bounding_box()
    lo = np.array([bb.min.X, bb.min.Y]) - 5; hi = np.array([bb.max.X, bb.max.Y]) + 5
    big = Face.make_rect(hi[0] - lo[0], hi[1] - lo[1], Plane.XY.move(Location(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0))))
    sp = BRepAlgoAPI_Splitter(); a = TopTools_ListOfShape(); a.Append(big.wrapped); t = TopTools_ListOfShape()
    for e in edges: t.Append(e.wrapped)
    sp.SetArguments(a); sp.SetTools(t); sp.Build()
    cells = []
    for f in Compound(sp.Shape()).faces():
        fb = f.bounding_box()
        if fb.min.X < lo[0] + 1e-6 or fb.min.Y < lo[1] + 1e-6 or fb.max.X > hi[0] - 1e-6 or fb.max.Y > hi[1] - 1e-6:
            continue
        if f.area < 1e-6: continue
        cells.append(f)
    L = trsf_from(sk.rot, np.array(sk.trans) * MM)
    return [c.moved(L) for c in cells]


# ----------------------------------------------------------------------------- reference queries
class Grid:
    """regular voxel grid; inside test by z-ray parity on the shape's tessellation (fast, no BOPs)."""
    def __init__(self, lo, hi, dxy=0.2, dz=0.1):
        self.lo = np.array(lo, float) + np.array([0.0137, 0.0071, 0.0029])   # jitter off feature planes
        self.d = np.array([dxy, dxy, dz])
        self.n = np.ceil((np.array(hi) - self.lo) / self.d).astype(int)
        self.dv = float(np.prod(self.d))

    def inside(self, shape, tol=0.01):
        nx, ny, nz = self.n
        out = np.zeros((nx, ny, nz + 1), np.int8)
        V = None
        for tl, an in ((tol, 0.1), (0.02, 0.2), (0.005, 0.05), (0.05, 0.3)):
            try:
                V, T = shape.tessellate(tl, an); break
            except Exception:
                V = None
        if V is None:
            # per-face fallback: skip faces that will not mesh
            V, T = [], []
            for fc in shape.faces():
                try:
                    v, t = fc.tessellate(tol, 0.1); T += [[a + len(V) for a in tt] for tt in t]; V += list(v)
                except Exception:
                    pass
        V = np.array([tuple(v) for v in V]); T = np.array(T)
        if len(T) == 0: return np.zeros(nx * ny * nz, bool)
        X = (V[T] - self.lo) / self.d - 0.5        # grid index space (voxel centers at integers)
        i0 = np.clip(np.ceil(X[:, :, 0].min(1)), 0, nx).astype(int); i1 = np.clip(np.floor(X[:, :, 0].max(1)), -1, nx - 1).astype(int)
        j0 = np.clip(np.ceil(X[:, :, 1].min(1)), 0, ny).astype(int); j1 = np.clip(np.floor(X[:, :, 1].max(1)), -1, ny - 1).astype(int)
        ok = (i1 >= i0) & (j1 >= j0)
        I, J, Z = [], [], []
        for t in np.nonzero(ok)[0]:
            ii, jj = np.meshgrid(np.arange(i0[t], i1[t] + 1), np.arange(j0[t], j1[t] + 1), indexing='ij')
            ii = ii.ravel(); jj = jj.ravel()
            (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = X[t]
            den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
            if abs(den) < 1e-14: continue
            l0 = ((y1 - y2) * (ii - x2) + (x2 - x1) * (jj - y2)) / den
            l1 = ((y2 - y0) * (ii - x2) + (x0 - x2) * (jj - y2)) / den
            l2 = 1 - l0 - l1
            m = (l0 >= 0) & (l1 >= 0) & (l2 >= 0)
            if not m.any(): continue
            I.append(ii[m]); J.append(jj[m]); Z.append(l0[m] * z0 + l1[m] * z1 + l2[m] * z2)
        if not I: return np.zeros(nx * ny * nz, bool)
        I = np.concatenate(I); J = np.concatenate(J); Z = np.concatenate(Z)
        k = np.clip(np.ceil(Z), 0, nz).astype(int)
        np.add.at(out, (I, J, k), 1)
        return (np.cumsum(out, 2) % 2).astype(bool)[:, :, :nz].ravel()


class Ref:
    def __init__(self, shape):
        self.s = shape
        self.V = shape.volume
        self.faces = shape.faces()
        self.kinds = []
        for f in self.faces:
            ad = BRepAdaptor_Surface(f.wrapped)
            t = ad.GetType()
            if t == GeomAbs_Cylinder: self.kinds.append(('cyl', ad.Cylinder().Radius()))
            elif t == GeomAbs_Torus: self.kinds.append(('torus', ad.Torus().MinorRadius()))
            elif t == GeomAbs_Plane:
                d = ad.Plane().Axis().Direction(); self.kinds.append(('plane', (d.X(), d.Y(), d.Z())))
            elif t == GeomAbs_Cone: self.kinds.append(('cone', None))
            else: self.kinds.append(('other', None))

    def init_points(self, cache=None):
        b = self.s.bounding_box()
        self.G = Grid(np.array(tuple(b.min)) - 1.0, np.array(tuple(b.max)) + 1.0)
        self.dv = self.G.dv
        self.rin = self.G.inside(self.s)
        self.Vpts = self.rin.sum() * self.dv
        print(f'ref grid {self.G.n} vol_grid={self.Vpts:.1f} vol_brep={self.V:.1f}', flush=True)

    def pts_in(self, shape, mask=None):
        return self.G.inside(shape)

    def miou(self, bin_):
        i = (bin_ & self.rin).sum(); u = (bin_ | self.rin).sum()
        return i / max(u, 1)

    def inside(self, p):
        c = BRepClass3d_SolidClassifier(self.s.wrapped, gp_Pnt(*p), 1e-6)
        return c.State() == TopAbs_IN

    def nearest(self, p, faces_idx=None):
        v = BRepBuilderAPI_MakeVertex(gp_Pnt(*p)).Vertex()
        best = (np.inf, -1)
        for i in (range(len(self.faces)) if faces_idx is None else faces_idx):
            d = BRepExtrema_DistShapeShape(v, self.faces[i].wrapped)
            if d.IsDone() and d.Value() < best[0]: best = (d.Value(), i)
        return best

    def iou(self, body):
        if body is None: return 0.0
        c = vcommon(body, self.s)
        return c / (vol(body) + self.V - c)


# ----------------------------------------------------------------------------- rebuild
class Rebuild:
    def __init__(self, dump=DUMP, ref=None):
        self.part = parse_dump(dump)
        self.ref = ref
        self.body = None
        self.bin = np.zeros(int(np.prod(ref.G.n)), bool) if ref is not None else None
        self.tools = {}      # feature -> ('boss'|'cut'|'blend', tool solid or blend params)
        self.choice = {}

    # --- extents ---------------------------------------------------------
    def plane_offsets(self, origin, n):
        """signed offsets (along n) of current body planar faces normal to n."""
        out = set()
        if self.body is None: return []
        for f in self.body.faces():
            ad = BRepAdaptor_Surface(f.wrapped)
            if ad.GetType() != GeomAbs_Plane: continue
            pl = ad.Plane(); d = pl.Axis().Direction(); o = pl.Location()
            if abs(abs(d.X() * n[0] + d.Y() * n[1] + d.Z() * n[2]) - 1) > 1e-6: continue
            s = (o.X() - origin[0]) * n[0] + (o.Y() - origin[1]) * n[1] + (o.Z() - origin[2]) * n[2]
            out.add(round(s, 5))
        return sorted(out)

    def side_candidates(self, cond, d, origin, n, e, which, caps=()):
        """list of (lo, hi) along n for one side. which=1 first direction (+n), 2 second (-n).
        caps: offsets (along n) of the feature's own FACE planes normal to n (v2 dump)."""
        sgn = 1 if which == 1 else -1
        dd = d * MM
        if cond == 0: return [(0, dd)]
        if cond in (1, 9): return [(0, BIG)]
        if cond == 6: return [(-dd / 2, dd / 2)]
        ref = e.upto1 if which == 1 else e.upto2
        if ref is not None and ref.kind == 'plane':
            o = np.array(ref.params['o']) * MM
            s = sgn * float(np.dot(o - origin, n))
            return [(0, s + (dd if cond == 5 else 0))]
        capc = sorted({sgn * c for c in caps if sgn * c > 1e-4})
        offs = [s * sgn for s in self.plane_offsets(origin, n)]
        if cond in (2, 4, 7, 3):
            c = sorted({s for s in offs if s > 1e-4})
            if cond == 2: c = c[:1]
            return [(0, s) for s in sorted(set(capc) | set(c))]
        if cond == 5:
            c = sorted({s + k * dd for s in offs for k in (1, -1) if s + k * dd > 1e-4})
            return [(0, s) for s in sorted(set(capc) | set(c))]
        return [(0, dd)]

    def prism(self, cells, n, lo, hi):
        sols = []
        for c in cells:
            f = c.moved(Location(tuple(np.array(n) * lo)))
            sols.append(extrude(f, amount=hi - lo, dir=tuple(n)))
        return sols

    @staticmethod
    def on_face(p, F, tol=2e-3):
        """point (mm) lies on dumped FACE surface F (m) and inside its box."""
        if F.box is not None:
            lo = np.array(F.box[:3]) * MM - 0.05; hi = np.array(F.box[3:6]) * MM + 0.05
            if np.any(p < lo) or np.any(p > hi): return False
        if F.kind == 'plane':
            nn = np.array(F.params['n']); o = np.array(F.params['o']) * MM
            return abs(np.dot(p - o, nn)) < tol
        if F.kind == 'cyl':
            ax = np.array(F.params['ax']); ax = ax / np.linalg.norm(ax); o = np.array(F.params['o']) * MM
            v = p - o; v = v - ax * np.dot(v, ax)
            return abs(np.linalg.norm(v) - F.params['r'] * MM) < tol
        return False

    def face_evidence(self, cell, n, ivs, faces):
        """fraction of the cell's boundary edges whose swept side lies on one of the feature's faces."""
        if not faces: return None
        hits = 0; es = cell.edges()
        for E in es:
            m = np.array(tuple(E.position_at(0.5)))
            ok = False
            for lo, hi in ivs:
                for u in (0.1, 0.5, 0.9):
                    z = lo + u * (hi - lo) if hi - lo < BIG else None
                    if z is None: continue
                    if any(self.on_face(m + np.array(n) * z, F) for F in faces): ok = True; break
                if ok: break
            hits += ok
        return hits / max(1, len(es))

    def columns(self, cell, n, ivs, solid_cls, body_cls, kind):
        """fraction of sample columns through the cell that hold reference material (boss: outside body)."""
        V, T = cell.tessellate(0.05)
        V = np.array([tuple(v) for v in V]); T = np.array(T)
        cen = V[T].mean(1); ar = 0.5 * np.linalg.norm(np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]), axis=1)
        rng = np.random.default_rng(1)
        idx = rng.choice(len(T), min(12, 3 * len(T)), p=ar / ar.sum())
        u = rng.random(len(idx)); w = rng.random(len(idx)); mk = u + w > 1; u[mk] = 1 - u[mk]; w[mk] = 1 - w[mk]
        P = V[T[idx, 0]] + u[:, None] * (V[T[idx, 1]] - V[T[idx, 0]]) + w[:, None] * (V[T[idx, 2]] - V[T[idx, 0]])
        good = 0
        for p in P:
            hit = False
            for lo, hi in ivs:
                lo2, hi2 = max(lo, -60), min(hi, 60)
                for z in np.arange(lo2 + 0.25, hi2, 0.5):
                    q = p + np.array(n) * z
                    solid_cls.Perform(gp_Pnt(*q), 1e-6)
                    if solid_cls.State() != TopAbs_IN: continue
                    if body_cls is not None:
                        body_cls.Perform(gp_Pnt(*q), 1e-6)
                        if body_cls.State() == TopAbs_IN: continue
                    hit = True; break
                if hit: break
            good += hit
        return good / len(P)

    def select_cells(self, cells, n, ivs, kind, name, faces=()):
        keep, info = [], []
        if self.ref is None:
            return list(cells), info
        rcls = BRepClass3d_SolidClassifier(self.ref.s.wrapped)
        bcls = BRepClass3d_SolidClassifier(self.body.wrapped) if self.body is not None else None
        for i, c in enumerate(cells):
            fe = self.face_evidence(c, n, ivs, faces)
            P = solid_of([s for lo, hi in ivs for s in self.prism([c], n, lo, hi)])
            inP = self.ref.pts_in(P)
            R = self.ref
            if kind == 'boss':
                new = inP & ~self.bin
                if new.sum() < 3: info.append('0'); continue
                fr = self.columns(c, n, ivs, rcls, bcls, kind)
                vf = (new & R.rin).sum() / new.sum()
                ok = fr > 0.75 or vf > 0.5
                fe = (fe, round(float(vf), 2))
            else:
                rem = inP & self.bin
                if rem.sum() < 3: info.append('0'); continue
                fr = 1 - (rem & R.rin).sum() / rem.sum()
                ok = fr > 0.5
            info.append(f'{fr:.2f}/{fe}')
            if ok: keep.append(c)
        return keep, info

    def extrude_feature(self, f):
        e = f.extrude
        skf = self.part.sketch_of(f)
        if skf is None or skf.sketch is None:
            log(f.name, 'SKIP', 'no sketch'); return
        sk = skf.sketch
        kind = 'cut' if 'cut' in f.name.lower() or f.type in ('Cut', 'CutThin') else 'boss'
        cells = sketch_cells(skf)
        origin = np.array(sk.trans) * MM
        n0 = np.array(sk.normal, float)
        if kind == 'cut': n0 = -n0
        if e.reverse: n0 = -n0
        best = None; ncand = 0
        signs = (1, -1) if e.end1 in (0, 5) and not e.both else (1,)
        for sg in signs:
            n = n0 * sg
            caps = []
            for F in f.faces:
                if F.kind == 'plane' and abs(abs(np.dot(F.params['n'], n)) - 1) < 1e-6:
                    caps.append(float(np.dot(np.array(F.params['o']) * MM - origin, n)))
                if F.box is not None and e.end1 in (2, 3, 4, 7):
                    b = np.array(F.box[:6]) * MM
                    pr = [float(np.dot(np.array([b[i], b[1 + j], b[2 + k]]) - origin, n))
                          for i in (0, 3) for j in (0, 3) for k in (0, 3)]
                    caps += [round(max(pr), 5), round(min(pr), 5)]
            c1 = [(-BIG, BIG)] if e.end1 == 9 else self.side_candidates(e.end1, e.d1, origin, n, e, 1, caps)
            c2 = [None]
            if e.both and e.end1 not in (6, 9):
                c2 = [(-hi, -lo) for lo, hi in self.side_candidates(e.end2, e.d2, origin, n, e, 2, caps)]
            for iv1 in c1:
                for iv2 in c2:
                    ncand += 1
                    ivs = [iv1] + ([iv2] if iv2 else [])
                    keep, info = self.select_cells(cells, n, ivs, kind, f.name, f.faces)
                    if not keep:
                        cand = (-1, ivs, keep, info, None, None, n)
                    else:
                        T = solid_of([s for lo, hi in ivs for s in self.prism(keep, n, lo, hi)])
                        sl = T.solids()
                        if len(sl) > 1: T = sl[0].fuse(*sl[1:]).clean()
                        inT = self.ref.pts_in(T)
                        nb = (self.bin | inT) if kind == 'boss' else (self.bin & ~inT)
                        sc = self.ref.miou(nb)
                        cand = (sc, ivs, keep, info, T, nb, n)
                    if best is None or cand[0] > best[0] + 1e-9: best = cand
        sc, ivs, keep, info, T, B, n = best
        if T is None:
            log(f.name, 'FAIL', 'no cells selected', cells=len(cells), info=info); return
        self.body = bop(self.body, T, 'fuse' if kind == 'boss' else 'cut')
        self.bin = B
        self.tools[f.name] = (kind, T)
        self.choice[f.name] = dict(kind=kind, cells_total=len(cells), cells_used=len(keep),
                                   intervals=[[round(a, 3), round(b, 3)] for a, b in ivs],
                                   n_candidates=ncand, cell_scores=info, dir=[round(x, 3) for x in n])
        log(f.name, 'OK', kind, end1=e.end1_name, cells=f'{len(keep)}/{len(cells)}', ivs=self.choice[f.name]['intervals'],
            cand=ncand, vol=round(vol(self.body), 1), iou=round(sc, 4), scores=info)

    # --- blends ----------------------------------------------------------
    @staticmethod
    def mirror_surface(F, mp):
        """mirror a dumped Surface through plane (normal nn, origin o) in metres."""
        import copy
        nn, o = mp
        G = copy.deepcopy(F)
        R = lambda p: tuple(np.array(p) - 2 * np.dot(np.array(p) - o, nn) * nn)
        Rv = lambda v: tuple(np.array(v) - 2 * np.dot(np.array(v), nn) * nn)
        if F.kind == 'plane': G.params = dict(n=Rv(F.params['n']), o=R(F.params['o']))
        elif F.kind == 'cyl': G.params = dict(o=R(F.params['o']), ax=Rv(F.params['ax']), r=F.params['r'])
        elif F.kind in ('torus', 'cone', 'sphere'):
            v = list(F.params['values']); v[0:3] = R(v[0:3])
            if F.kind != 'sphere': v[3:6] = Rv(v[3:6])
            G.params = dict(values=v)
        if F.box is not None:
            a = np.array(R(F.box[:3])); b = np.array(R(F.box[3:6]))
            G.box = list(np.minimum(a, b)) + list(np.maximum(a, b))
        return G

    def chamfer_edges(self, size, faces):
        """exact chamfer edge recovery from the dumped chamfer FACE planes.

        A 45 deg equal-distance chamfer face of size d replaces a sharp edge where two pre-blend faces met.
        That sharp edge is the intersection line of those two faces; it lies on the *outer* side of the
        chamfer plane (along its outward normal) at distance d*cos(45) and the chamfer normal bisects the
        two adjacent outward face normals.  So a body edge is the original edge when
          * both adjacent faces are planar and normalize(n1+n2) == chamfer normal,
          * signed distance to the chamfer plane == d/sqrt2 (> 0),
          * its projection onto the chamfer plane lies inside the dumped face bbox (ignoring the edge
            direction, since later features trim the chamfer face).
        Cone faces (chamfer running round an earlier fillet corner) are matched by arc centre on the
        cone axis; tangent arcs/lines between matched edges are then added so OCC gets whole chains.
        Returns (edges, matched_face_for_each_edge)."""
        body = _one(self.body)
        emap = {}
        for fc in body.faces():
            for e in fc.edges():
                L = emap.setdefault(hash(e), [])
                if not any(fc.is_same(g) for g in L): L.append(fc)
        adj_faces = lambda E: emap.get(hash(E), [])
        dexp = size / math.sqrt(2.0)
        sel, mf = [], []
        planes = [F for F in faces if F.kind == 'plane']
        cones = [F for F in faces if F.kind == 'cone']
        for E in body.edges():
            gt = str(E.geom_type).split('.')[-1]
            m = np.array(tuple(E.position_at(0.5))); t = np.array(tuple(E.tangent_at(0.5)))
            hit = None
            if gt == 'LINE':
                for F in planes:
                    nn = np.array(F.params['n'], float); nn /= np.linalg.norm(nn); o = np.array(F.params['o']) * MM
                    if abs(t @ nn) > 1e-3: continue
                    dd = (m - o) @ nn
                    if abs(abs(dd) - dexp) > 0.05 * size: continue
                    if not in_box_perp(m - nn * dd, F.box, t, tol=0.05): continue
                    af = adj_faces(E)
                    if len(af) != 2: continue
                    if any(BRepAdaptor_Surface(fc.wrapped).GetType() != GeomAbs_Plane for fc in af): continue
                    ns = [np.array(tuple(fc.normal_at(Vector(*m)))) for fc in af]
                    b = ns[0] + ns[1]
                    if np.linalg.norm(b) < 1e-6: continue
                    b /= np.linalg.norm(b)
                    if abs(b @ nn) < 0.995: continue          # dumped normals are not always outward
                    if dd * (b @ nn) < 0: continue            # sharp edge must be outside the chamfer plane
                    q = m - 0.02 * size * b                   # convex edge: material just inside the corner
                    if BRepClass3d_SolidClassifier(body.wrapped, gp_Pnt(*q), 1e-7).State() != TopAbs_IN: continue
                    hit = F; break
            elif gt == 'CIRCLE':
                for F in cones:
                    v = F.params['values']; c = np.array(v[0:3]) * MM; ax = np.array(v[3:6], float)
                    try: cc = np.array(tuple(E.arc_center))
                    except Exception: continue
                    w = cc - c
                    if np.linalg.norm(w - ax * (w @ ax)) > 1e-3: continue
                    if F.box is not None:
                        lo = np.array(F.box[:3]) * MM - 0.05; hi = np.array(F.box[3:6]) * MM + 0.05
                        if np.any(m < lo) or np.any(m > hi): continue
                    hit = F; break
            if hit is not None: sel.append(E); mf.append(hit)
        # tangent-chain closure: add edges tangent-continuous with a selected edge at a shared vertex
        # whose midpoint lies inside some chamfer face box (e.g. the little arcs of a filleted corner)
        boxes = [F for F in faces if F.box is not None]
        def in_any_box(p):
            for F in boxes:
                lo = np.array(F.box[:3]) * MM - 0.6 * size; hi = np.array(F.box[3:6]) * MM + 0.6 * size
                if np.all(p >= lo) and np.all(p <= hi): return F
            return None
        changed = True
        while changed:
            changed = False
            for E in body.edges():
                if any(E.is_same(x) for x in sel): continue
                F = in_any_box(np.array(tuple(E.position_at(0.5))))
                if F is None: continue
                for X in list(sel):
                    for ue, ux in ((0, 0), (0, 1), (1, 0), (1, 1)):
                        pe = np.array(tuple(E.position_at(ue))); px = np.array(tuple(X.position_at(ux)))
                        if np.linalg.norm(pe - px) > 1e-5: continue
                        te = np.array(tuple(E.tangent_at(ue))); tx = np.array(tuple(X.tangent_at(ux)))
                        if abs(abs(te @ tx) - 1) < 1e-4:
                            sel.append(E); mf.append(F); changed = True; break
                    if changed: break
                if changed: break
        return sel, mf

    def blend_edges(self, f, kind, size, faces):
        edges = self.body.edges()
        if kind == 'chamfer' and not f.edges:
            sel, mf = self.chamfer_edges(size, faces)
            if sel:
                self._ef.extend(zip(sel, mf))
                return sel
        if f.edges:
            sel = []
            for a, b in f.edges:
                a = np.array(a) * MM; b = np.array(b) * MM
                sel.append(min(edges, key=lambda E: np.linalg.norm(np.array(tuple(E.position_at(0))) - a) +
                               np.linalg.norm(np.array(tuple(E.position_at(1))) - b)))
            return sel
        r = size
        sel = []
        for E in edges:
            m = np.array(tuple(E.position_at(0.5))); t = np.array(tuple(E.tangent_at(0.5)))
            gt = str(E.geom_type).split('.')[-1]
            ok = False
            for F in faces:
                if F.box is not None:
                    lo = np.array(F.box[:3]) * MM - 0.6 * r; hi = np.array(F.box[3:6]) * MM + 0.6 * r
                    if np.any(m < lo) or np.any(m > hi): continue
                if kind == 'fillet' and F.kind == 'cyl' and abs(F.params['r'] * MM - r) < 1e-3:
                    ax = np.array(F.params['ax']); ax /= np.linalg.norm(ax)
                    if abs(abs(t @ ax) - 1) > 1e-3: continue
                    v = m - np.array(F.params['o']) * MM; v -= ax * (v @ ax); dd = np.linalg.norm(v)
                    if 1.02 * r < dd < 2.0 * r:
                        q = m - v + v / dd * r          # radial projection onto the fillet cylinder
                        ok = in_box_perp(q, F.box, ax)
                elif kind == 'fillet' and F.kind == 'torus':
                    v = F.params['values']; c = np.array(v[0:3]) * MM; ax = np.array(v[3:6]); R_, rr = v[6] * MM, v[7] * MM
                    if abs(rr - r) > 1e-3: continue
                    w = m - c; h = w @ ax; rad = np.linalg.norm(w - ax * h)
                    dd = math.hypot(rad - R_, h)
                    if 1.02 * r < dd < 2.0 * r and abs(t @ ax) < 1e-3: ok = True
                elif kind == 'chamfer' and F.kind == 'plane':
                    nn = np.array(F.params['n']); o = np.array(F.params['o']) * MM
                    if gt != 'LINE' or abs(t @ nn) > 1e-3: continue
                    dd = (m - o) @ nn
                    if 0.3 * r < abs(dd) < 1.0 * r:          # sharp edge lies outside the chamfer plane
                        q = m - nn * dd
                        ok = in_box_perp(q, F.box, t)
                elif kind == 'chamfer' and F.kind == 'cone':
                    v = F.params['values']; c = np.array(v[0:3]) * MM; ax = np.array(v[3:6])
                    if gt != 'CIRCLE': continue
                    try:
                        cc = np.array(tuple(E.arc_center))
                    except Exception:
                        continue
                    w = cc - c
                    if np.linalg.norm(w - ax * (w @ ax)) < 1e-3: ok = True
                if ok: break
            if ok: sel.append(E); self._ef.append((E, F))
        return sel

    @staticmethod
    def chamfer_tool(body, E, r):
        """material removed by an equal-distance chamfer r on a convex edge E of body (LINE: triangular
        prism; CIRCLE: the triangle revolved about the arc axis).  Works where OCC's chamfer refuses,
        e.g. when the chamfer consumes a whole adjacent face (2 mm chamfer on a 2x2 mm flange) or runs
        round an earlier fillet.  Returns a Solid or None."""
        from build123d import Wire, revolve
        gt = str(E.geom_type).split('.')[-1]
        if gt not in ('LINE', 'CIRCLE'): return None
        p0 = np.array(tuple(E.position_at(0))); t = np.array(tuple(E.tangent_at(0))); t /= np.linalg.norm(t)
        adj = []
        for fc in body.faces():
            if any(e.is_same(E) for e in fc.edges()) and not any(fc.is_same(g) for g in adj): adj.append(fc)
        if len(adj) != 2: return None
        ns = []
        for fc in adj:
            n = np.array(tuple(fc.normal_at(Vector(*p0)))); n = n - t * (n @ t); ns.append(n / np.linalg.norm(n))
        us = []
        for i in (0, 1):
            u = -ns[1 - i]; u = u - ns[i] * (u @ ns[i]); us.append(u / np.linalg.norm(u))
        q = p0 + 0.02 * r * sum(-n for n in ns)
        if BRepClass3d_SolidClassifier(body.wrapped, gp_Pnt(*q), 1e-7).State() != TopAbs_IN: return None
        e = 1e-3   # tiny overshoot outwards so the cut leaves no sliver at the sharp edge
        poly = [p0 + e * (ns[0] + ns[1]), p0 + r * us[0] + e * ns[0], p0 + r * us[1] + e * ns[1]]
        if gt == 'LINE':
            p1 = np.array(tuple(E.position_at(1))); L = float(np.linalg.norm(p1 - p0))
            w = Wire.make_polygon([Vector(*(x - t * 1e-3)) for x in poly], close=True)
            return _one(extrude(Face(w), amount=L + 2e-3, dir=tuple(t)))
        c = np.array(tuple(E.arc_center)); ax = np.cross(p0 - c, t); ax /= np.linalg.norm(ax)
        p1 = np.array(tuple(E.position_at(1)))
        a0 = p0 - c; a1 = p1 - c
        ang = math.degrees(math.atan2(np.cross(a0, a1) @ ax, a0 @ a1)) % 360.0
        if ang < 1e-6: ang = 360.0
        w = Wire.make_polygon([Vector(*x) for x in poly], close=True)
        return _one(revolve(Face(w), Axis(tuple(c), tuple(ax)), ang))

    def manual_blend_on(self, body, E, F, r, kind):
        keep = self.body; self.body = body
        try: return self.manual_blend(E, F, r, kind)
        finally: self.body = keep

    def manual_blend(self, E, F, r, kind):
        """explicit blend for a straight edge: fillet from the dumped cylinder, chamfer from distance."""
        if F is None or str(E.geom_type).split('.')[-1] != 'LINE': return None
        p0 = np.array(tuple(E.position_at(0))); p1 = np.array(tuple(E.position_at(1)))
        t = (p1 - p0) / np.linalg.norm(p1 - p0)
        adj = [fc for fc in self.body.faces() if any(e.is_same(E) for e in fc.edges())]
        if len(adj) != 2: return None
        ns = []
        for fc in adj:
            ad = BRepAdaptor_Surface(fc.wrapped)
            if ad.GetType() != GeomAbs_Plane: return None
            n = np.array(tuple(fc.normal_at(fc.center())))
            ns.append(n - t * (n @ t))
        ns = [n / np.linalg.norm(n) for n in ns]
        if kind == 'fillet':
            if F.kind != 'cyl': return None
            ax = np.array(F.params['ax'], float); ax /= np.linalg.norm(ax)
            if abs(abs(ax @ t) - 1) > 1e-3: return None
            o = np.array(F.params['o']) * MM
            A = o + ax * ((p0 - o) @ ax); A += -t * (t @ (A - p0))
            Ts = [A - n * ((A - p0) @ n) for n in ns]
            poly = [p0, Ts[0], A, Ts[1]]
        else:
            us = []
            for i in (0, 1):
                u = -ns[1 - i]; u = u - ns[i] * (u @ ns[i]); us.append(u / np.linalg.norm(u))
            poly = [p0, p0 + r * us[0], p0 + r * us[1]]
        L = float(np.linalg.norm(p1 - p0))
        from build123d import Wire
        w = Wire.make_polygon([Vector(*q) for q in poly], close=True)
        pr = extrude(Face(w), amount=L, dir=tuple(t))
        if kind == 'fillet':
            cyl = Solid.make_cylinder(r, L + 2, Plane(origin=tuple(A - t), z_dir=tuple(t)))
            pr = pr.cut(cyl)
        # convex if the corner region is material
        q = p0 + 0.5 * t * L + 0.02 * r * sum(-n for n in ns)
        cls = BRepClass3d_SolidClassifier(self.body.wrapped, gp_Pnt(*q), 1e-7)
        convex = cls.State() == TopAbs_IN
        return _one(bop(self.body, pr, 'cut' if convex else 'fuse'))

    @staticmethod
    def edge_chains(sel):
        """connected components of the selected edges (shared end vertices)."""
        ends = [(np.array(tuple(E.position_at(0))), np.array(tuple(E.position_at(1)))) for E in sel]
        par = list(range(len(sel)))
        def root(i):
            while par[i] != i: i = par[i]
            return i
        for i in range(len(sel)):
            for j in range(i + 1, len(sel)):
                if min(np.linalg.norm(a - b) for a in ends[i] for b in ends[j]) < 1e-5:
                    par[root(i)] = root(j)
        groups = {}
        for i in range(len(sel)): groups.setdefault(root(i), []).append(i)
        return list(groups.values())

    def _chamfer_chains(self, f, sel, size, op, score, s0, v0, bulk):
        """apply a chamfer chain by chain (OCC chamfer of the chain, else cut of the explicit chamfer tools),
        each chain kept only if the IoU vs the reference improves; falls back to single edges."""
        cur, sc, done = self.body, s0, 0
        applied = []
        for g in self.edge_chains(sel):
            es = [sel[i] for i in g]
            def occ(es=es):
                ce = []
                for E in es:
                    E2 = min(cur.edges(), key=lambda x: (x.center() - E.center()).length)
                    if (E2.center() - E.center()).length > 1e-4: return None
                    ce.append(E2)
                return op(cur, ce)
            def manual(es=es):
                body = _one(cur); tools = [self.chamfer_tool(body, E, size) for E in es]
                if any(T is None for T in tools): return None
                T = tools[0]
                for X in tools[1:]: T = bop(T, X, 'fuse')
                return _one(bop(body, T, 'cut'))
            best = None
            for how, t_ in (('occ', occ), ('manual', manual)):
                try:
                    nb = t_()
                    if nb is None or not nb.is_valid or vol(nb) < 0.5 * v0: continue
                    s1 = score(nb)
                    if s1 > sc + 1e-6 and (best is None or s1 > best[0]): best = (s1, nb, how)
                except Exception:
                    pass
            if best is not None:
                sc, cur = best[0], best[1]; done += len(es); applied.append((best[2], [self._edesc(E) for E in es]))
                continue
            # chain rejected as a whole: try its edges one by one with the explicit tool
            for E in es:
                try:
                    T = self.chamfer_tool(_one(cur), E, size)
                    if T is None: continue
                    nb = _one(bop(cur, T, 'cut'))
                    if not nb.is_valid: continue
                    s1 = score(nb)
                    if s1 > sc + 1e-6:
                        sc, cur = s1, nb; done += 1; applied.append(('manual1', [self._edesc(E)]))
                except Exception:
                    pass
        self._applied = applied
        if bulk is not None and bulk[0] >= sc and bulk[0] > s0:
            self.body = bulk[1]; self._applied = [('occ-bulk', [self._edesc(E) for E in sel])]; return bulk[2]
        if sc > s0:
            self.body = cur; return done
        self._applied = []
        return 0

    @staticmethod
    def _edesc(E):
        gt = str(E.geom_type).split('.')[-1]
        a = np.round(tuple(E.position_at(0)), 2).tolist(); b = np.round(tuple(E.position_at(1)), 2).tolist()
        return f'{gt} {a}->{b}'

    def blend_feature(self, f, mirror=None):
        bp = blend_params(f)
        if bp is None or bp[1] is None:
            log(f.name, 'SKIP', 'no size'); return
        kind, size = bp[0], bp[1] * MM
        faces = f.faces if mirror is None else [self.mirror_surface(F, mirror) for F in f.faces]
        self._ef = []
        sel = self.blend_edges(f, kind, size, faces)
        if not sel:
            log(f.name, 'SKIP', f'{kind} {size}: no matching edges'); return
        op = (lambda b, es: _one(b).fillet(size, es)) if kind == 'fillet' else (lambda b, es: _one(b).chamfer(size, None, es))
        v0 = vol(self.body)
        R = self.ref
        score = (lambda B: R.miou(R.G.inside(B))) if R is not None else (lambda B: 0.0)
        s0 = R.miou(self.bin) if R is not None else 0.0
        # (a) all matched edges at once
        bulk = None
        try:
            nb = op(self.body, sel)
            if nb is not None and nb.is_valid: bulk = (score(nb), nb, len(sel))
        except Exception:
            pass
        if R is None and bulk is not None:
            self.body = bulk[1]; done = len(sel)
        elif kind == 'chamfer' and not f.edges:
            done = self._chamfer_chains(f, sel, size, op, score, s0, v0, bulk)
        else:
            # (b) greedy per edge, kept only if the voxel IoU vs the reference improves
            cur, sc, done = self.body, s0, 0
            for E in sel:
                tries = []
                try:
                    E2 = min(cur.edges(), key=lambda x: (x.center() - E.center()).length)
                    if (E2.center() - E.center()).length < 1e-4:
                        tries.append(lambda E2=E2: op(cur, [E2]))
                except Exception:
                    pass
                F = next((F for e_, F in self._ef if e_ is E), None)
                tries.append(lambda: self.manual_blend_on(cur, E, F, size, kind))
                for t_ in tries:
                    try:
                        nb = t_()
                        if nb is None or not nb.is_valid or vol(nb) < 0.5 * v0: continue
                        s1 = score(nb)
                        if s1 > sc + 1e-6:
                            cur, sc = nb, s1; done += 1; break
                    except Exception:
                        pass
            if bulk is not None and bulk[0] >= sc and bulk[0] > s0:
                self.body, done = bulk[1], bulk[2]
            elif sc > s0:
                self.body = cur
            else:
                done = 0
        if self.ref is not None and done:
            self.bin = self.ref.G.inside(self.body)
        if mirror is None: self.tools[f.name] = ('blend', (kind, size))
        tag = f.name + ('(mirror)' if mirror is not None else '')
        log(tag, 'OK' if done == len(sel) else 'PART', f'{kind} {size:g}', edges=f'{done}/{len(sel)}',
            vol=round(vol(self.body), 1), iou=round(self.ref.miou(self.bin), 4) if self.ref else None)
        self.choice[tag] = dict(kind=kind, size=size, edges_matched=len(sel), edges_applied=done)
        if kind == 'chamfer' and getattr(self, '_applied', None):
            self.choice[tag]['applied'] = self._applied
            for how, es in self._applied:
                print(f'      {how:8s} ' + ' | '.join(es), flush=True)
        self._applied = []

    # --- mirror ----------------------------------------------------------
    def mirror_feature(self, f):
        planes = [self.part.by_name[n] for n, t in f.parents if t == 'RefPlane']
        if not planes or planes[0].plane is None:
            log(f.name, 'SKIP', 'mirror plane not a RefPlane'); return
        a = planes[0].plane
        nrm = Vector(*a[6:9]); org = Vector(*(np.array(a[9:12]) * MM))
        mp = Plane(origin=org, z_dir=nrm)
        order = [x.name for x in self.part.features]
        srcs = sorted([n for n, t in f.parents if n in self.tools], key=order.index)
        for n in srcs:
            kind, T = self.tools[n]
            if kind == 'blend':
                self.blend_feature(self.part.by_name[n], mirror=(np.array(a[6:9], float), np.array(a[9:12], float))); continue
            M = T.mirror(mp)
            self.body = bop(self.body, M, 'fuse' if kind == 'boss' else 'cut')
            if self.ref is not None:
                inM = self.ref.pts_in(M)
                self.bin = (self.bin | inM) if kind == 'boss' else (self.bin & ~inM)
        log(f.name, 'OK', 'mirror of ' + ','.join(srcs), vol=round(vol(self.body), 1))

    def run(self, start=None, ckpt=None):
        import pickle
        feats = [f for f in self.part.features if not f.suppressed]
        names = [f.name for f in feats]
        i0 = 0
        if start:
            i0 = names.index(start)
            prev = [n for n in names[:i0] if os.path.exists(os.path.join(ckpt, n + '.pkl'))]
            if prev:
                with open(os.path.join(ckpt, prev[-1] + '.pkl'), 'rb') as fh:
                    st = pickle.load(fh)
                self.body, self.tools, self.choice, self.bin = st['body'], st['tools'], st['choice'], st['bin']
                LOG[:] = st['log']
        for f in feats[i0:]:
            prev = self.body
            self._run_one(f)
            if self.body is not None and self.body is not prev:
                ok = self.body.is_valid
                if not ok:
                    from OCP.ShapeFix import ShapeFix_Shape
                    sf = ShapeFix_Shape(self.body.wrapped); sf.Perform()
                    fx = Compound(sf.Shape()) if not isinstance(self.body, Solid) else Solid(sf.Shape())
                    if fx.is_valid: self.body = fx
                    print(f'   !! {f.name}: body invalid; shapefix -> {fx.is_valid}', flush=True)
                    LOG.append(dict(feature=f.name, status='INVALID', fixed=bool(fx.is_valid)))
            if ckpt and (f.extrude is not None or f.type in ('Fillet', 'MirrorPattern') or f.type.startswith('Chamfer')):
                with open(os.path.join(ckpt, f.name + '.pkl'), 'wb') as fh:
                    pickle.dump(dict(body=_clean(self.body), tools={k: (a, _clean(b)) for k, (a, b) in self.tools.items()}, choice=self.choice, log=LOG, bin=self.bin), fh)
        return self.body

    def _run_one(self, f):
        if True:
            if f.extrude is not None: self.extrude_feature(f)
            elif f.type == 'Fillet' or f.type.startswith('Chamfer'): self.blend_feature(f)
            elif f.type == 'MirrorPattern': self.mirror_feature(f)
            elif f.type in ('ProfileFeature', 'RefPlane', 'OriginProfileFeature') or f.idx < 0 or 'Folder' in f.type \
                    or f.type in ('DetailCabinet',):
                return
            else:
                log(f.name, 'SKIP', f'unsupported type {f.type}')


# ----------------------------------------------------------------------------- comparison
def load_ref():
    """reference solid in the part frame (only for queries/comparison)."""
    ref_asm = import_brep(REF_BREP)
    inv = trsf_from(ASM_ROWS, ASM_T).inverse()
    return ref_asm.moved(inv)


def _tri(shape, tol=0.02):
    V, T = shape.tessellate(tol, 0.2)
    V = np.array([tuple(v) for v in V]); T = np.array(T)
    ar = 0.5 * np.linalg.norm(np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]), axis=1)
    return V, T[np.isfinite(ar) & (ar > 1e-10)]


def sample_surface(V, T, n, rng):
    A = V[T[:, 0]]; B = V[T[:, 1]]; C = V[T[:, 2]]
    ar = 0.5 * np.linalg.norm(np.cross(B - A, C - A), axis=1)
    idx = rng.choice(len(T), n, p=ar / ar.sum())
    u = rng.random(n); v = rng.random(n); m = u + v > 1; u[m] = 1 - u[m]; v[m] = 1 - v[m]
    return A[idx] + u[:, None] * (B[idx] - A[idx]) + v[:, None] * (C[idx] - A[idx])


def pt_tri_dist(P, A, B, C):
    ab = B - A; ac = C - A; ap = P - A
    d1 = (ab * ap).sum(1); d2 = (ac * ap).sum(1)
    bp = P - B; d3 = (ab * bp).sum(1); d4 = (ac * bp).sum(1)
    cp = P - C; d5 = (ab * cp).sum(1); d6 = (ac * cp).sum(1)
    va = d3 * d6 - d5 * d4; vb = d5 * d2 - d1 * d6; vc = d1 * d4 - d3 * d2
    den = va + vb + vc; den[den == 0] = 1e-30
    v = vb / den; w = vc / den
    Q = A + ab * v[:, None] + ac * w[:, None]
    def setq(mask, q): Q[mask] = q[mask]
    with np.errstate(divide='ignore', invalid='ignore'):
        m = (d1 <= 0) & (d2 <= 0); setq(m, A)
        m = (d3 >= 0) & (d4 <= d3); setq(m, B)
        m = (d6 >= 0) & (d5 <= d6); setq(m, C)
        t = d1 / (d1 - d3); m = (vc <= 0) & (d1 >= 0) & (d3 <= 0); setq(m, A + ab * t[:, None])
        t = d2 / (d2 - d6); m = (vb <= 0) & (d2 >= 0) & (d6 <= 0); setq(m, A + ac * t[:, None])
        t = (d4 - d3) / ((d4 - d3) + (d5 - d6)); m = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0); setq(m, B + (C - B) * t[:, None])
    return np.linalg.norm(P - Q, axis=1)


def surf_dev(P, V, T, k=16):
    from scipy.spatial import cKDTree
    cen = (V[T[:, 0]] + V[T[:, 1]] + V[T[:, 2]]) / 3
    _, nn = cKDTree(cen).query(P, k)
    best = np.full(len(P), np.inf)
    for j in range(k):
        t = T[nn[:, j]]
        best = np.minimum(best, pt_tri_dist(P, V[t[:, 0]], V[t[:, 1]], V[t[:, 2]]))
    return best


def compare(ours, ref):
    rng = np.random.default_rng(0)
    extra = bop(ours, ref, 'cut'); missing = bop(ref, ours, 'cut'); common = bop(ours, ref, 'common')
    cv = vol(ours) - vol(extra)
    res = dict(volume=dict(ours=vol(ours), ref=vol(ref)),
               extra=vol(extra), missing=vol(missing), common=cv, common_bop=vol(common),
               iou=cv / (vol(ours) + vol(ref) - cv))
    bo, br = ours.bounding_box(), ref.bounding_box()
    res['bbox'] = dict(ours=[list(map(float, bo.min)), list(map(float, bo.max))], ref=[list(map(float, br.min)), list(map(float, br.max))])
    Vo, To = _tri(ours); Vr, Tr = _tri(ref)
    Po = sample_surface(Vo, To, 40000, rng); Pr = sample_surface(Vr, Tr, 40000, rng)
    d1 = surf_dev(Po, Vr, Tr); d2 = surf_dev(Pr, Vo, To)
    res['dev'] = dict(ours_to_ref_max=float(d1.max()), ours_to_ref_mean=float(d1.mean()),
                      ref_to_ours_max=float(d2.max()), ref_to_ours_mean=float(d2.mean()),
                      frac_within_0p05=float(((d1 < 0.05).mean() + (d2 < 0.05).mean()) / 2))
    pieces = []
    for lab, S in (('extra', extra), ('missing', missing)):
        if S is None: continue
        for s in sorted(S.solids(), key=lambda x: -x.volume)[:12]:
            if s.volume < 0.5: continue
            b = s.bounding_box()
            pieces.append(dict(kind=lab, vol=round(s.volume, 2), lo=[round(x, 2) for x in tuple(b.min)], hi=[round(x, 2) for x in tuple(b.max)]))
    res['pieces'] = pieces
    return res


def render(shapes, titles, path, views):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(6 * len(shapes), 5.2 * len(views)))
    k = 1
    for elev, azim, vn in views:
        for sh, ti in zip(shapes, titles):
            V, T = _tri(sh, 0.05)
            ax = fig.add_subplot(len(views), len(shapes), k, projection='3d'); k += 1
            tri = V[T]; nn = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); nn /= np.linalg.norm(nn, axis=1)[:, None] + 1e-12
            e_, a_ = np.radians(elev), np.radians(azim)
            L = np.array([np.cos(e_) * np.cos(a_), np.cos(e_) * np.sin(a_), np.sin(e_)]) + np.array([0.3, -0.2, 0.5])
            L /= np.linalg.norm(L); sh_ = 0.35 + 0.65 * np.abs(nn @ L)
            ax.add_collection3d(Poly3DCollection(tri, facecolors=np.c_[sh_ * 0.35, sh_ * 0.55, sh_ * 0.85, np.ones(len(sh_))], edgecolor='none'))
            lo, hi = V.min(0), V.max(0); c = (lo + hi) / 2; r = (hi - lo).max() / 2
            ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
            ax.view_init(elev, azim); ax.set_box_aspect((1, 1, 1)); ax.set_title(f'{ti} - {vn}'); ax.set_axis_off()
    plt.tight_layout(); plt.savefig(path, dpi=90); plt.close(fig)


def main():
    t0 = time.time()
    ref = load_ref()
    R = Ref(ref); R.init_points(cache=os.path.join(HERE, 'ckpt', 'refpts.npz'))
    rb = Rebuild(ref=None if '--no-ref-select' in sys.argv else R)
    ck = os.path.join(HERE, 'ckpt'); os.makedirs(ck, exist_ok=True)
    st = sys.argv[sys.argv.index('--from') + 1] if '--from' in sys.argv else None
    ours = rb.run(start=st, ckpt=ck)
    if '--until-only' in sys.argv: return
    export_step(ours, os.path.join(HERE, 'rv01_from_dump.step'))
    out = dict(build_seconds=round(time.time() - t0, 1), choices=rb.choice, log=LOG)
    if '--compare' in sys.argv:
        r = compare(ours, ref)
        oin = R.G.inside(ours)
        r['points'] = dict(n=int(np.prod(R.G.n)), iou=float(R.miou(oin)), extra=float((oin & ~R.rin).sum() * R.dv),
                           missing=float((~oin & R.rin).sum() * R.dv), tracked_iou=float(R.miou(rb.bin)) if rb.bin is not None else None)
        if not (0.3 < r['iou'] <= 1.0) or r['extra'] > 0.5 * r['volume']['ours']:   # BOPs with ref broke
            r['bop_failed'] = True; r['iou'] = r['points']['iou']; r['extra'] = r['points']['extra']; r['missing'] = r['points']['missing']
        out['compare'] = r
        print(json.dumps({k: v for k, v in r.items()}, indent=1, default=float))
        if '--render' in sys.argv:
            render([ours, ref], ['ours (from dump)', 'reference STEP'], os.path.join(HERE, 'rv01_dump_iso.png'), [(30, -60, 'iso')])
            render([ours, ref], ['ours (from dump)', 'reference STEP'], os.path.join(HERE, 'rv01_dump_top.png'), [(90, -90, 'top (+Z)')])
    with open(os.path.join(HERE, 'rv01_from_dump.log.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=float)


if __name__ == '__main__':
    main()
