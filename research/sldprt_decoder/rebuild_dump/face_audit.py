"""Face-by-face audit: rebuilt STEP vs SolidWorks dump FACE lines (dumps_v2).

Usage:
    python face_audit.py <part.dump.txt> <rebuild.step> [--json out.json] [--md out.md]

Method
  * Dump faces (metres) -> mm.  STEP faces read with build123d/OCP.
  * Every face becomes a Face record: kind, canonical surface key, bbox, area, owning feature.
  * Faces lying on the same surface whose bboxes touch are merged into a *patch*
    (SolidWorks splits full cylinders into halves, OCC keeps one periodic face; splits also
    differ along edges), so the comparison is patch-vs-patch.
  * Pass 1  exact: same kind + same surface + bbox within BOX_TOL  -> match (area check).
  * Pass 2  same surface, bbox differs -> 'trim' (wrong extent / partially built).
  * Pass 3  same kind, bbox overlap, different radius/params -> 'param' (e.g. hole radius).
  * Remaining dump patches -> 'missing'; remaining rebuild patches -> 'extra'.
Exit code 0 always; returns structured result from audit().
"""
from __future__ import annotations
import argparse, json, math, os, sys
from dataclasses import dataclass, field, asdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LEN_TOL = 0.01      # mm, surface parameter tolerance
ANG_TOL = 1e-3      # rad / unit-vector component tolerance
BOX_TOL = 0.05      # mm, bbox coordinate tolerance (dump boxes are padded by 5e-6 m)
AREA_TOL = 0.01     # relative
TOUCH = 0.02        # mm, bboxes closer than this are 'touching' for patch merge
CANON_TOL = 1e-6    # mm, B-spline faces this close to an analytic surface are classified as it (round 17)


@dataclass
class Face:
    kind: str                 # plane cyl cone torus sphere surf
    key: tuple                # canonical surface parameters (mm/rad)
    box: list                 # xmin ymin zmin xmax ymax zmax (mm)
    area: float               # mm^2
    feature: str = ''
    radius: float | None = None
    minor: float | None = None


@dataclass
class Patch:
    faces: list = field(default_factory=list)

    @property
    def kind(self): return self.faces[0].kind
    @property
    def key(self): return self.faces[0].key
    @property
    def radius(self): return self.faces[0].radius
    @property
    def minor(self): return self.faces[0].minor
    @property
    def area(self): return sum(f.area for f in self.faces)
    @property
    def box(self):
        b = [f.box for f in self.faces]
        return [min(x[i] for x in b) for i in range(3)] + [max(x[i] for x in b) for i in range(3, 6)]
    @property
    def features(self): return sorted({n for f in self.faces for n in f.feature.split('+') if n})

    def desc(self):
        b = self.box
        c = ', '.join(f'{(b[i] + b[i + 3]) / 2:.2f}' for i in range(3))
        s = f'{self.kind}'
        if self.radius is not None:
            s += f' r={self.radius:.3f}'
        if self.minor is not None:
            s += f'/{self.minor:.3f}'
        return f'{s} @({c}) A={self.area:.3f}'


# ---------------------------------------------------------------- canonical keys
def _unit(v):
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    v = [x / n for x in v]
    # canonical sign: first significant component positive
    for x in v:
        if abs(x) > 1e-9:
            if x < 0:
                v = [-y for y in v]
            break
    return tuple(v)


def _line_key(o, ax):
    """Canonical infinite line: unit dir + point closest to origin."""
    d = _unit(ax)
    t = sum(o[i] * d[i] for i in range(3))
    p = tuple(o[i] - t * d[i] for i in range(3))
    return d, p


def plane_key(n, o):
    n = _unit(n)
    return ('plane', n, sum(n[i] * o[i] for i in range(3)))


def cyl_key(o, ax, r):
    d, p = _line_key(o, ax)
    return ('cyl', d, p, r)


def cone_key(o, ax, r, ang):
    d, p = _line_key(o, ax)
    return ('cone', d, p, abs(ang))          # apex position along line differs by convention


def torus_key(c, ax, R, r):
    return ('torus', _unit(ax), tuple(c), R, r)


def sphere_key(c, r):
    return ('sphere', tuple(c), r)


