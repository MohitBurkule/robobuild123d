"""Shared 2D-sketch helpers of printed and cut plates (mounts, spider, discs, spacers): build123d sketches in
each part's own frame, corner selection for 2D fillets, and the ring-sector window every spacer uses."""
import math

import build123d as bd

TURN_TOL_DEG = 1.0   # a boundary turn smaller than this is a tangent join (no corner to fillet)
EPS = 1e-6           # vertex coincidence (mm)


def _turn(face, v):
    """Signed turn (deg) of the outer boundary of `face` at vertex v, positive = convex (boundary turns left on a CCW loop)."""
    w = face.outer_wire()
    es = w.order_edges() if hasattr(w, "order_edges") else w.edges()
    pts = [e.position_at(0) for e in es]
    area = sum(p.X * q.Y - q.X * p.Y for p, q in zip(pts, pts[1:] + pts[:1]))
    for i, e in enumerate(es):
        if (e.position_at(0) - bd.Vector(v)).length < EPS:
            prev = es[i - 1]
            t_in = prev.tangent_at(1) if (prev.position_at(1) - bd.Vector(v)).length < EPS else -prev.tangent_at(0)
            t_out = e.tangent_at(0)
            ang = math.degrees(math.atan2(t_in.cross(t_out).Z, t_in.dot(t_out)))
            return ang if area > 0 else -ang
    return 0.0


def corners(face, convex=True):
    """Outer-boundary vertices of a sketch face (on Plane.XY) where it turns convex / concave (tangent joins skipped)."""
    out = []
    for v in face.outer_wire().vertices():
        a = _turn(face, v)
        if abs(a) > TURN_TOL_DEG and (a > 0) == convex:
            out.append(v)
    return out


def round_corners(face, r_out=0.0, r_in=0.0, keep=()):
    """2D fillets of a sketch face: convex corners r_out, concave corners r_in (the CAD 'sketch fillet' on every corner),
    except the corners at the points `keep` (left sharp)."""
    if not isinstance(face, bd.Face):
        fs = face.clean().faces()
        assert len(fs) == 1, f"round_corners: the sketch is {len(fs)} faces (a reversed loop does not fuse)"
        face = fs[0]
    if r_in:
        face = face.fillet_2d(r_in, _free(corners(face, convex=False), keep))
    if r_out:
        face = face.fillet_2d(r_out, _free(corners(face, convex=True), keep))
    return face


def _free(vs, keep):
    return [v for v in vs if all((bd.Vector(v) - bd.Vector(k)).length > EPS for k in keep)]


def ring_window(r_in, r_out, half_deg, round_out, round_in=None):
    """Ring-sector window on +X (Plane.XY): r_in..r_out, half_deg either side, outer corners round_out, inner round_in."""
    a = math.radians(half_deg)
    P = lambda r, s: bd.Vector(r * math.cos(s * a), r * math.sin(s * a))   # noqa: E731
    w = bd.Wire([bd.Edge.make_three_point_arc(P(r_out, -1), bd.Vector(r_out, 0), P(r_out, 1)), bd.Edge.make_line(P(r_out, 1), P(r_in, 1)),
                 bd.Edge.make_three_point_arc(P(r_in, 1), bd.Vector(r_in, 0), P(r_in, -1)), bd.Edge.make_line(P(r_in, -1), P(r_out, -1))])
    f = bd.Face(w)
    mid = (r_in + r_out) / 2
    f = f.fillet_2d(round_out, [v for v in f.vertices() if math.hypot(v.X, v.Y) > mid])
    return f.fillet_2d(round_out if round_in is None else round_in, [v for v in f.vertices() if math.hypot(v.X, v.Y) < r_in + EPS])


def polar(shape, n, phase=0.0):
    """Copies of a sketch shape turned about the origin: a polar pattern of n, the first at `phase` deg."""
    return [bd.Rot(0, 0, phase + 360.0 * k / n) * shape for k in range(n)]


def holes(r_hole, r_pcd, n, phase=0.0):
    """Bolt-circle hole set: n circles r_hole on the pitch radius r_pcd (PolarLocations)."""
    return [loc * bd.Circle(r_hole) for loc in bd.PolarLocations(r_pcd, n, start_angle=phase)]


def placed(shape, origin):
    """A part modelled in its own frame, placed at its frame origin (the joint rig's frame, see assembly_rig)."""
    return shape.moved(bd.Location(tuple(origin)))
