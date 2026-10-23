"""[fix-C] Revron hubs group: rear / front hubs, tyres and standoffs.

Hubs and tyres are drawn in their own frame (spin axis = +X, inner face at x = 0) and placed by the rig (`rig_wheels`): one solid
per kind serves both sides, the left one is the right one turned half a turn about Z (the hubs are axisymmetric apart from the
D-bore, whose flat stays on top)."""
import math
from .params_drive import (RH_GAP, RH_D, RH_SEAT_R, RH_FLANGE_R, RH_FLANGE_T, RH_BLOCK, RH_GROOVE_DEPTH, RH_GROOVE_FLOOR, RH_GROOVE_FILLET,
                           RH_CROWN_H, RH_CROWN_W, RH_ROOT_R, RH_LIP_R, RH_LIP_ANG, RH_LEN, RH_WALL_R, RH_WALL_T, RH_BORE_X, RH_NUT_X, RH_NUT_HALF, RH_NUT_Z, RH_GRUB_X, RH_GRUB_D, HUB_GRUB_PRINTABLE, RH_ORIGIN_X, RH_ROOT_X,
                           FH_BORE_R, FH_FLANGE_R, FH_SEAT_R, FH_FLANGE_T, FH_GROOVE_W, FH_SEAT_W, FH_FILLET, FH_GUSSET, FH_LEN, FH_ORIGIN_X,
                           TY_REAR, TY_FRONT, TY_ARC_STEP, SO_R, SO_CHAMFER, SO_TAP_R, SO_PITCH, SO_THREAD_H)
from .params_chassis import SA, RY, RZ, CH_HALF_W, SA_X
from .params_hardware import HUB_PIVOT_X
from .common import _b, _S, _ext, _cyl, _box, _face, _revolve_x


def _d_outline(d=RH_D):
    from shapely.geometry import Polygon
    fa = math.asin(d["flat"] / d["r"])
    hx = d["r"] * math.cos(fa)
    a0, span = math.pi - fa, math.pi + 2 * fa
    arc = [(d["r"] * math.cos(a0 + span * k / (d["arc_n"] - 1)), d["r"] * math.sin(a0 + span * k / (d["arc_n"] - 1))) for k in range(d["arc_n"])]
    n = max(2, round(2 * hx / (d["r"] * span) * d["arc_n"]))                              # flat facets as long as the arc's
    flat = [(hx - 2 * hx * k / n, d["flat"] - d["crown"] * math.sin(math.pi * k / n)) for k in range(1, n)]
    return Polygon(arc + flat)


def _grub():
    from robot.cad.holes import hole_tool
    top = RH_SEAT_R
    if not HUB_GRUB_PRINTABLE:                                                # STEP Cut-Extrude4: plain bore from the D-bore up through the wall (nothing below the bore)
        return _cyl(RH_GRUB_D / 2, 0, top, (RH_GRUB_X - RH_ORIGIN_X, 0), "z")
    x = RH_GRUB_X - RH_ORIGIN_X - (0.2 if HUB_GRUB_PRINTABLE else 0)
    return hole_tool((x, 0, top), (0, 0, -1), "M2x5" if HUB_GRUB_PRINTABLE else "M3x5", head="cap", into="tapped", side="thread",
                     engage=top - RH_D["flat"])[0]


def _nut_slot():
    z0, z1 = RH_NUT_Z
    return _box(RH_BORE_X - RH_ORIGIN_X, RH_NUT_X - RH_ORIGIN_X, -RH_NUT_HALF, RH_NUT_HALF, z0, z1)


def _round_corner(a, b, c, r):
    """Points rounding the vertex b of the polyline a-b-c with a fillet of radius r (tangent points and the arc between)."""
    u1, u2 = (a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1])
    u1 = (u1[0] / math.hypot(*u1), u1[1] / math.hypot(*u1))
    u2 = (u2[0] / math.hypot(*u2), u2[1] / math.hypot(*u2))
    half = math.acos(max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))) / 2
    d, m = r / math.tan(half), (u1[0] + u2[0], u1[1] + u2[1])
    m = (m[0] / math.hypot(*m), m[1] / math.hypot(*m))
    cen = (b[0] + m[0] * r / math.sin(half), b[1] + m[1] * r / math.sin(half))
    a1 = math.degrees(math.atan2(b[1] + u1[1] * d - cen[1], b[0] + u1[0] * d - cen[0]))
    a2 = math.degrees(math.atan2(b[1] + u2[1] * d - cen[1], b[0] + u2[0] * d - cen[0]))
    if a2 - a1 > 180:
        a2 -= 360
    elif a1 - a2 > 180:
        a2 += 360
    return _arc(cen, r, a1, a2)


