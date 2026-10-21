"""Fillets and chamfers of a reference B-rep (STEP solid), found from the geometry alone.

    python -m robot.cad.blend_finder rvrn_2.0.step <solid index>

A fillet face is a cylinder / torus / sphere face that meets its neighbours tangentially (G1) along its long edges;
a chamfer face is a narrow plane (or 45 deg cone) whose long edges meet both neighbours at the same non-tangent angle.
Blend faces of the same kind and size that share an edge form a tangent chain (one fillet / chamfer the designer
picked). For each chain: kind, size (radius, or chamfer leg) to RES mm, angle, convex/concave, its faces, the
spine (the sharp edge it replaced, approximated by the face centre line) and the corner it sits on (the two
neighbour faces' normals). No reference data other than the solid is read.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field

import numpy as np
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Circle, GeomAbs_Cone, GeomAbs_Cylinder, GeomAbs_Plane, GeomAbs_Sphere, GeomAbs_Torus

RES = 0.05              # mm: size resolution
TANGENT_SOFT = math.radians(5)   # a blend meets its neighbour within this angle (fillet into fillet is near-tangent)
CHAMFER_MAX = 4.0       # mm: a chamfer face is at most this wide


@dataclass
class Blend:
    kind: str                     # fillet | chamfer
    size: float                   # radius (fillet) or leg (chamfer), mm
    angle: float = 90.0           # chamfer angle deg / fillet corner angle deg
    convex: bool = True
    faces: list = field(default_factory=list)     # build123d Faces
    corners: list = field(default_factory=list)   # per face: (centre xyz, neighbour normal a, neighbour normal b)

    @property
    def n_faces(self):
        return len(self.faces)

    def summary(self):
        c = np.array([k[0] for k in self.corners])
        return dict(kind=self.kind, size=self.size, angle=round(self.angle, 1), convex=self.convex, faces=self.n_faces,
                    lo=np.round(c.min(0), 2).tolist(), hi=np.round(c.max(0), 2).tolist())


def _snap(v):
    return round(round(v / RES) * RES, 3)


def _edge_faces(solid):
    """{edge hash: [faces]} adjacency of a solid."""
    m = {}
    for f in solid.faces():
        for e in f.edges():
            L = m.setdefault(hash(e), [])
            if not any(f.is_same(g) for g in L):
                L.append(f)
    return m


def neighbours(solid, face, emap):
    """[(edge, other face)] across each edge of `face`."""
    return [(e, g) for e in face.edges() for g in emap.get(hash(e), []) if not g.is_same(face)]


def _edge_angle(e, fa, fb):
    """Angle (rad) between the two faces' normals at the edge midpoint (0 = tangent)."""
    p = e.position_at(0.5)
    na, nb = np.array(tuple(fa.normal_at(p))), np.array(tuple(fb.normal_at(p)))
    return math.acos(max(-1.0, min(1.0, float(na @ nb))))


def _surface(face):
    ad = BRepAdaptor_Surface(face.wrapped)
    return ad, ad.GetType()


def _centre_side(ad, t, p, n):
    """True when the centre of curvature lies behind the outward normal (a convex round)."""
    if t == GeomAbs_Sphere:
        c = ad.Sphere().Location(); c = np.array([c.X(), c.Y(), c.Z()])
    else:
        ax = ad.Cylinder().Axis() if t == GeomAbs_Cylinder else ad.Torus().Axis()
        o, d = ax.Location(), ax.Direction()
        o, d = np.array([o.X(), o.Y(), o.Z()]), np.array([d.X(), d.Y(), d.Z()])
        c = o + d * ((p - o) @ d)
        if t == GeomAbs_Torus:
            w = p - c
            c = c + w / np.linalg.norm(w) * ad.Torus().MajorRadius()
    return float((p - c) @ n) > 0


def _same_surface(a, b):
    """Two faces on one cylinder (a split round), not a blend and its neighbour."""
    sa, sb = BRepAdaptor_Surface(a.wrapped), BRepAdaptor_Surface(b.wrapped)
    if sa.GetType() != sb.GetType() or sa.GetType() != GeomAbs_Cylinder:
        return False
    ca, cb = sa.Cylinder(), sb.Cylinder()
    return abs(ca.Radius() - cb.Radius()) < 1e-6 and ca.Axis().IsCoaxial(cb.Axis(), 1e-6, 1e-6)


def _opposite_pairs(face, nb):
    """Pairs of neighbours across roughly parallel edges of a planar face (the two sides of a bevel strip)."""
    out = []
    for i, j in [(i, j) for i in range(len(nb)) for j in range(i + 1, len(nb))]:
        (ea, fa), (eb, fb) = nb[i], nb[j]
        if fa.is_same(fb) or str(ea.geom_type)[-4:] != "LINE" or str(eb.geom_type)[-4:] != "LINE":
            continue
        ta, tb = np.array(tuple(ea.tangent_at(0.5))), np.array(tuple(eb.tangent_at(0.5)))
        if abs(ta @ tb) > 1 - 1e-6:
            out.append((nb[i], nb[j]))
    return out


