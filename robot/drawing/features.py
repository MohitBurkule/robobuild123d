"""[drawing] Feature recognition on the B-rep: holes (full concave cylinders), fillets (partial cylinders, tori) and
45 degree chamfers (narrow planar faces). Every number comes from the surface definitions, never from a table."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

AXES = np.eye(3)


@dataclass
class Cyl:
    face: object
    axis_p: np.ndarray      # point on the axis
    axis_d: np.ndarray      # unit axis direction (sign normalised)
    r: float
    span_deg: float         # angular coverage of this face
    concave: bool
    t0: float               # axial extent along axis_d (projections of the face's vertices / samples)
    t1: float


@dataclass
class Hole:
    centre: np.ndarray      # point on the axis at the hole's upper end (max t)
    axis: np.ndarray
    r: float
    depth: float
    faces: list = field(default_factory=list)

    @property
    def d(self):
        return 2 * self.r


@dataclass
class Fillet:
    kind: str               # "cyl" or "torus"
    r: float
    axis: np.ndarray        # cylinder axis / torus axis
    centre: np.ndarray      # a point of the arc centre (cylinder: mid of axial extent)
    mid: np.ndarray         # a point on the face (where a leader can land)
    span_deg: float
    face: object = None


@dataclass
class Chamfer:
    leg: float              # leg length (width / sqrt 2)
    width: float
    angle_deg: float
    normal: np.ndarray
    centre: np.ndarray
    face: object = None


def _snap_axis(d):
    d = np.asarray(d, float)
    d = d / np.linalg.norm(d)
    i = int(np.argmax(np.abs(d)))
    if d[i] < 0:
        d = -d
    return d


def _face_samples(face, n=5):
    from OCP.BRepTools import BRepTools
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    u0, u1, v0, v1 = BRepTools.UVBounds_s(face.wrapped)
    s = BRepAdaptor_Surface(face.wrapped)
    pts = []
    for a in np.linspace(0, 1, n):
        for b in np.linspace(0, 1, n):
            p = s.Value(u0 + a * (u1 - u0), v0 + b * (v1 - v0))
            pts.append((p.X(), p.Y(), p.Z()))
    return np.array(pts), (u0, u1, v0, v1), s


def cylinders(shape):
    """All cylindrical faces with axis, radius, angular span and concavity."""
    from OCP.GeomAbs import GeomAbs_Cylinder
    out = []
    for f in shape.faces():
        pts, (u0, u1, v0, v1), s = _face_samples(f, 3)
        if s.GetType() != GeomAbs_Cylinder:
            continue
        c = s.Cylinder()
        ax = c.Axis()
        p0 = np.array([ax.Location().X(), ax.Location().Y(), ax.Location().Z()])
        d = _snap_axis([ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z()])
        um, vm = (u0 + u1) / 2, (v0 + v1) / 2
        pm = s.Value(um, vm)
        pm = np.array([pm.X(), pm.Y(), pm.Z()])
        radial = pm - p0 - ((pm - p0) @ d) * d
        from build123d import Vector
        nrm = np.array(tuple(f.normal_at(Vector(*pm))))
        concave = float(nrm @ radial) < 0
        p0 = p0 - (p0 @ d) * d          # foot of the axis from the origin: t is then absolute along d
        ts = pts @ d
        out.append(Cyl(f, p0, d, c.Radius(), math.degrees(u1 - u0), concave, ts.min(), ts.max()))
    return out


def holes(shape, min_span=300.0, max_r=6.0):
    """Concave cylinders grouped by coaxial axis and equal radius whose faces together close the circle."""
    groups = []
    for c in cylinders(shape):
        if not c.concave or c.r > max_r:
            continue
        for g in groups:
            h = g[0]
            off = c.axis_p - h.axis_p
            off = off - (off @ h.axis_d) * h.axis_d
            if abs(c.r - h.r) < 1e-4 and abs(abs(c.axis_d @ h.axis_d) - 1) < 1e-6 and np.linalg.norm(off) < 1e-4:
                g.append(c)
                break
        else:
            groups.append([c])
    res = []
    for g in groups:
        # split a coaxial group into axially separate holes (mirrored holes share one axis line)
        g.sort(key=lambda c: c.t0)
        runs = [[g[0]]]
        for c in g[1:]:
            if c.t0 <= max(x.t1 for x in runs[-1]) + 1e-4:
                runs[-1].append(c)
            else:
                runs.append([c])
        for run in runs:
            if sum(c.span_deg for c in run) < min_span:
                continue
            t0, t1 = min(c.t0 for c in run), max(c.t1 for c in run)
            h = run[0]
            res.append(Hole(h.axis_p + t1 * h.axis_d, h.axis_d, h.r, t1 - t0, [c.face for c in run]))
    return res


def fillets(shape, max_r=10.0, hole_list=None):
    """Partial cylinders (not part of a hole) and toroidal faces: their radius is a fillet / round radius."""
    from OCP.GeomAbs import GeomAbs_Torus
    hole_faces = set()
    for h in hole_list or []:
        for f in h.faces:
            hole_faces.add(hash(f))
    out = []
    for c in cylinders(shape):
        if c.r > max_r or c.span_deg >= 300 or hash(c.face) in hole_faces:
            continue
        pts, _, _ = _face_samples(c.face, 3)
        mid = pts[len(pts) // 2]
        cen = c.axis_p + ((mid - c.axis_p) @ c.axis_d) * c.axis_d
        out.append(Fillet("cyl", c.r, c.axis_d, cen, mid, c.span_deg, c.face))
    for f in shape.faces():
        pts, (u0, u1, v0, v1), s = _face_samples(f, 3)
        if s.GetType() != GeomAbs_Torus:
            continue
        t = s.Torus()
        ax = t.Axis()
        d = _snap_axis([ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z()])
        cen = np.array([ax.Location().X(), ax.Location().Y(), ax.Location().Z()])
        if t.MinorRadius() <= max_r:
            out.append(Fillet("torus", t.MinorRadius(), d, cen, pts[len(pts) // 2], math.degrees(v1 - v0), f))
    return out


def chamfers(shape, max_width=4.0, angle_tol=1.0):
    """Planar faces at 45 deg to two principal axes and narrow (<= max_width): a chamfer of leg = width / sqrt 2."""
    from build123d import GeomType
    out = []
    for f in shape.faces():
        if f.geom_type != GeomType.PLANE:
            continue
        nrm = np.array(tuple(f.normal_at()))
        a = np.abs(nrm)
        srt = np.sort(a)
        if srt[0] > 1e-6:
            continue
        ang = math.degrees(math.atan2(srt[1], srt[2]))
        if abs(ang - 45) > angle_tol:
            continue
        # width: extent across the face perpendicular to its longest straight edge
        edges = [e for e in f.edges() if e.geom_type == GeomType.LINE]
        if not edges:
            continue
        lng = max(edges, key=lambda e: e.length)
        t = np.array(tuple(lng.tangent_at(0)))
        across = np.cross(nrm, t)
        vs = np.array([tuple(v) for v in f.vertices()])
        w = float(np.ptp(vs @ across))
        if w < 0.3 or w > max_width or lng.length < 2 * w:
            continue
        out.append(Chamfer(w / math.sqrt(2), w, 45.0 if abs(ang - 45) < angle_tol else ang, nrm,
                           np.array(tuple(f.center())), f))
    return out


def group_by(values, key, tol=0.005):
    """Group objects by a float key within tol, sorted by key; returns [(key, [objs])]."""
    out = []
    for o in sorted(values, key=key):
        k = key(o)
        if out and abs(out[-1][0] - k) <= tol:
            out[-1][1].append(o)
        else:
            out.append((k, [o]))
    return out