def _rear_profile():
    """RV21 section (x, r) from the inner face: flange | O-ring groove (r0.2 floor corners) | flange | R1 root | seat with the
    crown (45 deg flanks, centred on the tyre) | lip slope | end face with the shallow recess."""
    f, t, g, s = RH_FLANGE_R, RH_FLANGE_T, RH_GROOVE_DEPTH, RH_SEAT_R
    x0 = t + (RH_BLOCK - 2 * t - RH_GROOVE_FLOOR) / 2           # groove floor span (the walls slope down to it)
    x1 = x0 + RH_GROOVE_FLOOR
    c, ch, w2 = RH_BLOCK + TY_REAR["w"] / 2, RH_CROWN_H, RH_CROWN_W / 2
    lip = (RH_LIP_R - s) / math.tan(math.radians(RH_LIP_ANG))
    return [(0, 0), (0, f), (t, f), *_round_corner((t, f), (x0, f - g), (x1, f - g), RH_GROOVE_FILLET),
            *_round_corner((x0, f - g), (x1, f - g), (RH_BLOCK - t, f), RH_GROOVE_FILLET), (RH_BLOCK - t, f), (RH_BLOCK, f),
            (RH_BLOCK, s + RH_ROOT_R), *_arc((RH_BLOCK + RH_ROOT_R, s + RH_ROOT_R), RH_ROOT_R, 180, 180 + 90)[1:],
            (c - w2 - ch, s), (c - w2, s + ch), (c + w2, s + ch), (c + w2 + ch, s), (RH_LEN - lip, s), (RH_LEN, RH_LIP_R),
            (RH_LEN, RH_WALL_R), (RH_LEN - RH_WALL_T, RH_WALL_R), (RH_LEN - RH_WALL_T, 0)]


def rear_hub():
    """RV21 rear hub in its own frame: axis +X through the origin, inner face x = 0."""
    body = _spin(_rear_profile())
    return _S(body, _ext(_d_outline(), "yz", RH_BORE_X - RH_ORIGIN_X, RH_NUT_X - RH_ORIGIN_X), _nut_slot(), _grub())


def _arc(c, r, a0, a1):
    n = max(2, int(abs(a1 - a0) / TY_ARC_STEP) + 1)
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / (n - 1))), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / (n - 1)))) for k in range(n)]


def _spin(pts):
    """Solid of revolution about +X of a closed (x, r) outline; arcs are true arcs."""
    from shapely.geometry import Polygon
    b = _b()
    return b.Solid.revolve(_face(Polygon(pts), "xz", arcs=True)[0], 360, b.Axis((0, 0, 0), (1, 0, 0)))


def front_hub():
    """RV19 micro hub: flange | O-ring groove (r0.5 roots) | flange | 6 mm tyre seat (45 deg gussets at its ends) | flange."""
    t, f, g, r, c = FH_FLANGE_T, FH_FLANGE_R, FH_GROOVE_W, FH_FILLET, FH_GUSSET
    x1, x2 = t, t + g   # groove walls
    seat0, seat1 = x2 + t, x2 + t + FH_SEAT_W
    pts = [(0, FH_BORE_R), (0, f), (x1, f), (x1, FH_SEAT_R + r), *_arc((x1 + r, FH_SEAT_R + r), r, 180, 180 + 90)[1:],
           *_arc((x2 - r, FH_SEAT_R + r), r, 180 + 90, 360)[:-1], (x2, FH_SEAT_R + r), (x2, f), (seat0, f), (seat0, FH_SEAT_R + c), (seat0 + c, FH_SEAT_R),
           (seat1 - c, FH_SEAT_R), (seat1, FH_SEAT_R + c), (seat1, f), (FH_LEN, f), (FH_LEN, FH_BORE_R)]
    return _spin(pts)


def rear_tyre():
    """RV22 F1 tyre: OD 21.5 x 9.5 wide, 1 x 45 deg chamfers, r0.5 on the chamfer / face / bore edges, bore 12 with the 7 x 2.5 centre groove."""
    from shapely.geometry import Polygon
    t = TY_REAR
    R, w, ch, fr, rb = t["od"] / 2, t["w"], t["chamfer"], t["fillet"], t["bore"] / 2
    body = Polygon([(0, rb), (0, R - ch), (ch, R), (w - ch, R), (w, R - ch), (w, rb)])
    body = body.buffer(-fr, join_style=1, quad_segs=int(90 / TY_ARC_STEP)).buffer(fr, join_style=1, quad_segs=int(90 / TY_ARC_STEP))   # r0.5 on every convex edge of the section
    g0, g1 = (w - t["groove_w"]) / 2, (w + t["groove_w"]) / 2
    sec = body.difference(Polygon([(g0, rb - 1), (g1, rb - 1), (g1, t["groove_r"]), (g0, t["groove_r"])]))
    b = _b()
    return b.Solid.revolve(_face(sec, "xz", arcs=True)[0], 360, b.Axis((0, 0, 0), (1, 0, 0)))