def classify_face(solid, face, emap):
    """('fillet', r, convex) / ('chamfer', leg, angle) / None for one face."""
    ad, t = _surface(face)
    nb = neighbours(solid, face, emap)
    if len(nb) < 2:
        return None
    if t in (GeomAbs_Cylinder, GeomAbs_Torus, GeomAbs_Sphere):
        r = ad.Cylinder().Radius() if t == GeomAbs_Cylinder else (ad.Torus().MinorRadius() if t == GeomAbs_Torus else ad.Sphere().Radius())
        # a round boss / hole meets its caps at 90 deg; a blend runs into at least one other face tangentially
        tang = [x for x in sorted(nb, key=lambda x: -x[0].length)
                if _edge_angle(x[0], face, x[1]) < TANGENT_SOFT and not _same_surface(face, x[1])]
        if not tang:
            return None
        p = np.array(tuple(face.center()))
        n = np.array(tuple(face.normal_at(face.center())))
        other = tang[1][1] if len(tang) > 1 else tang[0][1]
        return ("fillet", _snap(r), _centre_side(ad, t, p, n), tang[0][1], other)
    if t == GeomAbs_Cone:
        if abs(abs(math.degrees(ad.Cone().SemiAngle())) - 45) > 0.5:
            return None
        rs = [BRepAdaptor_Curve(e.wrapped).Circle().Radius() for e, _g in nb if BRepAdaptor_Curve(e.wrapped).GetType() == GeomAbs_Circle]
        lines = [e.length for e, _g in nb if str(e.geom_type)[-4:] == "LINE"]
        leg = max(rs) - min(rs) if len(rs) >= 2 else (max(lines) * math.sqrt(0.5) if lines else 0.0)   # 45 deg: radial = axial leg
        if leg < 1e-3 or leg > CHAMFER_MAX:
            return None
        return ("chamfer", _snap(leg), 45.0, nb[0][1], nb[-1][1])
    if t == GeomAbs_Plane:
        best = None
        for (ea, fa), (eb, fb) in _opposite_pairs(face, nb):
            ang = (_edge_angle(ea, face, fa), _edge_angle(eb, face, fb))
            if min(ang) < math.radians(10) or max(ang) > math.radians(80):
                continue
            pa = np.array(tuple(ea.position_at(0.5)))
            w = min(np.linalg.norm(pa - np.array(tuple(eb.position_at(u)))) for u in np.linspace(0, 1, 41))
            if 1e-3 < w <= CHAMFER_MAX and (best is None or w < best[0]):
                best = (w, ang, fa, fb)
        if best is None:
            return None
        w, ang, fa, fb = best
        s_ = math.sin(ang[0] + ang[1])
        leg = min(w * math.sin(ang[1]) / s_, w * math.sin(ang[0]) / s_)   # removed corner triangle: legs along each neighbour
        return ("chamfer", _snap(leg), math.degrees(ang[0]), fa, fb)
    return None


def find(solid):
    """[Blend] chains of a build123d Solid."""
    emap = _edge_faces(solid)
    faces = solid.faces()
    info = {}
    for i, f in enumerate(faces):
        try:
            c = classify_face(solid, f, emap)
        except Exception:
            c = None
        if c is not None:
            info[i] = c
    idx = {hash(f): i for i, f in enumerate(faces)}
    parent = {i: i for i in info}

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in info:
        for _e, g in neighbours(solid, faces[i], emap):
            j = idx.get(hash(g))
            if j is not None and j in info and info[j][:2] == info[i][:2]:
                parent[root(i)] = root(j)
    groups = {}
    for i in info:
        groups.setdefault(root(i), []).append(i)
    out = []
    for ids in groups.values():
        k, size, extra, fa, fb = info[ids[0]]
        b = Blend(k, size, angle=extra if k == "chamfer" else 90.0, convex=extra if k == "fillet" else True)
        for i in ids:
            f = faces[i]
            _, _, _, na, nb = info[i]
            p = f.center()
            b.faces.append(f)
            b.corners.append((np.array(tuple(p)), _safe_normal(na), _safe_normal(nb)))
        out.append(b)
    return sorted(out, key=lambda b: (b.kind, -b.size))


def _safe_normal(f):
    try:
        return np.round(np.array(tuple(f.normal_at(f.center()))), 4)
    except Exception:
        return None


def load_step_solid(path, index):
    from build123d import import_step
    return import_step(str(path)).solids()[int(index)]


if __name__ == "__main__":
    s = load_step_solid(sys.argv[1], sys.argv[2])
    for b in find(s):
        print(b.summary())
