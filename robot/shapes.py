"""JSON shape trees to build123d solids (OpenCascade B-rep), plus Python model files.

Shape types (all centred on their own origin, mm, degrees):
  box {size}, cylinder {radius, height} (axis z), sphere {radius}, prism {points [[x,y]..], height} (z, centred),
  tube {points [[x,y,z]..], radius}, union {items}, intersect {items}, subtract {base, cut [..]},
  place {shape, at, rot}, offset {shape, d}            -- same as the Rust crate
  revolve {profile [[r,z]..], angle}                   -- profile in the XZ half plane, revolved about Z
  spline_prism {points [[x,y]..], height}              -- closed periodic B-spline outline extruded along z (centred)
  loft {sections [{points [[x,y]..], z, spline}], ruled}  -- skin through planar sections (B-spline surfaces)
  fillet {shape, radius}, chamfer {shape, length}      -- round / bevel every edge of a child
  mirror {shape, axis "x"|"y"|"z"}                     -- reflect across the plane normal to that axis
  model {file, params}                                 -- python file next to the spec; `build(**params)` returns a build123d solid
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

from . import xform

MAX_DEPTH = 24
MAX_NODES = 4000


class ShapeError(ValueError):
    pass


def validate(s, depth=0, n=None) -> None:
    n = n if n is not None else [0]
    n[0] += 1
    if depth > MAX_DEPTH:
        raise ShapeError(f"shape nesting deeper than {MAX_DEPTH}")
    if n[0] > MAX_NODES:
        raise ShapeError(f"shape has more than {MAX_NODES} nodes")
    if not isinstance(s, dict) or "type" not in s:
        raise ShapeError("shape must be an object with a `type`")
    t = s["type"]

    def pos(name, v):
        try:
            ok = math.isfinite(float(v)) and float(v) > 0
        except (TypeError, ValueError):
            ok = False
        if not ok:
            raise ShapeError(f"{name} must be a positive finite number, got {v}")

    def pts(name, p, k, lo, hi):
        if not isinstance(p, list) or not (lo <= len(p) <= hi):
            raise ShapeError(f"{name} needs {lo} to {hi} points")
        for q in p:
            if not isinstance(q, (list, tuple)) or len(q) < k or not all(math.isfinite(float(x)) for x in q[:k]):
                raise ShapeError(f"{name} point must be {k} finite numbers")

    if t == "box":
        size = s.get("size") or []
        if len(size) != 3:
            raise ShapeError("box size needs 3 numbers")
        for v in size:
            pos("box size", v)
    elif t == "cylinder":
        pos("cylinder radius", s.get("radius"))
        pos("cylinder height", s.get("height"))
    elif t == "sphere":
        pos("sphere radius", s.get("radius"))
    elif t == "tube":
        pos("tube radius", s.get("radius"))
        pts("tube", s.get("points"), 3, 1, 4000)
    elif t == "ring":
        pos("ring radius", s.get("radius"))
        if not s.get("path"):
            raise ShapeError("ring needs a closed `path` of line/arc segments")
    elif t in ("prism", "spline_prism"):
        pos(f"{t} height", s.get("height"))
        pts(t, s.get("points"), 2, 3, 2000)
    elif t == "revolve":
        pts("revolve profile", s.get("profile"), 2, 3, 2000)
        if any(float(q[0]) < -1e-9 for q in s["profile"]):
            raise ShapeError("revolve profile radius must be >= 0")
    elif t == "loft":
        secs = s.get("sections") or []
        if len(secs) < 2:
            raise ShapeError("loft needs at least 2 sections")
        for sec in secs:
            pts("loft section", sec.get("points"), 2, 3, 2000)
    elif t in ("union", "intersect"):
        items = s.get("items") or []
        if not items:
            raise ShapeError("union/intersect needs at least one item")
        for i in items:
            validate(i, depth + 1, n)
    elif t == "subtract":
        validate(s.get("base"), depth + 1, n)
        for c in s.get("cut") or []:
            validate(c, depth + 1, n)
    elif t == "place":
        if not all(math.isfinite(float(v)) for v in list(s.get("at") or [0, 0, 0]) + list(s.get("rot") or [0, 0, 0])):
            raise ShapeError("place has a non-finite value")
        validate(s.get("shape"), depth + 1, n)
    elif t == "offset":
        d = float(s.get("d", 0))
        if not math.isfinite(d) or abs(d) > 50:
            raise ShapeError("offset must be finite and within +-50 mm")
        validate(s.get("shape"), depth + 1, n)
    elif t in ("fillet", "chamfer"):
        pos(t, s.get("radius", s.get("length")))
        validate(s.get("shape"), depth + 1, n)
    elif t == "mirror":
        if s.get("axis", "x") not in ("x", "y", "z"):
            raise ShapeError("mirror axis must be x, y or z")
        validate(s.get("shape"), depth + 1, n)
    elif t == "model":
        if not s.get("file"):
            raise ShapeError("model needs `file`")
    else:
        raise ShapeError(f"unknown shape type `{t}`")


# ---------------------------------------------------------------------------- build123d conversion


def _b():
    import build123d  # noqa: PLC0415 - heavy import, only when geometry is really built

    return build123d


def location(M):
    from OCP.gp import gp_Trsf

    b = _b()
    t = gp_Trsf()
    t.SetValues(*[float(M[i, j]) for i in range(3) for j in range(4)])
    return b.Location(t)


def place(solid, M):
    return solid.moved(location(M))


def _solid(x):
    """Booleans may return a Compound or ShapeList; keep it as one shape."""
    b = _b()
    if isinstance(x, (list, tuple)) or x.__class__.__name__ == "ShapeList":
        items = list(x)
        return items[0] if len(items) == 1 else b.Compound(items)
    return x


def _polygon_face(points, close=True):
    b = _b()
    vs = [b.Vector(float(p[0]), float(p[1]), float(p[2]) if len(p) > 2 else 0.0) for p in points]
    # Drop repeated closing point.
    if len(vs) > 3 and (vs[0] - vs[-1]).length < 1e-9:
        vs = vs[:-1]
    if _area2(vs, close) < 0:
        vs = vs[::-1]
    w = b.Wire.make_polygon(vs, close=True)
    return b.Face(w)


def self_intersecting(points) -> bool:
    from shapely.geometry import Polygon

    try:
        return not Polygon([(float(p[0]), float(p[1])) for p in points]).is_valid
    except Exception:  # noqa: BLE001
        return True


def _valid_faces(points, xz=False):
    """Faces of a 2-D outline; a self-intersecting outline is repaired with even-odd parity (like the Rust SDF)."""
    from shapely.geometry import Polygon
    from shapely.validation import make_valid

    b = _b()
    poly = Polygon([(float(p[0]), float(p[1])) for p in points])
    geoms = [poly] if poly.is_valid else [g for g in getattr(make_valid(poly), "geoms", [make_valid(poly)]) if g.geom_type == "Polygon"]
    if not poly.is_valid:
        g = make_valid(poly)
        geoms = [x for x in (g.geoms if hasattr(g, "geoms") else [g]) if x.geom_type == "Polygon" and x.area > 1e-9]

    def wire(coords):
        cs = list(coords)[:-1]
        vs = [b.Vector(x, 0.0, y) if xz else b.Vector(x, y, 0.0) for x, y in cs]
        return b.Wire.make_polygon(vs, close=True)

    faces = []
    for g in geoms:
        g = g.buffer(0) if not g.is_valid else g
        f = b.Face(wire(g.exterior.coords), [wire(i.coords) for i in g.interiors])
        faces.append(f)
    if not faces:
        raise ShapeError("outline has no area")
    return faces


def _area2(vs, xy=True):
    # Signed doubled area in XY (or XZ for revolve profiles, where the face must face -Y to sweep the right way).
    if xy:
        return sum(a.X * b.Y - b.X * a.Y for a, b in zip(vs, vs[1:] + vs[:1]))
    return sum(a.X * b.Z - b.X * a.Z for a, b in zip(vs, vs[1:] + vs[:1]))


def _spline_face(points, z=0.0):
    b = _b()
    vs = [b.Vector(float(p[0]), float(p[1]), z) for p in points]
    if len(vs) > 3 and (vs[0] - vs[-1]).length < 1e-9:
        vs = vs[:-1]
    if _area2(vs) < 0:
        vs = vs[::-1]
    e = b.Edge.make_spline(vs, periodic=True)
    return b.Face(b.Wire([e]))


def to_solid(s, base_dir: Path | None = None):
    b = _b()
    t = s["type"]
    if t == "box":
        x, y, z = (float(v) for v in s["size"])
        return b.Solid.make_box(x, y, z).moved(b.Location((-x / 2, -y / 2, -z / 2)))
    if t == "cylinder":
        r, h = float(s["radius"]), float(s["height"])
        return b.Solid.make_cylinder(r, h).moved(b.Location((0, 0, -h / 2)))
    if t == "sphere":
        return b.Solid.make_sphere(float(s["radius"]))
    if t == "prism":
        h = float(s["height"])
        sols = [b.Solid.extrude(f, b.Vector(0, 0, h)).moved(b.Location((0, 0, -h / 2))) for f in _valid_faces(s["points"])]
        return sols[0] if len(sols) == 1 else _solid(sols[0].fuse(*sols[1:]).clean())
    if t == "spline_prism":
        h = float(s["height"])
        return b.Solid.extrude(_spline_face(s["points"]), b.Vector(0, 0, h)).moved(b.Location((0, 0, -h / 2)))
    if t == "revolve":
        ang = float(s.get("angle", 360.0))
        sols = [b.Solid.revolve(f, ang, b.Axis.Z) for f in _valid_faces(s["profile"], xz=True)]
        return sols[0] if len(sols) == 1 else _solid(sols[0].fuse(*sols[1:]).clean())
    if t == "loft":
        faces = []
        for sec in s["sections"]:
            z = float(sec.get("z", 0.0))
            if sec.get("spline", True):
                faces.append(_spline_face(sec["points"], z))
            else:
                faces.append(_polygon_face([[p[0], p[1], z] for p in sec["points"]]))
        return b.Solid.make_loft([f.outer_wire() for f in faces], ruled=bool(s.get("ruled", False)))
    if t == "ring":
        # round section swept along a closed planar path (XY plane) of ["line", p, q] / ["arc", p, mid, q] segments: an O-ring / belt loop
        edges = []
        for seg in s["path"]:
            pts = [b.Vector(float(v[0]), float(v[1]), 0.0) for v in seg[1:]]
            edges.append(b.Edge.make_line(*pts) if seg[0] == "line" else b.Edge.make_three_point_arc(*pts))
        path = b.Wire(edges)
        t0 = path.tangent_at(0)
        start = path.position_at(0)
        prof = b.Plane(origin=start, z_dir=t0)
        circ = b.Wire(b.Edge.make_circle(float(s["radius"]), prof))
        return b.Solid.sweep(b.Face(circ), path)
    if t == "tube":
        r = float(s["radius"])
        pts = [np.asarray(p, float) for p in s["points"]]
        pieces = [b.Solid.make_sphere(r).moved(b.Location(tuple(p))) for p in pts]
        for p, q in zip(pts, pts[1:]):
            d = q - p
            L = float(np.linalg.norm(d))
            if L < 1e-6:
                continue
            c = b.Solid.make_cylinder(r, L)
            pieces.append(place(c, xform.make(xform.align_z_to(d), p)))
        if len(pieces) == 1:
            return pieces[0]
        return _solid(pieces[0].fuse(*pieces[1:]).clean())
    if t == "union":
        items = [to_solid(i, base_dir) for i in s["items"]]
        if len(items) == 1:
            return items[0]
        return _solid(items[0].fuse(*items[1:]).clean())
    if t == "intersect":
        items = [to_solid(i, base_dir) for i in s["items"]]
        out = items[0]
        for i in items[1:]:
            out = _solid(out.intersect(i))
        return out
    if t == "subtract":
        base = to_solid(s["base"], base_dir)
        cuts = [to_solid(c, base_dir) for c in s.get("cut") or []]
        if not cuts:
            return base
        return _solid(base.cut(*cuts).clean())
    if t == "place":
        return place(to_solid(s["shape"], base_dir), xform.pose(s.get("at") or [0, 0, 0], s.get("rot") or [0, 0, 0]))
    if t == "offset":
        return _offset(to_solid(s["shape"], base_dir), float(s["d"]))
    if t == "fillet":
        child = to_solid(s["shape"], base_dir)
        return child.fillet(float(s["radius"]), child.edges())
    if t == "chamfer":
        child = to_solid(s["shape"], base_dir)
        return child.chamfer(float(s.get("length", s.get("radius"))), None, child.edges())
    if t == "mirror":
        child = to_solid(s["shape"], base_dir)
        plane = {"x": b.Plane.YZ, "y": b.Plane.XZ, "z": b.Plane.XY}[s.get("axis", "x")]
        return child.mirror(plane)
    if t == "model":
        return _model(s, base_dir)
    raise ShapeError(f"unknown shape type `{t}`")


def _offset(solid, d):
    from OCP.BRepOffset import BRepOffset_Skin
    from OCP.BRepOffsetAPI import BRepOffsetAPI_MakeOffsetShape
    from OCP.GeomAbs import GeomAbs_Arc

    b = _b()
    mk = BRepOffsetAPI_MakeOffsetShape()
    mk.PerformByJoin(solid.wrapped, d, 1e-4, BRepOffset_Skin, False, False, GeomAbs_Arc)
    mk.Build()
    if not mk.IsDone():
        raise ShapeError("offset failed")
    return b.Solid(mk.Shape()) if mk.Shape().ShapeType().name == "TopAbs_SOLID" else b.Compound(mk.Shape())


def _model(s, base_dir):
    path = Path(s["file"])
    if not path.is_absolute():
        path = (base_dir or Path.cwd()) / path
    if not path.is_file():
        raise ShapeError(f"model file {path} not found")
    spec = importlib.util.spec_from_file_location(f"robot_model_{hashlib.sha1(str(path).encode()).hexdigest()[:8]}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "build"):
        raise ShapeError(f"{path} has no build(**params) function")
    out = mod.build(**(s.get("params") or {}))
    if hasattr(out, "part"):  # BuildPart context
        out = out.part
    return _solid(out)


def model_files(s, base_dir: Path | None) -> list[Path]:
    """Python files a shape depends on (for the cache key)."""
    out = []
    if isinstance(s, dict):
        if s.get("type") == "model" and s.get("file"):
            p = Path(s["file"])
            out.append(p if p.is_absolute() else (base_dir or Path.cwd()) / p)
        for v in s.values():
            out += model_files(v, base_dir)
    elif isinstance(s, list):
        for v in s:
            out += model_files(v, base_dir)
    return out


def shape_key(s, base_dir: Path | None, extra: str = "") -> str:
    h = hashlib.sha256(json.dumps(s, sort_keys=True).encode())
    from . import cache

    for f in model_files(s, base_dir):
        # the model file and everything it imports or reads (helpers, params modules, robot.cad.*), by content only
        h.update(cache.model_hash(f).encode())
    h.update(extra.encode())
    return h.hexdigest()[:24]
