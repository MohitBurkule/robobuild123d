"""Smooth parts from measured stations: loft (or sweep) exact B-spline sections, then fillet; plus a stair-step metric.

WHY: shells built by stacking extrusions or unioning boxes at measured heights show stair steps (a 90 deg crease
every station) that the reference does not have, fail silhouette/section matching and print badly. Lofting smooth
sections through the stations gives one continuous surface; `smoothness()` proves it.

  Station(at, profile, axis="z")            one section: `at` = position along the axis (or a 3D point with `path`)
  profile kinds (dicts, so they live in params JSON):
      {"type": "bspline", "ctrl": [[x, y], ...], "closed": true}       (from robot.cad.fit / measure-ref --fit)
      {"type": "ellipse", "rx": 10, "ry": 6}       {"type": "rounded_rect", "w": 20, "h": 10, "r": 3}
      {"type": "spline", "points": [[x, y], ...]}  (interpolating, periodic)
      optional "center": [cx, cy], "rot_deg": a
  loft_stations(stations, ruled=False)      -> build123d Solid
  sweep_profile(profile, path_points)       -> Solid swept along an interpolating 3D spline
  fillet_all(solid, r)                      -> filleted solid (falls back to the input if OCC refuses; returns flag)
  smoothness(mesh_or_solid, axis, n=80)     -> {"max_crease_deg", "profile_curvature_max", "steps"}
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

AX = {"x": 0, "y": 1, "z": 2}


@dataclass
class Station:
    at: float
    profile: dict
    axis: str = "z"


def _plane(at, axis):
    import build123d as bd

    if axis == "z":
        return bd.Plane(origin=(0, 0, at), x_dir=(1, 0, 0), z_dir=(0, 0, 1))
    if axis == "x":
        return bd.Plane(origin=(at, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    return bd.Plane(origin=(0, at, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))


def bspline_wire(ctrl, closed=True, plane=None):
    """Exact uniform cubic B-spline (periodic or clamped) with these 2D control points, on `plane`."""
    import build123d as bd
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
    from OCP.Geom import Geom_BSplineCurve
    try:
        from OCP.TColgp import TColgp_Array1OfPnt
        from OCP.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal
    except ImportError:  # newer OCP exposes NCollection arrays under these names
        from OCP.collections import Array1_double as TColStd_Array1OfReal  # noqa: N811
        from OCP.collections import Array1_gp_Pnt as TColgp_Array1OfPnt  # noqa: N811
        from OCP.collections import Array1_int as TColStd_Array1OfInteger  # noqa: N811

    plane = plane or bd.Plane.XY
    C = np.asarray(ctrl, float)
    n = len(C)
    poles = TColgp_Array1OfPnt(1, n)
    for i, (x, y) in enumerate(C):
        p = plane.from_local_coords((float(x), float(y), 0.0))
        poles.SetValue(i + 1, bd.Vector(p).to_pnt())
    if closed:
        nk = n + 1
        knots, mults = TColStd_Array1OfReal(1, nk), TColStd_Array1OfInteger(1, nk)
        for i in range(nk):
            knots.SetValue(i + 1, float(i))
            mults.SetValue(i + 1, 1)
        curve = Geom_BSplineCurve(poles, knots, mults, 3, True)
    else:
        inner = max(n - 4, 0)
        nk = inner + 2
        knots, mults = TColStd_Array1OfReal(1, nk), TColStd_Array1OfInteger(1, nk)
        for i in range(nk):
            knots.SetValue(i + 1, i / (inner + 1))
            mults.SetValue(i + 1, 4 if i in (0, nk - 1) else 1)
        curve = Geom_BSplineCurve(poles, knots, mults, 3, False)
    edge = bd.Edge(BRepBuilderAPI_MakeEdge(curve).Edge())
    return bd.Wire([edge])


def profile_wire(profile: dict, plane=None):
    import build123d as bd

    plane = plane or bd.Plane.XY
    t = profile.get("type")
    cx, cy = profile.get("center", (0.0, 0.0))
    a = math.radians(profile.get("rot_deg", 0.0))
    ca, sa = math.cos(a), math.sin(a)
    tf = lambda pts: [(cx + ca * x - sa * y, cy + sa * x + ca * y) for x, y in pts]  # noqa: E731
    if t == "bspline":
        return bspline_wire(tf(profile["ctrl"]), profile.get("closed", True), plane)
    if t == "spline":
        pts = [plane.from_local_coords((x, y, 0)) for x, y in tf(profile["points"])]
        return bd.Wire([bd.Spline(*pts, periodic=True)])
    if t == "ellipse":
        # an 8-pole periodic fit (error < 0.01 mm) keeps every profile the same curve type, which lofts cleanly
        from .fit import fit_bspline

        th = np.linspace(0, 2 * math.pi, 200, endpoint=False)
        dense = tf(np.column_stack([profile["rx"] * np.cos(th), profile["ry"] * np.sin(th)]))
        return bspline_wire(fit_bspline(dense, True, 8, 0.005)["ctrl"], True, plane)
    if t == "rounded_rect":
        w, h, r = profile["w"], profile["h"], profile.get("r", 0.0)
        sk = bd.RectangleRounded(w, h, r) if r > 0 else bd.Rectangle(w, h)
        face = (bd.Pos(cx, cy) * bd.Rot(0, 0, math.degrees(a)) * sk).faces()[0]
        return _on_plane(face.outer_wire(), plane)
    raise ValueError(f"unknown profile type `{t}`")


def _on_plane(wire, plane):
    import build123d as bd

    return bd.Location(plane) * wire


def loft_stations(stations, ruled=False):
    """Loft closed sections at the stations (sorted along their axis) into one solid."""
    import build123d as bd

    st = sorted(stations, key=lambda s: s.at)
    faces = [bd.Face(profile_wire(s.profile, _plane(s.at, s.axis))) for s in st]
    return bd.loft(faces, ruled=ruled)


def sweep_profile(profile, path_points, transition="right"):
    """Sweep one closed profile along an interpolating spline through 3D path points (profile plane = path start
    normal)."""
    import build123d as bd

    path = bd.Spline(*[tuple(map(float, p)) for p in path_points])
    pl = bd.Plane(origin=path @ 0, z_dir=path % 0)
    face = bd.Face(profile_wire(profile, pl))
    return bd.sweep(face, path=path, transition=bd.Transition.RIGHT if transition == "right" else bd.Transition.ROUND)


def fillet_all(solid, r, edges=None):
    """Fillet the given edges (default: the end-cap edges of a loft, i.e. every edge) with radius r.
    Returns (solid, ok). OCC fails on radii larger than the local curvature allows; the input is then returned."""
    import build123d as bd

    try:
        out = bd.fillet(edges if edges is not None else solid.edges(), r)
        if out.is_valid:
            return out, True
    except Exception:  # noqa: BLE001 - OCC fillet failure is common; report it instead of crashing
        pass
    return solid, False


# ---------------------------------------------------------------- smoothness metric


def _mesh(x):
    import trimesh

    if isinstance(x, trimesh.Trimesh):
        return x
    from ..geom import FINE, tessellate

    V, F = tessellate(x, FINE)
    return trimesh.Trimesh(V, F)


def smoothness(obj, axis="z", n=80, cap_deg=60.0):
    """Stair-step metrics.
      max_crease_deg        largest angle between adjacent faces, end caps skipped (faces near the axis ends whose
                            normal is within `cap_deg` of the axis); a lofted surface stays near the tessellation
                            angle (~6-12 deg), a stacked extrusion has 90 deg creases at every tread
      profile_curvature_max max |d2 r / ds2| (1/mm) of the equivalent radius r = sqrt(area/pi) of n sections along
                            the axis; a step shows up as a spike that grows as 1/h^2
      steps                 count of sections where r jumps by more than 3x the median change (stair treads)
    """
    import trimesh

    m = _mesh(obj)
    ax = AX[axis]
    a = np.zeros(3)
    a[ax] = 1
    lo, hi = m.bounds[0][ax], m.bounds[1][ax]
    zc = m.triangles_center[:, ax]
    # every face except the two end caps (faces on the extreme ends of the axis); a stair tread is interior
    side = ~((np.abs(m.face_normals @ a) > math.cos(math.radians(90 - cap_deg))) & ((zc < lo + 0.3) | (zc > hi - 0.3)))
    adj = m.face_adjacency
    ang = m.face_adjacency_angles
    both = side[adj[:, 0]] & side[adj[:, 1]]
    crease = float(np.degrees(ang[both].max())) if both.any() else 0.0
    hs = np.linspace(lo, hi, n + 2)[1:-1]
    from ..checks.ref_features import section

    r = []
    for hh in hs:
        g = section(m, ax, hh)
        r.append(math.sqrt(g.area / math.pi) if g is not None else 0.0)
    r = np.asarray(r)
    h = hs[1] - hs[0]
    d1 = np.diff(r)
    d2 = np.diff(r, 2) / h ** 2 if len(r) > 2 else np.zeros(1)
    med = float(np.median(np.abs(d1))) if len(d1) else 0.0
    steps = int(np.sum(np.abs(d1) > max(3 * med, 0.05))) if len(d1) else 0
    del trimesh
    return {"max_crease_deg": round(crease, 2), "profile_curvature_max": round(float(np.abs(d2).max()), 4),
            "steps": steps}