def _close(a, b):
    if isinstance(a, str) or isinstance(b, str):
        return a == b
    if isinstance(a, (tuple, list)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    return abs(a - b) <= max(LEN_TOL, ANG_TOL)


def same_surface(a: Face | Patch, b: Face | Patch) -> bool:
    if a.kind != b.kind:
        return False
    if a.kind == 'surf':
        return box_close(a.box, b.box, 0.2)
    return _close(a.key, b.key)


def box_close(a, b, tol=BOX_TOL):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def box_overlap(a, b, pad=0.0):
    return all(a[i] - pad <= b[i + 3] and b[i] - pad <= a[i + 3] for i in range(3))


def box_iou(a, b):
    def vol(x):
        return max(1e-3, x[3] - x[0]) * max(1e-3, x[4] - x[1]) * max(1e-3, x[5] - x[2])
    lo = [max(a[i], b[i]) for i in range(3)]
    hi = [min(a[i + 3], b[i + 3]) for i in range(3)]
    if any(hi[i] < lo[i] - 1e-6 for i in range(3)):
        return 0.0
    inter = vol(lo + hi)
    return inter / (vol(a) + vol(b) - inter)


# ---------------------------------------------------------------- loaders
def faces_from_dump(path: str) -> list[Face]:
    from dump_parser import parse_dump
    part = parse_dump(path)
    out = []

    def walk(feats):
        for f in feats:
            for s in f.faces:
                out.append(_dump_face(s, f.name))

    walk(part.features)
    return dedupe(out)


def dedupe(faces: list[Face]) -> list[Face]:
    """A dump lists a final-body face under every feature that touched it; keep one copy."""
    out: list[Face] = []
    for f in faces:
        for g in out:
            if same_surface(g, f) and box_close(g.box, f.box, 0.02) and \
                    abs(g.area - f.area) <= 1e-3 * max(g.area, 1e-9) + 1e-4:
                if f.feature not in g.feature.split('+'):
                    g.feature += '+' + f.feature
                break
        else:
            out.append(f)
    return out


def _dump_face(s, feat) -> Face:
    m = 1000.0
    box = [x * m for x in s.box] if s.box else [0] * 6
    area = (s.area or 0) * 1e6
    p = s.params
    if s.kind == 'plane':
        return Face('plane', plane_key(p['n'], [x * m for x in p['o']]), box, area, feat)
    if s.kind == 'cyl':
        r = p['r'] * m
        return Face('cyl', cyl_key([x * m for x in p['o']], p['ax'], r), box, area, feat, r)
    v = p.get('values', [])
    if s.kind == 'cone':
        r = v[6] * m
        return Face('cone', cone_key([x * m for x in v[:3]], v[3:6], r, v[7]), box, area, feat, r,
                    math.degrees(v[7]))
    if s.kind == 'torus':
        R, r = v[6] * m, v[7] * m
        return Face('torus', torus_key([x * m for x in v[:3]], v[3:6], R, r), box, area, feat, R, r)
    if s.kind == 'sphere':
        r = v[3] * m
        return Face('sphere', sphere_key([x * m for x in v[:3]], r), box, area, feat, r)
    return Face('surf', ('surf',), box, area, feat)


def faces_from_step(path: str) -> list[Face]:
    from build123d import import_step
    return faces_from_shape(import_step(path))


def faces_from_shape(shape) -> list[Face]:
    """Face records of a build123d shape (round 17: used directly, without a STEP round trip)."""
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import (GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Torus,
                             GeomAbs_Sphere)
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    out = []
    for f in shape.faces():
        ad = BRepAdaptor_Surface(f.wrapped)
        t = ad.GetType()
        if t not in (GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Torus, GeomAbs_Sphere):
            ad = _canonical(f, ad); t = ad.GetType()
        bb = Bnd_Box(); bb.SetGap(0.0)
        BRepBndLib.AddOptimal_s(f.wrapped, bb, False, False)
        mn, mx = bb.CornerMin(), bb.CornerMax()
        box = [mn.X(), mn.Y(), mn.Z(), mx.X(), mx.Y(), mx.Z()]
        area = f.area

        def P(p): return (p.X(), p.Y(), p.Z())
        if t == GeomAbs_Plane:
            pl = ad.Plane(); ax = pl.Axis()
            out.append(Face('plane', plane_key(P(ax.Direction()), P(ax.Location())), box, area))
        elif t == GeomAbs_Cylinder:
            c = ad.Cylinder(); ax = c.Axis(); r = c.Radius()
            out.append(Face('cyl', cyl_key(P(ax.Location()), P(ax.Direction()), r), box, area, '', r))
        elif t == GeomAbs_Cone:
            c = ad.Cone(); ax = c.Axis(); r = c.RefRadius()
            out.append(Face('cone', cone_key(P(ax.Location()), P(ax.Direction()), r, c.SemiAngle()),
                            box, area, '', r, math.degrees(abs(c.SemiAngle()))))
        elif t == GeomAbs_Torus:
            c = ad.Torus(); ax = c.Axis()
            out.append(Face('torus', torus_key(P(ax.Location()), P(ax.Direction()), c.MajorRadius(),
                                               c.MinorRadius()), box, area, '', c.MajorRadius(),
                            c.MinorRadius()))
        elif t == GeomAbs_Sphere:
            c = ad.Sphere()
            out.append(Face('sphere', sphere_key(P(c.Location()), c.Radius()), box, area, '',
                            c.Radius()))
        else:
            out.append(Face('surf', ('surf',), box, area))
    return out


def _canonical(f, ad, tol=CANON_TOL):
    """Round 17: a rebuilt B-spline face that is exactly (within tol mm) a plane / cylinder / cone /
    sphere / torus is classified as that analytic surface (OCC fillets of some edge chains come
    out as B-splines that are geometrically cylinders: Top Panel Fillet1).  Other faces unchanged."""
    try:
        from OCP.GeomConvert import GeomConvert_SurfToAnaSurf
        from OCP.GeomAdaptor import GeomAdaptor_Surface
        from OCP.BRep import BRep_Tool
        c = GeomConvert_SurfToAnaSurf(BRep_Tool.Surface_s(f.wrapped))
        s = c.ConvertToAnalytical(tol)
        if s is not None and c.Gap() <= tol: return GeomAdaptor_Surface(s)
    except Exception:
        pass
    return ad


# ---------------------------------------------------------------- patches + matching
def make_patches(faces: list[Face]) -> list[Patch]:
    patches: list[Patch] = []
    for f in faces:
        hit = [p for p in patches if same_surface(p.faces[0], f) and
               any(box_overlap(g.box, f.box, TOUCH) for g in p.faces)]
        if not hit:
            patches.append(Patch([f]))
            continue
        base = hit[0]; base.faces.append(f)
        for p in hit[1:]:
            base.faces.extend(p.faces); patches.remove(p)
    return patches


def audit(dump_faces: list[Face], our_faces: list[Face]) -> dict:
    D = make_patches(dump_faces)
    O = make_patches(our_faces)
    used = set()
    res = dict(matched=[], area=[], trim=[], param=[], split=[], missing=[], extra=[],
               counts=dict(dump_faces=len(dump_faces), our_faces=len(our_faces),
                           dump_patches=len(D), our_patches=len(O)))

    def take(pred, score):
        out = []
        for d in D:
            if id(d) in done:
                continue
            cands = [(score(d, o), k, o) for k, o in enumerate(O) if k not in used and pred(d, o)]
            if cands:
                _, k, o = max(cands, key=lambda x: x[0])
                used.add(k); done.add(id(d)); out.append((d, o))
        return out
    done = set()
    # pass 1 exact
    for d, o in take(lambda d, o: same_surface(d, o) and box_close(d.box, o.box),
                     lambda d, o: -abs(d.area - o.area)):
        rel = abs(o.area - d.area) / max(d.area, 1e-9)
        (res['area'] if rel > AREA_TOL else res['matched']).append(_pair(d, o, rel))
    # pass 2 same surface, different trim
    for d, o in take(lambda d, o: same_surface(d, o) and box_overlap(d.box, o.box, TOUCH),
                     lambda d, o: box_iou(d.box, o.box)):
        res['trim'].append(_pair(d, o, abs(o.area - d.area) / max(d.area, 1e-9)))
    # pass 3 same kind, overlapping, different parameters (radius etc.)
    for d, o in take(lambda d, o: d.kind == o.kind and d.kind != 'plane' and box_iou(d.box, o.box) > 0.2,
                     lambda d, o: box_iou(d.box, o.box)):
        res['param'].append(_pair(d, o, abs(o.area - d.area) / max(d.area, 1e-9)))
    # pass 4 split: leftover dump patch on a surface already paired with a rebuild patch
    for d in D:
        if id(d) in done:
            continue
        for k, o in enumerate(O):
            if k in used and same_surface(d, o) and box_overlap(d.box, o.box, TOUCH):
                done.add(id(d)); res['split'].append(dict(dump=_pd(d), ours=_pd(o))); break
    for d in D:
        if id(d) not in done:
            # nearest rebuild face of other type at same place (e.g. cyl rebuilt as polyline planes)
            near = [o for o in O if box_iou(d.box, o.box) > 0.3]
            res['missing'].append(dict(dump=_pd(d), near=[o.desc() for o in near[:4]]))
    for k, o in enumerate(O):
        if k not in used:
            if any(same_surface(o, d) and box_overlap(d.box, o.box, TOUCH) for d in D):
                res['split'].append(dict(dump=None, ours=_pd(o)))
            else:
                res['extra'].append(dict(ours=_pd(o)))
    for m in res['missing']:
        m['blend'] = is_blend(m['dump'])
    res['counts'].update({k: len(v) for k, v in res.items() if isinstance(v, list)})
    return res


def is_blend(pd: dict) -> bool:
    """Dump face created by a Fillet/Chamfer feature (or a blend surface type)."""
    return pd['kind'] in ('torus', 'sphere') or any(
        f.startswith(('Fillet', 'Chamfer')) for f in pd['features'])


def _pd(p: Patch):
    return dict(kind=p.kind, radius=p.radius, minor=p.minor, area=round(p.area, 4),
                box=[round(x, 3) for x in p.box], features=p.features, n_faces=len(p.faces),
                desc=p.desc())


def _pair(d, o, rel):
    return dict(dump=_pd(d), ours=_pd(o), area_rel=round(rel, 4))


def where(box) -> str:
    """Human position label (RV01 frame: -Y = front wall, +Z = top)."""
    c = [(box[i] + box[i + 3]) / 2 for i in range(3)]
    side = 'centre' if abs(c[0]) < 1 else ('right(+X)' if c[0] > 0 else 'left(-X)')
    return f"{side} y={c[1]:.1f} z={c[2]:.1f}"


def to_markdown(r: dict, title='') -> str:
    L = [f'## Face audit {title}', '',
         '| class | count |', '|---|---|']
    L += [f'| {k} | {v} |' for k, v in r['counts'].items()]

    def row(*c): return '| ' + ' | '.join(str(x) for x in c) + ' |'
    # (a) cylinders that are not fillet faces
    L += ['', '### (a) Cylindrical holes/bosses: radius, extent or presence differs', '',
          row('position', 'dump feature', 'dump r', 'ours r', 'status', 'dump area', 'ours area'),
          row(*['---'] * 7)]
    for cls in ('param', 'trim', 'missing', 'extra'):
        for x in r[cls]:
            d, o = x.get('dump'), x.get('ours')
            ref = d or o
            if ref['kind'] != 'cyl' or (d and is_blend(d)):
                continue
            L.append(row(where(ref['box']), ','.join(d['features']) if d else '-',
                         f"{d['radius']:.3f}" if d else '-', f"{o['radius']:.3f}" if o else '-', cls,
                         f"{d['area']:.2f}" if d else '-', f"{o['area']:.2f}" if o else '-'))
    # (b) missing blends
    L += ['', '### (b) Missing / wrong blend faces (fillet, chamfer)', '',
          row('feature', 'kind', 'r / size', 'position', 'status', 'dump area', 'nearest rebuild face'),
          row(*['---'] * 7)]
    for x in r['missing']:
        d = x['dump']
        if x['blend']:
            L.append(row(','.join(d['features']), d['kind'],
                         '' if d['radius'] is None else f"{d['radius']:.3f}", where(d['box']), 'missing',
                         f"{d['area']:.2f}", '; '.join(x['near'][:2]) or '-'))
    for cls in ('trim', 'param'):
        for x in r[cls]:
            d, o = x['dump'], x['ours']
            if is_blend(d) and x['area_rel'] > AREA_TOL:
                L.append(row(','.join(d['features']), d['kind'],
                             '' if d['radius'] is None else f"{d['radius']:.3f}", where(d['box']),
                             f"{cls} (area {x['area_rel']:+.0%})", f"{d['area']:.2f}", o['desc']))
    L += ['', '### (c) Extra rebuild faces (no counterpart in dump)', '',
          row('kind', 'r', 'position', 'area'), row(*['---'] * 4)]
    for x in r['extra']:
        o = x['ours']
        L.append(row(o['kind'], '' if o['radius'] is None else f"{o['radius']:.3f}", where(o['box']),
                     f"{o['area']:.3f}"))
    L += ['', '### (d) Non-blend faces present on both sides with area mismatch > 1% (or other non-blend missing)', '',
          row('dump feature', 'kind', 'position', 'dump area', 'ours area', 'rel'), row(*['---'] * 6)]
    for cls in ('area', 'trim', 'param'):
        for x in r[cls]:
            d, o = x['dump'], x['ours']
            if not is_blend(d) and d['kind'] != 'cyl' and x['area_rel'] > AREA_TOL:
                L.append(row(','.join(d['features']), d['kind'], where(d['box']), f"{d['area']:.2f}",
                             f"{o['area']:.2f}", f"{x['area_rel']:.1%}"))
    for x in r['missing']:
        d = x['dump']
        if not x['blend'] and d['kind'] != 'cyl':
            L.append(row(','.join(d['features']), d['kind'], where(d['box']), f"{d['area']:.2f}", 'MISSING', ''))
    return '\n'.join(L) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('dump'); ap.add_argument('step')
    ap.add_argument('--json'); ap.add_argument('--md')
    a = ap.parse_args(argv)
    r = audit(faces_from_dump(a.dump), faces_from_step(a.step))
    print(json.dumps(r['counts'], indent=1))
    if a.json:
        json.dump(r, open(a.json, 'w'), indent=1)
    if a.md:
        open(a.md, 'w').write(to_markdown(r, os.path.basename(a.step)))
    return r


if __name__ == '__main__':
    main()
