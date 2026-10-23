"""[fix-B] Weapon mounts RV02/RV03: profile, notch, standoff screws, stator holes, motor back spacer.

[fix-B-rebuild] One plate builder for both mounts, in the mount frame (MNT_FRAME: x out from the inner face, y, z from
the weapon axis): a build123d side sketch (teardrop round the axis, nose round the SB standoff, heel and the notch over
the chassis tab) from the chassis features it fits and the per-side MNT_SIDE masters, extruded as a slab plus a
battered boss, holes as patterns. RV03 is built as drawn; RV02 is the same builder with its own profile masters,
mirrored to -X. Placed on MNT_FRAME (the joint rig's mount frames)."""
import math
import os
import sys

import build123d as bd

from . import plate as pl
from .common import _U, _b, _m2, _polar, _tangent_line_circle
from .params_chassis import HERE, MNT_IN, MNT_SLAB_T, MNT_T, SA, SB, TOP_Z0, WY, WZ
from .params_weapon import (BIG, MNT_ABOVE_RIM_X, BOSS_OVER, BRG_SEAT_R, BSP, BSP_T, CB_FLOOR_X, CB_R,
                            HOLE_FACE_RISE, LEAD_FLOOR_W, LEAD_GROOVE_R, LEAD_GROOVE_X, LEAD_MOUTH, LEAD_ROUND, MNT_FRAME,
                            MNT_HEEL, MNT_NOTCH_GAP, MNT_NOTCH_UP, MNT_RELIEF_R, MNT_SCREW, MNT_SCREW_FIT, MNT_CSK_CLEAR, MNT_SIDE,
                            MNT_TIP_REACH, MNT_TIP_WALL, MNT_TOP_Z, N_STACK, NOSE_PAD_R, NOSE_R, NUT_RECESS_R,
                            LEAD_GROOVE, RV03_BORE_R, STATOR_HOLES, STATOR_SCREW_FIT, TAB, WM_DES, boss_line_z, lead_groove_ends)

AXIS = bd.Vector(WY, WZ)   # the weapon axis in the chassis side view (Y, Z): the mount frame's origin in that view


def stator_bolt_circle():
    """(dY, dZ) of the weapon motor's base screws about the weapon axis (STATOR_HOLES, from the motor catalog entry;
    GR1507: one per arm of the stator cross on its 12 mm PCD). RV03's counterbores, the back spacer's holes and the
    reference deviations all use this one pattern."""
    return [(dy, dz) for dy, dz, _ in STATOR_HOLES]


def _v(p):
    return bd.Vector(*p)


def _at(c, r, deg):
    return _v(c) + bd.Vector(r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))


# ------------------------------------------------------------------------------------------------- side profile
def _tab():
    """The chassis tab the notch drops over (side view, chassis Y, Z): rear Y0 to the front face Y1 + MNT_NOTCH_GAP,
    floor Z0, height h, its two front corners chamfered `cham` (STEP RV02/RV03 notch). The tub is cut by the real
    mount, so its tab takes this shape (the STEP tub tab has the same chamfers)."""
    t = dict(TAB, y1=TAB["y1"] + MNT_NOTCH_GAP)
    zt = t["z0"] + t["h"]
    return bd.Polygon((t["y0"], t["z0"]), (t["y1"] - t["cham"], t["z0"]), (t["y1"], t["z0"] + t["cham"]), (t["y1"], zt - t["cham"]),
                      (t["y1"] - t["cham"], zt), (t["y0"], zt), align=None)


