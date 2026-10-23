"""[fix-C] Revron fork: the fork_5 sketch in its own frame (origin on the standoff axis), placed on the 15 mm standoff by the rig.

Driving dims are the designer's (Mirrorfork 5 sketch: hole, pin hole and distance/angle, tip, 2 mm rails, r0.2 fillet, 1.5 mm
sheet); the eye and boss rings, tangent edges, window and tip land are relations of those. One solid serves both sides: the
STEP places the same part at two X offsets and two tilts, so there is no mirror."""
import math
from .params_drive import (FK_EYE_D, FK_PIN_D, FK_PIN_DIST, FK_PIN_ANG, FK_TIP, FK_RAIL, FK_FILLET, FK_T, FK_WEB, FK_KERF,
                           FK_BOT_ANG, FK_X0, FK_TILT, FK_RES)
from .params_chassis import SB, SB_X, SB_X_STOCK
from .common import _ext, _round, _b


def _tangent_top(t, r):
    """Tangent point on the circle (origin, r) of the upper tangent from the external point t."""
    d = math.hypot(*t)
    ph = math.atan2(t[1], t[0]) - math.acos(r / d)    # the larger-y tangent of the two for a tip behind and below the eye
    pts = [(r * math.cos(a), r * math.sin(a)) for a in (math.atan2(t[1], t[0]) + math.acos(r / d), ph)]
    return max(pts, key=lambda p: p[1])


def fork_outline(window=True):
    """fork_5 laser outline in the sketch frame (u back along the blade, v up), standoff axis at the origin; window=False leaves the
    lightening window filled (the wedgelet's slit has no island in it)."""
    from shapely.geometry import Point, Polygon
    r_eye = FK_EYE_D / 2
    a = math.radians(90 - FK_PIN_ANG)
    pin = (FK_PIN_DIST * math.cos(a), FK_PIN_DIST * math.sin(a))
    r_pin, r_hole = FK_PIN_D / 2, r_eye - FK_WEB
    r_boss = r_pin + FK_WEB                                               # boss round the pin hole (the STEP's is tangent to the eye's top line: 0.02 smaller)
    tip = (-FK_TIP[0], -FK_TIP[1])
    al = math.radians(FK_BOT_ANG)
    t_top = _tangent_top(tip, r_eye)
    t_low = (r_eye * math.sin(al), -r_eye * math.cos(al))                 # lower edge: tangent to the eye, FK_BOT_ANG off level, down to the tip's level
    x_low = (r_eye - FK_TIP[1] * math.cos(al)) / math.sin(al)
    q = lambda r, c=(0, 0): Point(*c).buffer(r, FK_RES)
    eye = q(r_eye).union(q(r_boss, pin)).convex_hull
    blade = Polygon([tip, t_top, (0, 0), t_low, (x_low, tip[1])])
    m = (t_top[1] - tip[1]) / (t_top[0] - tip[0])                          # upper edge slope: the land is where the knife is 3 kerfs wide
    land = 3 * FK_KERF
    body = eye.union(blade).union(Polygon([tip, (tip[0] + land / m, tip[1]), (tip[0] + land / m, tip[1] + land), (tip[0], tip[1] + land)]))
    body = _round(body, r_out=FK_KERF)                                   # kerf: tip corners r >= kerf
    # lightening window: the blade's two edges offset RAIL inwards, closed at the back by a RAIL run, the eye ring left standing
    n_low = (-math.sin(al), math.cos(al))
    w0 = (x_low, (FK_RAIL - r_eye + math.sin(al) * x_low) / math.cos(al))    # lower rail start (on the offset line, above the lower edge's corner)
    ut = ((t_top[0] - tip[0]), (t_top[1] - tip[1]))
    ut = (ut[0] / math.hypot(*ut), ut[1] / math.hypot(*ut))
    n_up = (ut[1], -ut[0])                                                 # inward normal of the upper edge
    # v0: the upper rail line n_up.(p - tip) = RAIL at the level of w0
    vu = tip[0] + (FK_RAIL - n_up[1] * (w0[1] - tip[1])) / n_up[0]
    v0 = (vu, w0[1])
    tl = (math.cos(al), math.sin(al))
    f = (n_low[0] * (FK_RAIL - r_eye), n_low[1] * (FK_RAIL - r_eye))
    h = math.sqrt(r_eye ** 2 - (r_eye - FK_RAIL) ** 2)
    e_low = (f[0] - tl[0] * h, f[1] - tl[1] * h)                           # lower rail meets the eye ring
    # upper rail meets the eye ring
    d_up = FK_RAIL - (n_up[0] * (0 - tip[0]) + n_up[1] * (0 - tip[1]))     # signed offset of the origin from the rail line
    foot = (n_up[0] * d_up, n_up[1] * d_up)
    hu = math.sqrt(r_eye ** 2 - d_up ** 2)
    e_up = (foot[0] - ut[0] * hu, foot[1] - ut[1] * hu)
    win = Polygon([v0, w0, e_low, (0, 0), e_up]).buffer(0).difference(q(r_eye))   # buffer(0): a small eye makes the outline touch itself
    win = _round(win, r_out=FK_FILLET)                                     # Fillet1: r0.2 on the window's corners
    return body.difference(q(r_hole)).difference(q(r_pin, pin)).difference(win if window else Polygon())


