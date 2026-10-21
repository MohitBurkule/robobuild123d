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
from .params import (
    BEZIER_DEG, FLOOR_Z, SP_BEND_R, SP_BEND_TENSION, SP_FRONT, SP_LEAN, SP_MID_Y, SP_MID_Z_FRONT,
    SP_NOSE_RUN, SP_NOSE_Z, SP_REAR_Y_END, SP_W_FLOOR, SP_W_TOP, SP_X_IN, SP_Z_TOP)
from .common import _U


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


def _bend(b, a_pts, mid_pts):
    """The S-bend (Loft1): the swing's end section -> the mid wall's front section. Its four corner curves leave along +X and arrive
    along -Y (normal to each profile, like a guide-less SolidWorks loft): cubic Beziers with handles SP_BEND_TENSION x chord / 3 long.
    Each side face is the single ruled B-spline surface between two neighbouring corner curves (the SolidWorks loft's `surf` faces)."""
    def corner(p0, p1):
        k = SP_BEND_TENSION * math.dist(p0[:2], p1[:2]) / BEZIER_DEG
        return b.Edge.make_bezier(b.Vector(*p0), b.Vector(p0[0] + k, p0[1], p0[2]), b.Vector(p1[0], p1[1] + k, p1[2]), b.Vector(*p1))
    c = [corner(p0, p1) for p0, p1 in zip(a_pts, mid_pts)]
    sides = [b.Face.make_surface_from_curves(c[k], c[(k + 1) % len(c)]) for k in range(len(c))]
    return b.Solid(b.Shell(sides + [_quad(b, *a_pts), _quad(b, *mid_pts)]))


def nose_body(b):
    """The nose block (STEP RV23): the swing's outer cone swept straight on by SP_NOSE_RUN along +Y, so its outer face is the battered plane
    to the sweep end and then a quarter cone (same 40 deg lean, same radius law) about the axis there; its inner face is the plane X = swing
    axis. Un-trimmed in height / ramp (side._side_body cuts those)."""
    (cx, cy), z1 = SP_FRONT["c"], SP_NOSE_Z[1]
    sec = lambda y: _quad(b, *[(cx - _swing_r(1, FLOOR_Z), y, FLOOR_Z), (cx, y, FLOOR_Z), (cx, y, z1), (cx - _swing_r(1, z1), y, z1)])
    run = b.Solid.extrude(sec(cy), b.Vector(0, SP_NOSE_RUN, 0))
    return _U(run, _spin(b, sec(cy + SP_NOSE_RUN), (cx, cy + SP_NOSE_RUN), -90.0))


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