def _outline(m):
    """Closed side outline (chassis Y, Z) of the plate before the notch: notch top -> tangent -> teardrop rim (top_r
    round the axis) -> front edge -> nose arc (NOSE_R round SB) -> flat underside -> heel hooked under the tab ->
    rear face up the tab's rear Y -> leaned top-rear corner -> notch top."""
    t, h = TAB, MNT_HEEL
    top = _v((m["notch_y"], MNT_TOP_Z))
    t0 = _v(_tangent_line_circle((m["notch_y"], MNT_TOP_Z), (WY, WZ), m["top_r"], upper=True))
    a0 = math.degrees(math.atan2(t0.Y - AXIS.Y, t0.X - AXIS.X))
    rim1 = _at(AXIS, m["top_r"], m["rim_end"])
    nose_a0 = m["rim_end"]                               # front edge = common tangent of the rim and the nose arc: same normal angle
    nose0, nose1 = _at(SB, NOSE_R, nose_a0), _at(SB, NOSE_R, -90.0)
    # heel lip -> tab floor: the corner relief (MNT_RELIEF_R, tangent to the lip) runs out on the tab's rear-bottom
    # corner, the lip under the tab being shorter than the relief radius
    relief = MNT_RELIEF_R > 0
    if relief:
        rc = (t["y0"] - math.sqrt(MNT_RELIEF_R ** 2 - (h["z_lip"] + MNT_RELIEF_R - t["z0"]) ** 2), h["z_lip"] + MNT_RELIEF_R)
        lip_end = (rc[0], h["z_lip"])
    else:
        lip_end = (t["y0"], h["z_lip"])                  # the STEP's sharp corner where the lip meets the tab's rear face
    heel = [nose1, (t["y0"] + h["step"], h["z"]), (t["y0"] - h["back"], h["z_hook"]), (t["y0"] - h["back"], h["z_lip"]), lip_end]
    rear = [(t["y0"], t["z0"]), (t["y0"], MNT_TOP_Z - MNT_NOTCH_UP), (t["y0"] - MNT_NOTCH_UP, MNT_TOP_Z), top, t0]
    edges = [bd.Edge.make_three_point_arc(t0, _at(AXIS, m["top_r"], (a0 + m["rim_end"]) / 2), rim1), bd.Edge.make_line(rim1, nose0),
             bd.Edge.make_three_point_arc(nose0, _at(SB, NOSE_R, (nose_a0 - 90.0) / 2), nose1)]
    if relief:
        a_end = math.degrees(math.atan2(t["z0"] - rc[1], t["y0"] - rc[0]))
        edges.append(bd.Edge.make_three_point_arc(_v(lip_end), _at(rc, MNT_RELIEF_R, (-90.0 + a_end) / 2), _v(rear[0])))
    else:
        edges.append(bd.Edge.make_line(_v(lip_end), _v(rear[0])))
    edges += [bd.Edge.make_line(_v(p), _v(q)) for line in (heel, rear) for p, q in zip(line, line[1:])]
    f = bd.Face(bd.Wire(edges))
    return f if f.normal_at().Z > 0 else -f              # counter-clockwise, so it fuses with the pad circle


def mount_profile(side):
    """Side sketch of a mount (chassis Y, Z): the outline, a pad round the nose CSK (NOSE_PAD_R = CSK cone + a printed
    wall: the STEP nose arc left the cone a 0 mm knife edge), the notch-top wedge thickened to MNT_TIP_WALL within
    MNT_TIP_REACH (rearmost point kept), concave corners relieved MNT_RELIEF_R, then the notch: the tab cut out, its
    corners sharp as the tab's."""
    m = MNT_SIDE[side]
    p = _outline(m)
    if NOSE_PAD_R:
        p = p + bd.Pos(*SB) * bd.Circle(NOSE_PAD_R)
    if MNT_TIP_WALL:
        top = _v((m["notch_y"], MNT_TOP_Z))
        zone = (bd.Pos(*top) * bd.Circle(MNT_TIP_REACH)) & (bd.Pos(*top) * bd.Rectangle(MNT_TIP_REACH, MNT_TIP_REACH, align=bd.Align.MIN))
        p = p + (bd.offset(p, MNT_TIP_WALL / 2, kind=bd.Kind.ARC) & zone)
    tab = _tab()
    return pl.round_corners(p, r_in=MNT_RELIEF_R, keep=tab.vertices()) - tab


def _boss_zone(prof):
    """Side region of the boss: above the line from the notch top to the nose (boss_line_z), and above the notch top
    behind the tab (the leaned rear corner), out to the profile's own extent."""
    bb = prof.bounding_box()
    y0, y1, z1 = bb.min.X, bb.max.X, bb.max.Y
    return bd.Polygon((TAB["y0"], MNT_TOP_Z), (y1, boss_line_z(y1)), (y1, z1), (y0, z1), (y0, MNT_TOP_Z), align=None)


def _side_plane(x):
    """The mount frame's side-view plane at x (out from the inner face): sketch (u, v) = chassis (Y, Z) - axis."""
    return bd.Plane(origin=(x, -WY, -WZ), x_dir=(0, 1, 0), z_dir=(1, 0, 0))


