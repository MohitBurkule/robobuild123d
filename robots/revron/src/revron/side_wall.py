"""[fix-C] Revron side-panel wall rebuilt from the RV23 feature tree (Loft1/Loft2, Revolve5/6/7): a handful of analytic faces.

Plan, from the front (nose) to the rear, one wall of constant cross-section family (chassis-side face + battered outer face):
  swing    Revolve5   90 deg about a vertical axis at the nose front: both faces cones (40 deg lean), tangent to the nose plane
  S-bend   Loft1      one ruled patch per face from the swing's end section to the mid wall's front section
  mid wall Loft2      straight, inner face the plane X = SP_X_IN, outer face battered 12 deg; its top rises towards the rear
  bend 1   Revolve6   90 deg about a vertical axis, the wall steps out to the rear wheel
  bend 2   Revolve7   90 deg back to straight
  rear     extrude    straight rear wall
Every junction is a shared planar section, so the fused wall has no step and no tessellation-split organic surface."""
import math
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _quad(b, *pts):
    return b.Face(b.Wire.make_polygon([b.Vector(*p) for p in pts], close=True))


def _trap(b, plane, at, x_in, z_hi, sign):
    """Wall section in a vertical plane: chassis-side face vertical at offset `x_in`, outer face battered from SP_W_FLOOR thick at the
    floor to SP_W_TOP at `z_hi`. plane 'y': section in the plane Y = at (u = X, outer = -sign direction); 'x': plane X = at (u = Y)."""
    z0 = FLOOR_Z
    t = lambda z: SP_W_FLOOR + (SP_W_TOP - SP_W_FLOOR) * (z - z0) / (z_hi - z0)
    pts = [(x_in - sign * t(z0), z0), (x_in, z0), (x_in, z_hi), (x_in - sign * t(z_hi), z_hi)]
    return _quad(b, *[(u, at, v) if plane == "y" else (at, u, v) for u, v in pts])


def _spin(b, face, c, angle, lead=0.0):
    """Revolve `face` (in a vertical plane through the axis) about the vertical axis at plan point c by `angle` deg (CCW from above when
    positive), starting `lead` deg early so the solid overlaps its neighbour."""
    if lead:
        face = face.rotate(b.Axis((c[0], c[1], 0.0), (0, 0, 1)), -math.copysign(lead, angle))
    return b.Solid.revolve(face, abs(angle) + lead, b.Axis((c[0], c[1], 0.0), (0, 0, math.copysign(1.0, angle))))


def _swing_r(k, z):
    """Radius of the swing's chassis-side (k=0) / outer (k=1) cone at height z."""
    fr = SP_FRONT
    return fr["r_in"] + k * fr["w"] - SP_LEAN * (z - FLOOR_Z)


def _hermite(p0, p1, h0, h1, m, u):
    """Cubic Hermite point at u between 3D points p0 -> p1 leaving along h0, arriving along h1 (tangent length m, none in Z)."""
    h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
    return tuple(h00 * p0[k] + h10 * m * h0[k] + h01 * p1[k] + h11 * m * h1[k] for k in range(3))