def front_tyre():
    """RV20 micro tyre: ring OD 11 / ID 7 x 6 wide, 0.2 x 45 deg chamfer on all four edges."""
    t = TY_FRONT
    R, r, w, c = t["od"] / 2, t["id"] / 2, t["w"], t["chamfer"]
    return _spin([(0, r + c), (c, r), (w - c, r), (w, r + c), (w, R - c), (w - c, R), (c, R), (0, R - c)])


def rig_wheels(r, s, n):
    """Joints / mates of the wheel group: rear hub on the N10 D-shaft (pivot = hub spin joint), front hub on the 25 mm standoff axle,
    each tyre on its hub's tyre seat (flange wall, end of the flange land)."""
    r.joint(f"whub_r{n}", "d_bore", (HUB_PIVOT_X["rear"] - RH_ORIGIN_X, 0, 0))
    r.joint(f"whub_r{n}", "tyre_seat", (RH_ROOT_X, 0, 0))
    r.joint(f"wheel_r{n}", "inner", (0, 0, 0))
    r.mate(f"whub_r{n}", "tyre_seat", f"wheel_r{n}", "inner")
    r.joint(f"whub_f{n}", "bore", (HUB_PIVOT_X["front"] - FH_ORIGIN_X, 0, 0))
    r.joint(f"whub_f{n}", "tyre_seat", (2 * FH_FLANGE_T + FH_GROOVE_W, 0, 0))
    r.joint(f"wheel_f{n}", "inner", (0, 0, 0))
    r.mate(f"whub_f{n}", "tyre_seat", f"wheel_f{n}", "inner")
    # the designer's other mates of the wheel group (each re-derives the pose the chain above already gives)
    flip = (0, 0, 0 if s > 0 else 180)
    r.joint("tub", f"wheel_face_{n}", (s * RH_ORIGIN_X, RY, RZ), flip)              # Distance2: rear hub inner face RH_GAP off the chassis wall
    r.joint(f"whub_r{n}", "inner_face", (0, 0, 0))
    r.mate("tub", f"wheel_face_{n}", f"whub_r{n}", "inner_face")
    r.joint(f"whub_r{n}", "front_plane", (0, (SA[0] - RY) * s, SA[1] - RZ))         # Coincident82: front hub inner face in the same plane (its axis at SA)
    r.joint(f"whub_f{n}", "inner_face", (0, 0, 0))
    r.mate(f"whub_r{n}", "front_plane", f"whub_f{n}", "inner_face")
    r.joint("tub", f"so_a_bore_{n}", (s * SA_X[0], *SA))                            # Concentric5: the 25 mm standoff in the chassis bore
    r.mate("tub", f"so_a_bore_{n}", f"so_a{n}", "inner_end")
    r.joint(f"side_{n}", "wheel_axis", (s * HUB_PIVOT_X["front"], *SA), flip)           # Concentric83: the side panel's axle hole on the front hub bore
    r.mate(f"side_{n}", "wheel_axis", f"whub_f{n}", "bore")


def standoff_end(L_x, c):
    """The standoff's outboard end: (point, outward axis). The side panel's SA boss seats on it."""
    x = max(L_x, key=abs)
    return (x, *c), (x / abs(x), 0.0, 0.0)


def _thread_bore(L):
    """Inner wall of the tapped M3 bore from x = L to 0 as (x, r) points: the minor cylinder with a groove per pitch (60 deg flanks,
    flat root P/8, depth 5/8 H): the STEP's swept thread as rings, so the volume and the see-through minor bore are the thread's."""
    P, h, land = SO_PITCH, SO_THREAD_H, SO_PITCH / 8
    half = (land + 2 * h * math.tan(math.radians(30))) / 2
    pts = []
    for k in range(round(L / P) - 1, -1, -1):
        c = (k + 0.5) * P
        pts += [(c + half, SO_TAP_R), (c + land / 2, SO_TAP_R + h), (c - land / 2, SO_TAP_R + h), (c - half, SO_TAP_R)]
    return pts


def standoff(L_x, c):
    """RV10 / RV11 standoff: tube with the tapped M3 bore (thread as ring grooves) and the 0.2 x 45 deg end chamfers."""
    b = _b()
    x0, L, ch = min(L_x), abs(L_x[1] - L_x[0]), SO_CHAMFER
    s = _revolve_x([(0, SO_TAP_R), (0, SO_R - ch), (ch, SO_R), (L - ch, SO_R), (L, SO_R - ch), (L, SO_TAP_R), *_thread_bore(L)], x0, c)
    p, z = standoff_end(L_x, c)
    b.RigidJoint("end", s, b.Location(b.Plane(origin=p, z_dir=z)))   # [fix-C-j1] the panel's `sa` joint connects here
    return s