def _prism(sk, x0, x1):
    return bd.extrude(_side_plane(x0) * sk, amount=x1 - x0)


def _batter(m):
    """The battered outer face as a plane in the mount frame (x = MNT_T - drop - lean*z - toe*y)."""
    b = m["batter"]
    return bd.Plane(origin=(MNT_T - b["drop"], 0, 0), z_dir=(1, b["toe"], b["lean"]))


def batter_x(side, y, z):
    """x (mount frame) of the battered outer face at (y, z) about the axis."""
    b = MNT_SIDE[side]["batter"]
    return MNT_T - b["drop"] - b["lean"] * z - b["toe"] * y


# ------------------------------------------------------------------------------------------- phase-lead groove
def lead_groove_section(half=False):
    """[(kind, points)] outline in (u = world X, v = offset across the run) of RV03's phase-lead C-groove section: the
    round channel (LEAD_GROOVE_R) on u = LEAD_GROOVE_X, opened to the inner face by the LEAD_MOUTH slot through the
    LEAD_LIP lip, the lip / channel chord filleted LEAD_ROUND (it was a sharp crease, mfg.sharp_internal_corner), a
    LEAD_FLOOR_W flat on the channel floor (the revolved ends then close on a flat, not on a degenerate pole: integrity.solids).
    kind 'l' = line (2 points), 'a' = arc (3 points); half=True gives the v >= 0 half closed on v = 0."""
    X, R, h, r = LEAD_GROOVE_X, LEAD_GROOVE_R, LEAD_MOUTH / 2, LEAD_ROUND
    u0 = MNT_IN - LEAD_ROUND                                                   # slot starts outside the part
    uc = X - math.sqrt((R + r) ** 2 - (h + r) ** 2)                           # fillet centre (uc, h + r): on the lip side, tangent to both
    k = R / (R + r)
    t = (X + k * (uc - X), k * (h + r))                                       # fillet / channel tangent point
    def fm(sg):   # fillet arc midpoint on the side sg
        a0, a1 = math.atan2(-r, 0.0), math.atan2(t[1] - (h + r), t[0] - uc)
        a = (a0 + a1) / 2
        return (uc + r * math.cos(a), sg * (h + r + r * math.sin(a)))
    top = [("l", [(u0, h), (uc, h)]), ("a", [(uc, h), fm(1), t])]
    w = LEAD_FLOOR_W / 2                                                      # flat floor strip: the revolved ends get a flat, not a pole on the surface
    ta, fa = math.atan2(t[1], t[0] - X), math.asin(w / R)
    am = (ta + fa) / 2
    f = (X + R * math.cos(fa), w)
    arc = lambda sg: ("a", [(t[0], sg * t[1]), (X + R * math.cos(am), sg * R * math.sin(am)), (f[0], sg * w)])   # noqa: E731
    if half:
        return [("l", [(u0, 0.0), (u0, h)])] + top + [arc(1), ("l", [f, (f[0], 0.0)]), ("l", [(f[0], 0.0), (u0, 0.0)])]
    rev = lambda e: (e[0], e[1][::-1])   # noqa: E731
    return ([("l", [(u0, -h), (u0, h)])] + top + [arc(1), ("l", [f, (f[0], -w)]), rev(arc(-1)), ("a", [(t[0], -t[1]), fm(-1), (uc, -h)]), ("l", [(uc, -h), (u0, -h)])])


def lead_groove():
    """Cutter of RV03's phase-lead C-groove: lead_groove_section() swept along the run between the lead_groove_ends(),
    each end closed by its half section revolved half a turn about the X line through it (a round end matching the section)."""
    bb = _b()
    (y0, z0), (y1, z1) = lead_groove_ends()
    L = math.hypot(y1 - y0, z1 - z0)
    ry, rz = (y1 - y0) / L, (z1 - z0) / L
    def face(y, z, outline):
        P = lambda q: bb.Vector(q[0], y - q[1] * rz, z + q[1] * ry)   # noqa: E731
        return bb.Face(bb.Wire([bb.Edge.make_line(*map(P, q)) if kd == "l" else bb.Edge.make_three_point_arc(*map(P, q)) for kd, q in outline]))
    body = bb.Solid.extrude(face(y0, z0, lead_groove_section()), bb.Vector(0, y1 - y0, z1 - z0))
    # half a turn each, outwards only: a full turn would lie on the swept prism's own faces (coincident boolean faces)
    ends = [bb.Solid.revolve(face(y, z, lead_groove_section(half=True)), 180, bb.Axis((0, y, z), (k, 0, 0))) for (y, z), k in (((y0, z0), 1), ((y1, z1), -1))]
    return _U(body, *ends)