def _bend(b, a_pts, mid_pts):
    """The S-bend (Loft1): four corner curves from the swing's end section to the mid wall's front section (cubic Hermite, leaving
    along +X and arriving along -Y, i.e. normal to each profile like a guide-less SolidWorks loft), each face a strip of SP_BEND_STEPS
    planar triangle pairs along the curves. The facets turn less than the 6 deg faceting-seam threshold, so the tessellated skin has
    no seam where a freeform surface would (OCC splits a skinned spline near the threshold); the end sections are the neighbours' own."""
    n = SP_BEND_STEPS
    rows = []
    for u in [(1 - math.cos(math.pi * i / n)) / 2 for i in range(n + 1)]:   # stations bunch up at both ends, where the curves turn hardest
        rows.append([_hermite(p0, p1, (1.0, 0.0, 0.0), (0.0, -1.0, 0.0), SP_BEND_TENSION * math.dist(p0[:2], p1[:2]), u)
                     for p0, p1 in zip(a_pts, mid_pts)])
    rows[0], rows[-1] = list(a_pts), list(mid_pts)
    V = lambda q: b.Vector(*q)
    tri = lambda *q: b.Face(b.Wire.make_polygon([V(x) for x in q], close=True))
    faces = [_quad(b, *a_pts), _quad(b, *mid_pts)]
    lerp = lambda p, q, w: tuple(p[k] + (q[k] - p[k]) * w for k in range(3))
    for r0, r1 in zip(rows[:-1], rows[1:]):
        for k in range(4):
            k1 = (k + 1) % 4
            m = SP_BEND_LEVELS if k in (1, 3) else 1          # the tall faces (chassis-side, outer) are cut into levels: less twist per facet
            for j in range(m):
                w0, w1 = j / m, (j + 1) / m
                # the side runs corner k -> k1 (k=1: floor-in -> top-in; k=3: top-out -> floor-out), levels along it
                q = lambda r, w: lerp(r[k], r[k1], w)
                faces += [tri(q(r0, w0), q(r0, w1), q(r1, w1)), tri(q(r0, w0), q(r1, w1), q(r1, w0))]
    return b.Solid(b.Shell(faces))


def sp_wall(b):
    """The whole wall, un-trimmed (the side profile, the top line and the rear round cut it in side._side_body)."""
    s, fr = SP_X_IN, SP_FRONT
    (cx, cy), zt = fr["c"], fr["z_top"]
    y_rear, y_front = SP_MID_Y
    r1, r2 = SP_BEND_R
    c1 = (s - r1, y_rear)                          # bend 1 axis: the chassis-side face is r1 from it
    c2 = (c1[0], c1[1] - r1 - r2)                  # bend 2 axis: tangent continuation, the chassis-side face is r2 from it
    # swing (Revolve5): 90 deg from the nose plane round to the plane X = cx, leading in past the nose plane
    sec = lambda y: [(cx - _swing_r(k, z), y, z) for z, k in ((FLOOR_Z, 1), (FLOOR_Z, 0), (zt, 0), (zt, 1))]
    swing = _spin(b, _quad(b, *sec(cy)), (cx, cy), 90.0, fr["over"])
    # S-bend (Loft1): the swing's end section (plane X = cx) -> the mid wall's front section (plane Y = y_front), swept on
    # SP_BEND_SECTIONS sections that turn the outward normal 90 deg and blend the profile, so the loft never twists
    mid_f = _trap(b, "y", y_front, s, SP_MID_Z_FRONT, 1)
    a_pts = [(cx, cy - _swing_r(k, z), z) for z, k in ((FLOOR_Z, 1), (FLOOR_Z, 0), (zt, 0), (zt, 1))]
    t = lambda z: SP_W_FLOOR + (SP_W_TOP - SP_W_FLOOR) * (z - FLOOR_Z) / (SP_MID_Z_FRONT - FLOOR_Z)
    mid_pts = [(s - t(FLOOR_Z), y_front, FLOOR_Z), (s, y_front, FLOOR_Z), (s, y_front, SP_MID_Z_FRONT), (s - t(SP_MID_Z_FRONT), y_front, SP_MID_Z_FRONT)]
    bend = _bend(b, a_pts, mid_pts)
    # mid wall (Loft2): front section -> rear section (full height)
    mid_r = _trap(b, "y", y_rear, s, SP_Z_TOP, 1)
    mid = b.Solid.make_loft([mid_f.outer_wire(), mid_r.outer_wire()], ruled=True)
    # rear bends (Revolve6, Revolve7) and the straight rear wall
    b1 = _spin(b, mid_r, c1, -90.0)
    b2 = _spin(b, _trap(b, "x", c1[0], c2[1] + r2, SP_Z_TOP, -1), c2, 90.0)
    rear = b.Solid.extrude(_trap(b, "y", c2[1], c2[0] - r2, SP_Z_TOP, 1), b.Vector(0, SP_REAR_Y_END - c2[1], 0))
    return _U(swing, bend, mid, b1, b2, rear)