def fork_local(window=True):
    """The fork_5 solid in its own frame (sketch plane at w = 0, sheet FK_T towards +w), joint `seat` at the standoff axis."""
    s = _ext(fork_outline(window), "xy", 0.0, FK_T, arcs=True)
    b = _b()
    b.RigidJoint("seat", s, b.Location((0, 0, 0)))
    return s


def seat_plane(s):
    """Where the fork's frame sits in the robot frame: origin on the standoff axis at X = FK_X0, u back along the blade
    (robot -Y) tilted nose-down, v up, w towards the chassis centre (robot -X for the right fork); the same part both sides."""
    b = _b()
    t = math.radians(FK_TILT[s])
    return b.Plane(origin=(FK_X0[s], *SB), x_dir=(0, -math.cos(t), -math.sin(t)), z_dir=(-1, 0, 0))


def fork_world(s, window=True):
    """The fork where the assembly puts it (for the wedgelet's seat); the spec places the local part by the rig mate."""
    return fork_local(window).moved(_b().Location(seat_plane(s)))


def _fork_slot(s):
    """Seat for the fork tine in the wedgelet nose: exactly the 1.5 mm tine (window and tilt included), so the cut volume
    is the volume the fork fills and nothing else is taken from the TPU."""
    return fork_world(s)


def rig_fork(r, s, n):
    """Mates of fork_5: its `seat` frame (the sketch origin) on the 15 mm standoff axis at the STEP's plane; the right fork is also
    mated to the chassis the way the designer does (Concentric20 sketch hole on the lug bore, Parallel2 lower edge level)."""
    b = _b()
    seat = b.Location(seat_plane(s))
    b.RigidJoint("seat", r._host(f"fork_{n}"), b.Location((0, 0, 0)))
    b.RigidJoint("fork_seat", r._host(f"so_b{n}"), seat)
    r.mate(f"so_b{n}", "fork_seat", f"fork_{n}", "seat")
    if s > 0:
        for lab in ("fork_axis", "fork_level"):
            b.RigidJoint(f"{lab}_{n}", r._host("tub"), seat)
            r.mate("tub", f"{lab}_{n}", f"fork_{n}", "seat")


def rig_nose(r, s, n):
    """Concentric82: the side panel's nose screw hole on the wedgelet's, both on the 15 mm standoff axis."""
    r.joint(f"side_{n}", "nose_axis", (s * SB_X_STOCK[1], *SB))
    r.joint(f"wedgelet_{n}", "nose_axis", (s * SB_X_STOCK[1], *SB))
    r.mate(f"side_{n}", "nose_axis", f"wedgelet_{n}", "nose_axis")