# --------------------------------------------------------------------------------------------------------- the plate
def _plate(side):
    """Mount body in the mount frame, outboard = +x: a slab (MNT_SLAB_T) carrying the
    full profile, and the boss over the rest of MNT_T on the boss zone, its outer face battered (split on _batter)."""
    m = MNT_SIDE[side]
    prof = mount_profile(side)
    slab = _prism(prof, 0.0, MNT_SLAB_T)
    boss = _prism(prof & _boss_zone(prof), MNT_SLAB_T, MNT_T + BOSS_OVER).split(_batter(m), keep=bd.Keep.BOTTOM)
    return _U(slab, boss)


def _bore(r, x0, x1):
    """Cylinder r on the weapon axis from x0 to x1 (mount frame)."""
    return bd.Solid.make_cylinder(r, x1 - x0, bd.Plane(origin=(x0, 0, 0), z_dir=(1, 0, 0)))


def _hole_tool():
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    return hole_tool


def _to_mount(p, side="r", world=True):
    """A mount-frame point in world coordinates (world=True), else as is; the mirrored RV02 frame flips x."""
    if not world:
        return p
    s = 1 if side == "r" else -1
    o = MNT_FRAME[side]
    return (o[0] + s * p[0], o[1] + p[1], o[2] + p[2])


def _mount_csk(s, y, z, fastener, world=True):
    """robot.cad.holes cutter + record for a mount-to-standoff M3 CSK (bolt_u*) at chassis (y, z): head flush in the
    inner face, DIN 7991 countersink (dk 6.0 head in the STEP's 6.2 mm cone) and ISO 273 loose clearance through the
    slab, so the notch, not the shank, takes fore/aft load. world=False: in the (unmirrored) mount frame."""
    side = "r" if s > 0 else "l"
    p = _to_mount((0.0, y - WY, z - WZ), side, world)
    d = (s, 0, 0) if world else (1, 0, 0)
    return _hole_tool()(p, d, fastener, head="csk", into="through", side="head", grip=MNT_SLAB_T, fit=MNT_SCREW_FIT, csk_clear=MNT_CSK_CLEAR)


def _stator_hole(s, dy, dz, world=True, des=WM_DES):
    """robot.cad.holes cutter + record for one RV03 stator screw (bolt_wm*): M2x8 button through RV03, head on the
    counterbore floor (STEP CB_FLOOR_X); the counterbore opens on the battered face, measured from its highest
    point over the hole (HOLE_FACE_RISE)."""
    from robot.cad import fastener_catalog as fc
    b = MNT_SIDE["r"]["batter"]
    x = batter_x("r", dy, dz) + HOLE_FACE_RISE * math.hypot(b["lean"], b["toe"])
    d = fc.parse(des).d
    cut, rec = _hole_tool()(_to_mount((x, dy, dz), "r", world), (-s, 0, 0), des, head="button", into="through", side="head",
                            grip=x, cbore=x - (CB_FLOOR_X - MNT_IN), cbore_clear=2 * CB_R - fc.head(d, "button")[0], fit=STATOR_SCREW_FIT)
    return (cut.solids()[0] if hasattr(cut, "solids") and len(cut.solids()) == 1 else cut), rec


def _stack_hole(fastener, x, y, z, sx, grip):
    """robot.cad.holes record of an M2 button screw on the weapon axis direction sx: clearance through `grip` mm, tapped beyond."""
    return _hole_tool()((x, y, z), (sx, 0, 0), fastener, head="button", into="tapped", side="both", grip=grip, fit="close")[1]


def _notch_clip(body):
    """[cut] above the rim the mount rises through the top panel's front notch: clear its outer edge (MNT_ABOVE_RIM_X, mount
    frame) when a narrow chassis pulls the notch in (hyp: mount/top_panel overlap at width -10 %); None when nothing pokes past."""
    z0 = TOP_Z0 - WZ
    cut = bd.Solid.make_box(BIG, 2 * BIG, BIG, bd.Plane(origin=(MNT_ABOVE_RIM_X, -BIG, z0)))
    return cut if (body & cut).volume > 0.01 else None   # mm3: ignore a boolean sliver on the line


def weapon_mount(side):
    """RV02 (left, shaft end) / RV03 (right, stator): 8 mm printed XALT HD plates. A slab carries the full profile; the
    boss above the standoff line has its outer face battered (leans in) so side hits glance off. The rear notch drops
    over the chassis tab: the tab, not the screws, takes fore/aft load. Built in the mount frame (RV02 mirrored)."""
    body = _plate(side)
    cuts = [_mount_csk(1, y, z, f, world=False)[0] for (y, z), f in zip((SA, SB), MNT_SCREW)]   # M3 CSK into the standoffs
    if side == "r":
        cuts.append(_bore(RV03_BORE_R, -MNT_T, 2 * MNT_T))                                      # centre hole behind the shaft end
        cuts += [_stator_hole(1, dy, dz, world=False)[0] for dy, dz in stator_bolt_circle()]     # GR1507 stator M2
        if LEAD_GROOVE:                                                                          # optional variant: snap-in channel for the phase leads
            cuts.append(lead_groove().moved(bd.Location(tuple(-v for v in MNT_FRAME["r"]))))
    else:
        cuts.append(_bore(BRG_SEAT_R, -MNT_T, 2 * MNT_T))                                        # outboard bearing seat (MR85, pressed)
        cuts.append(_bore(NUT_RECESS_R, MNT_SLAB_T, 2 * MNT_T))                                  # shaft nut recess
    clip = _notch_clip(body)
    if clip is not None:
        cuts.append(clip)
    part = body.cut(*cuts).clean()
    if clip is not None and not part.is_valid:
        part = part.fix()   # the clip lands on RV03's batter seam (the uncut plate is not valid on its own; the default never clips)
    part = part if side == "r" else part.mirror(bd.Plane.YZ)
    return pl.placed(part.solids()[0] if len(part.solids()) == 1 else part, MNT_FRAME[side])


# ----------------------------------------------------------------------------------------------- motor back spacer
def motor_back_spacer():
    """1.5 mm printed spacer between the weapon motor's stator base and RV03 (mount frame, inboard of the inner face):
    clears the motor's rear bearing boss and wires; close clearance holes for the stator screws (motor catalog), N_STACK
    windows midway between them."""
    from robot.cad import fastener_catalog as fc
    b = BSP
    win = pl.ring_window(b["win_in"], b["win_out"], b["half_deg"], b["round_out"], b["round_in"])
    sk = (bd.Circle(b["r"]) - bd.Circle(b["bore_r"]) - pl.polar(win, N_STACK, b["phase"])
          - [bd.Pos(dy, dz) * bd.Circle(fc.clearance(d, "close") / 2) for dy, dz, d in STATOR_HOLES])
    plane = bd.Plane(origin=(-BSP_T, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    return pl.placed(bd.extrude(plane * sk, amount=BSP_T), MNT_FRAME["r"])


# ------------------------------------------------------------------------------------- 2D views for the wedgelet
def _mount_profile(side, tol=0.005):
    """mount_profile() as a shapely polygon (chassis Y, Z), its edges sampled to `tol` chord: the wedgelet's nose tab
    and the profile tests work in shapely."""
    from shapely.geometry import Polygon
    f = mount_profile(side).faces()[0]

    def ring(w):
        pts = []
        for e in w.order_edges():
            n = 1 if e.geom_type == bd.GeomType.LINE else max(2, int(math.ceil(e.length / math.sqrt(8 * tol * e.radius))))
            pts += [(q.X, q.Y) for q in (e.position_at(k / n) for k in range(n))]
        return pts
    return Polygon(ring(f.outer_wire()), [ring(w) for w in f.inner_wires()]).buffer(0)


def _mount_clip():
    """The boss zone as a shapely half-plane (above the notch-top-to-nose line, run on to Y = BIG) for the wedgelet."""
    from shapely.geometry import Polygon
    return Polygon([(TAB["y0"], MNT_TOP_Z), (BIG, boss_line_z(BIG)), (BIG, BIG), (0, BIG), (0, MNT_TOP_Z)])
